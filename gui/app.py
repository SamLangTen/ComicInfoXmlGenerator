import customtkinter as ctk
import os

try:
    ctk.set_appearance_mode("Dark")
except Exception:
    pass

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ComicInfoXmlGenerator")
        self.geometry(f"{1100}x580")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CIXG", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.scan_button = ctk.CTkButton(self.sidebar_frame, text="Scan Directory", command=self.sidebar_button_event)
        self.scan_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # Create main entry (file list on left, details on right)
        self.file_list_frame = ctk.CTkFrame(self)
        self.file_list_frame.grid(row=0, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.file_list_label = ctk.CTkLabel(self.file_list_frame, text="Comic Archives", font=ctk.CTkFont(size=16, weight="bold"))
        self.file_list_label.pack(padx=20, pady=10)

        self.details_frame = ctk.CTkFrame(self, width=250)
        self.details_frame.grid(row=0, column=2, rowspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.details_label = ctk.CTkLabel(self.details_frame, text="Metadata Details", font=ctk.CTkFont(size=16, weight="bold"))
        self.details_label.pack(padx=20, pady=10)

        # Create log/output area at bottom
        self.log_textbox = ctk.CTkTextbox(self, height=100)
        self.log_textbox.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Set default values
        self.appearance_mode_optionemenu.set("Dark")

    def sidebar_button_event(self):
        print("sidebar_button click")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = App()
    app.mainloop()
