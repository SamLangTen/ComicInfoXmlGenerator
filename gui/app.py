import customtkinter as ctk
import os
import sys
import threading
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import core logic
from src.scanner import scan_archives
from src.comic_info import ComicInfo
from src.archive import inject_comic_info_xml
from src.scraper.filename_scraper import RegexFilenameScraper, OldSchoolFilenameScraper, LlmFilenameScraper
from src.config_manager import config_manager
from tkinter import filedialog

def safe_set_theme(mode):
    """Safely apply theme to avoid macOS version errors."""
    try:
        ctk.set_appearance_mode(mode)
    except Exception as e:
        print(f"Warning: Could not set appearance mode '{mode}': {e}")

# Initial theme setup
safe_set_theme(config_manager.get("appearance_mode"))

class SettingsForm(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        
        row = 0
        ctk.CTkLabel(self, text="LLM Configuration", font=ctk.CTkFont(size=16, weight="bold")).grid(row=row, column=0, columnspan=2, pady=(10, 20), sticky="w")
        row += 1

        self.llm_url = self._add_setting(row, "Base URL:", "llm_base_url")
        row += 1
        self.llm_key = self._add_setting(row, "API Key:", "llm_api_key", show="*")
        row += 1
        self.llm_model = self._add_setting(row, "Model:", "llm_model")
        row += 1

        ctk.CTkLabel(self, text="UI Configuration", font=ctk.CTkFont(size=16, weight="bold")).grid(row=row, column=0, columnspan=2, pady=(20, 20), sticky="w")
        row += 1

        ctk.CTkLabel(self, text="Appearance:", anchor="w").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        self.appearance_menu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"], command=self._change_appearance)
        self.appearance_menu.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        self.appearance_menu.set(config_manager.get("appearance_mode"))
        row += 1

        ctk.CTkButton(self, text="Save Settings", command=self.save_settings).grid(row=row, column=0, columnspan=2, pady=30)

    def _add_setting(self, row, label, config_key, show=None):
        ctk.CTkLabel(self, text=label, anchor="w").grid(row=row, column=0, padx=10, pady=5, sticky="w")
        entry = ctk.CTkEntry(self, show=show)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        entry.insert(0, config_manager.get(config_key))
        return (entry, config_key)

    def _change_appearance(self, mode):
        config_manager.set("appearance_mode", mode)
        safe_set_theme(mode)

    def save_settings(self):
        config_manager.set(self.llm_url[1], self.llm_url[0].get())
        config_manager.set(self.llm_key[1], self.llm_key[0].get())
        config_manager.set(self.llm_model[1], self.llm_model[0].get())
        print("Settings saved to config.json")

class MetadataForm(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.fields = {}
        row = 0
        for label_text in ["Series", "Number", "Volume", "Year", "Publisher", "Genre"]:
            lbl = ctk.CTkLabel(self, text=label_text, anchor="w")
            lbl.grid(row=row, column=0, padx=10, pady=5, sticky="w")
            entry = ctk.CTkEntry(self)
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.fields[label_text] = entry
            row += 1
        self.summary_text = ctk.CTkTextbox(self, height=120)
        self.summary_text.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        row += 1
        self.save_button = ctk.CTkButton(self, text="Inject Metadata", command=self.on_save)
        self.save_button.grid(row=row, column=0, columnspan=2, padx=10, pady=20)

    def load_comic(self, comic: ComicInfo):
        self.fields["Series"].delete(0, "end")
        self.fields["Series"].insert(0, comic.Series)
        self.fields["Number"].delete(0, "end")
        self.fields["Number"].insert(0, comic.Number)
        self.fields["Volume"].delete(0, "end")
        self.fields["Volume"].insert(0, str(comic.Volume) if comic.Volume != -1 else "")
        self.fields["Year"].delete(0, "end")
        self.fields["Year"].insert(0, str(comic.Year) if comic.Year != -1 else "")
        self.fields["Publisher"].delete(0, "end")
        self.fields["Publisher"].insert(0, comic.Publisher)
        self.fields["Genre"].delete(0, "end")
        self.fields["Genre"].insert(0, comic.Genre)
        self.summary_text.delete("0.0", "end")
        self.summary_text.insert("0.0", comic.Summary)

    def on_save(self):
        if hasattr(self.master.master.master, 'save_current_comic'):
             self.master.master.master.save_current_comic()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ComicInfoXmlGenerator")
        self.geometry(f"{1100}x750")
        self.current_directory = None
        self.found_files = []
        self.selected_paths = set() # Store multiple selected paths
        self.file_buttons = {} # path -> button widget
        self.selected_comic = None # Primary comic for editor

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.tabview.add("Editor")
        self.tabview.add("Settings")

        self._setup_editor_tab()
        self._setup_settings_tab()

    def _setup_editor_tab(self):
        tab = self.tabview.tab("Editor")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)
        tab.grid_rowconfigure(1, weight=1)

        # Top tools
        top_frame = ctk.CTkFrame(tab)
        top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        ctk.CTkButton(top_frame, text="Scan Directory", command=self.browse_directory, width=120).pack(side="left", padx=5)
        
        ctk.CTkButton(top_frame, text="Select All", command=self.select_all, width=80, fg_color="gray", hover_color="dim gray").pack(side="left", padx=5)
        ctk.CTkButton(top_frame, text="Clear", command=self.clear_selection, width=60, fg_color="gray", hover_color="dim gray").pack(side="left", padx=5)

        ctk.CTkLabel(top_frame, text="|").pack(side="left", padx=5)
        
        self.scraper_menu = ctk.CTkOptionMenu(top_frame, values=["Regex", "OldSchool", "LLM"], width=100)
        self.scraper_menu.pack(side="left", padx=5)
        self.scraper_menu.set(config_manager.get("default_scraper"))
        
        self.mode_var = ctk.StringVar(value="Overwrite")
        self.mode_switch = ctk.CTkSegmentedButton(top_frame, values=["Overwrite", "Fill Gaps"], variable=self.mode_var)
        self.mode_switch.pack(side="left", padx=10)

        self.apply_button = ctk.CTkButton(top_frame, text="Apply Scraper", command=self.apply_scraper, fg_color="green", hover_color="darkgreen")
        self.apply_button.pack(side="left", padx=10)
        self.apply_button.configure(state="disabled") # Disabled until a file is selected

        # Left List
        self.file_list_container = ctk.CTkScrollableFrame(tab)
        self.file_list_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Right Editor
        self.metadata_form = MetadataForm(tab)
        self.metadata_form.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Bottom Log and Status
        self.log_textbox = ctk.CTkTextbox(tab, height=100)
        self.log_textbox.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")

        # Status and Progress Area
        self.status_frame = ctk.CTkFrame(tab, height=30, fg_color="transparent")
        self.status_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="ew")
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready", font=ctk.CTkFont(size=12))
        self.status_label.pack(side="left", padx=5)
        
        self.progress_bar = ctk.CTkProgressBar(self.status_frame, width=200)
        self.progress_bar.pack(side="right", padx=10)
        self.progress_bar.set(0)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.pack_forget() # Hide by default

    def set_busy(self, busy: bool, message: str = "Processing..."):
        if busy:
            self.status_label.configure(text=message)
            self.progress_bar.pack(side="right", padx=10)
            self.progress_bar.start()
        else:
            self.status_label.configure(text="Ready")
            self.progress_bar.stop()
            self.progress_bar.pack_forget()

    def _setup_settings_tab(self):
        tab = self.tabview.tab("Settings")
        tab.grid_columnconfigure(0, weight=1)
        self.settings_form = SettingsForm(tab)
        self.settings_form.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def log(self, message: str):
        self.log_textbox.insert("end", f"{message}\n")
        self.log_textbox.see("end")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.current_directory = directory
            self.log(f"Selected: {directory}")
            self.scan()

    def scan(self):
        if not self.current_directory: return
        self.log("Scanning...")
        self.found_files = scan_archives(self.current_directory)
        self.log(f"Found {len(self.found_files)} archives.")
        
        # Reset selection state
        self.selected_paths.clear()
        self.file_buttons.clear()
        self.apply_button.configure(state="disabled")

        for widget in self.file_list_container.winfo_children(): widget.destroy()
        
        for f in self.found_files:
            rel_path = os.path.relpath(f, self.current_directory)
            btn = ctk.CTkButton(
                self.file_list_container, 
                text=rel_path, 
                anchor="w", 
                fg_color="transparent", 
                text_color=("gray10", "gray90"),
                command=lambda p=f: self.toggle_selection(p)
            )
            btn.pack(fill="x", padx=5, pady=2)
            self.file_buttons[f] = btn

    def toggle_selection(self, file_path: str):
        if file_path in self.selected_paths:
            self.selected_paths.remove(file_path)
        else:
            self.selected_paths.add(file_path)
            # Load the most recently selected item into editor
            self.on_file_load(file_path)
        
        self._refresh_file_list_visuals()
        
        # Update Apply Button state
        if self.selected_paths:
            self.apply_button.configure(state="normal", text=f"Apply Scraper ({len(self.selected_paths)})")
        else:
            self.apply_button.configure(state="disabled", text="Apply Scraper")

    def _refresh_file_list_visuals(self):
        for path, btn in self.file_buttons.items():
            if path in self.selected_paths:
                btn.configure(fg_color=("#3B8ED0", "#1f538d"), text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color=("gray10", "gray90"))

    def select_all(self):
        if not self.found_files: return
        self.selected_paths = set(self.found_files)
        self._refresh_file_list_visuals()
        self.apply_button.configure(state="normal", text=f"Apply Scraper ({len(self.selected_paths)})")

    def clear_selection(self):
        self.selected_paths.clear()
        self.selected_comic = None
        self._refresh_file_list_visuals()
        self.apply_button.configure(state="disabled", text="Apply Scraper")
        # Could also clear the form here if desired

    def on_file_load(self, file_path: str):
        self.log(f"Selected: {os.path.basename(file_path)}")
        self.selected_comic = ComicInfo(path=file_path)
        self.metadata_form.load_comic(self.selected_comic)

    def _merge_metadata(self, target: ComicInfo, source: ComicInfo, mode: str):
        """Merge source (scraper result) into target (current) based on mode."""
        fields = ["Series", "Number", "Volume", "Year", "Publisher", "Genre", "Summary"]
        for field in fields:
            new_val = getattr(source, field)
            curr_val = getattr(target, field)
            
            should_update = False
            if mode == "Overwrite":
                should_update = True
            elif mode == "Fill Gaps":
                # Check if field is 'empty'
                if isinstance(curr_val, str):
                    if not curr_val.strip(): should_update = True
                elif isinstance(curr_val, int):
                    if curr_val == -1: should_update = True
            
            if should_update and new_val not in [None, "", -1]:
                setattr(target, field, new_val)

    def apply_scraper(self):
        if not self.selected_comic: return
        strategy = self.scraper_menu.get().lower()

        self.set_busy(True, f"Running {strategy} scraper...")
        self.log(f"Applying {strategy} scraper (background)...")

        # Run in background thread
        thread = threading.Thread(target=self._async_apply_scraper, args=(strategy,))
        thread.daemon = True
        thread.start()

    def _async_apply_scraper(self, strategy: str):
        try:
            if strategy == "oldschool": 
                scraper = OldSchoolFilenameScraper()
            elif strategy == "llm":
                api_key = config_manager.get("llm_api_key")
                if not api_key:
                    self.after(0, lambda: self.log("Error: LLM API Key is missing!"))
                    self.after(0, lambda: self.set_busy(False))
                    return
                scraper = LlmFilenameScraper(
                    api_key=api_key,
                    base_url=config_manager.get("llm_base_url"),
                    model=config_manager.get("llm_model")
                )
            else: 
                scraper = RegexFilenameScraper()

            scraper.search(self.selected_comic)

            # Update UI on main thread
            self.after(0, self._on_scraper_complete)
        except Exception as e:
            self.after(0, lambda err=e: self.log(f"Scraper Error: {err}"))
            self.after(0, lambda: self.set_busy(False))

    def _on_scraper_complete(self):
        self.metadata_form.load_comic(self.selected_comic)
        self.set_busy(False)
        self.log("Scraper finished.")


    def save_current_comic(self):
        if not self.selected_comic: return
        f = self.metadata_form.fields
        self.selected_comic.Series = f["Series"].get()
        self.selected_comic.Number = f["Number"].get()
        vol = f["Volume"].get()
        self.selected_comic.Volume = int(vol) if vol.isdigit() else -1
        year = f["Year"].get()
        self.selected_comic.Year = int(year) if year.isdigit() else -1
        self.selected_comic.Publisher = f["Publisher"].get()
        self.selected_comic.Genre = f["Genre"].get()
        self.selected_comic.Summary = self.metadata_form.summary_text.get("0.0", "end").strip()
        
        try:
            inject_comic_info_xml(self.selected_comic.path, self.selected_comic)
            self.log(f"Success: {os.path.basename(self.selected_comic.path)}")
        except Exception as e:
            self.log(f"Error: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
