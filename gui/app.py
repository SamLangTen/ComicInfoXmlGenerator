import customtkinter as ctk
import os
from src.scanner import scan_archives
from src.comic_info import ComicInfo
from src.archive import inject_comic_info_xml
from src.scraper.filename_scraper import RegexFilenameScraper, OldSchoolFilenameScraper, LlmFilenameScraper
from tkinter import filedialog

try:
    ctk.set_appearance_mode("Dark")
except Exception:
    pass

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

        # Summary as a text area
        self.summary_label = ctk.CTkLabel(self, text="Summary", anchor="w")
        self.summary_label.grid(row=row, column=0, padx=10, pady=5, sticky="nw")
        self.summary_text = ctk.CTkTextbox(self, height=80)
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
        if hasattr(self.master.master, 'save_current_comic'):
             self.master.master.save_current_comic()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ComicInfoXmlGenerator")
        self.geometry(f"{1100}x650")
        self.current_directory = None
        self.found_files = []
        self.selected_comic = None

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CIXG", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.scan_button = ctk.CTkButton(self.sidebar_frame, text="Scan Directory", command=self.browse_directory)
        self.scan_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.scraper_label = ctk.CTkLabel(self.sidebar_frame, text="Strategy:", anchor="w")
        self.scraper_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.scraper_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Regex", "OldSchool", "LLM"])
        self.scraper_menu.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.scraper_menu.set("Regex")

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # File List
        self.file_list_frame = ctk.CTkFrame(self)
        self.file_list_frame.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.file_list_label = ctk.CTkLabel(self.file_list_frame, text="Archives", font=ctk.CTkFont(size=16, weight="bold"))
        self.file_list_label.pack(padx=20, pady=10)
        self.file_list_container = ctk.CTkScrollableFrame(self.file_list_frame)
        self.file_list_container.pack(expand=True, fill="both", padx=10, pady=10)

        # Editor
        self.details_frame = ctk.CTkFrame(self)
        self.details_frame.grid(row=0, column=2, rowspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.details_label = ctk.CTkLabel(self.details_frame, text="Editor", font=ctk.CTkFont(size=16, weight="bold"))
        self.details_label.pack(padx=20, pady=10)
        
        self.metadata_form = MetadataForm(self.details_frame)
        self.metadata_form.pack(expand=True, fill="both", padx=10, pady=10)

        # Log
        self.log_textbox = ctk.CTkTextbox(self, height=100)
        self.log_textbox.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def log(self, message: str):
        self.log_textbox.insert("end", f"{message}\n")
        self.log_textbox.see("end")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.current_directory = directory
            self.log(f"Selected directory: {directory}")
            self.scan()

    def scan(self):
        if not self.current_directory: return
        self.log("Scanning...")
        self.found_files = scan_archives(self.current_directory)
        self.log(f"Found {len(self.found_files)} archives.")
        for widget in self.file_list_container.winfo_children(): widget.destroy()
        for f in self.found_files:
            rel_path = os.path.relpath(f, self.current_directory)
            btn = ctk.CTkButton(self.file_list_container, text=rel_path, anchor="w", fg_color="transparent", 
                                command=lambda p=f: self.on_file_select(p))
            btn.pack(fill="x", padx=5, pady=2)

    def on_file_select(self, file_path: str):
        self.log(f"Loading: {os.path.basename(file_path)}")
        self.selected_comic = ComicInfo(path=file_path)
        
        strategy = self.scraper_menu.get().lower()
        if strategy == "oldschool": scraper = OldSchoolFilenameScraper()
        elif strategy == "llm": scraper = LlmFilenameScraper()
        else: scraper = RegexFilenameScraper()
        
        scraper.search(self.selected_comic)
        self.metadata_form.load_comic(self.selected_comic)

    def save_current_comic(self):
        if not self.selected_comic: return
        
        self.selected_comic.Series = self.metadata_form.fields["Series"].get()
        self.selected_comic.Number = self.metadata_form.fields["Number"].get()
        vol = self.metadata_form.fields["Volume"].get()
        self.selected_comic.Volume = int(vol) if vol.isdigit() else -1
        year = self.metadata_form.fields["Year"].get()
        self.selected_comic.Year = int(year) if year.isdigit() else -1
        self.selected_comic.Publisher = self.metadata_form.fields["Publisher"].get()
        self.selected_comic.Genre = self.metadata_form.fields["Genre"].get()
        self.selected_comic.Summary = self.metadata_form.summary_text.get("0.0", "end").strip()
        
        try:
            inject_comic_info_xml(self.selected_comic.path, self.selected_comic)
            self.log(f"Success: Metadata injected into {os.path.basename(self.selected_comic.path)}")
        except Exception as e:
            self.log(f"Error: {e}")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
