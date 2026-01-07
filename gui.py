import customtkinter as ctk
import threading
import analyzer
from tkinter import messagebox

# 1. Дизайн стилін орнату
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WardenXGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Терезе баптаулары
        self.title("WARDEN-X | AI Intelligence")
        self.geometry("850x900")
        self.configure(fg_color="#0D0D0D") 

        # Негізгі орталық фрейм
        self.main_frame = ctk.CTkFrame(
            self, 
            fg_color="#161616", 
            corner_radius=20, 
            border_width=1, 
            border_color="#333333"
        )
        self.main_frame.pack(pady=30, padx=40, fill="both", expand=True)

        # Логотип және Тақырып
        self.title_label = ctk.CTkLabel(
            self.main_frame, text="WARDEN-X AI", 
            font=ctk.CTkFont(family="Inter", size=32, weight="bold"),
            text_color="#FFFFFF"
        )
        self.title_label.pack(pady=(25, 5))

        # Статус индикаторы
        self.status_dot = ctk.CTkLabel(
            self.main_frame, 
            text="● SYSTEM READY", 
            font=("Inter", 11, "bold"), 
            text_color="#22C55E"
        )
        self.status_dot.pack(pady=(0, 20))

        # Мәтін енгізу өрісі
        self.input_label = ctk.CTkLabel(self.main_frame, text="Тексерілетін мәтінді енгізіңіз:", font=("Inter", 12), text_color="#888888")
        self.input_label.pack(pady=(0, 5))

        # МӘТІН ЕНГІЗУ ТЕРЕЗЕСІ
        self.text_entry = ctk.CTkTextbox(
            self.main_frame, width=650, height=150, 
            fg_color="#0A0A0A", border_color="#262626", border_width=2,
            corner_radius=15, font=("Inter", 13), text_color="#E5E5E5"
        )
        self.text_entry.pack(pady=10, padx=40)
        
        # --- МӘЖБҮРЛІ ТҮРДЕ PASTE (ҚОЮ) ФУНКЦИЯСЫН ҚОСУ ---
        self.text_entry.bind("<Control-v>", self.force_paste)
        self.text_entry.bind("<Control-V>", self.force_paste)
        # ------------------------------------------------

        # БАТЫРМАЛАР БЛОГЫ
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=10)

        # SCAN Батырмасы
        self.analyze_button = ctk.CTkButton(
            self.button_frame, text="START SCAN", 
            command=self.start_ai_analysis,
            fg_color="#007AFF", hover_color="#005BB7",
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            corner_radius=12, height=50, width=250
        )
        self.analyze_button.grid(row=0, column=0, padx=10)

        # CLEAR Батырмасы
        self.clear_button = ctk.CTkButton(
            self.button_frame, text="CLEAR ALL", 
            command=self.clear_fields,
            fg_color="transparent", border_width=1, border_color="#444444",
            font=("Inter", 14), corner_radius=12, height=50, width=150
        )
        self.clear_button.grid(row=0, column=1, padx=10)

        # НӘТИЖЕ ШЫҒАТЫН АЙМАҚ
        self.result_label_title = ctk.CTkLabel(self.main_frame, text="ANALYSIS REPORT:", font=("Inter", 10, "bold"), text_color="#444444")
        self.result_label_title.pack(pady=(10, 0))

        self.ai_results_box = ctk.CTkTextbox(
            self.main_frame, 
            width=650, height=350, 
            fg_color="#111111", border_color="#1A1A1A", border_width=1,
            corner_radius=10, font=("Inter", 12), text_color="#B0B0B0",
            padx=20, pady=20
        )
        self.ai_results_box.pack(pady=(10, 20), padx=40)

    # Мәтінді мәжбүрлі түрде қою функциясы
    def force_paste(self, event=None):
        try:
            text = self.clipboard_get() # Жүйеден мәтінді алу
            self.text_entry.insert("insert", text) # Курсор тұрған жерге қою
            return "break" # Стандартты (істемейтін) функцияны тоқтату
        except:
            pass

    def clear_fields(self):
        self.text_entry.delete("1.0", "end")
        self.ai_results_box.delete("1.0", "end")
        self.status_dot.configure(text="● SYSTEM READY", text_color="#22C55E")
        self.analyze_button.configure(state="normal", text="START SCAN")

    def start_ai_analysis(self):
        text = self.text_entry.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Warden-X", "Please enter a message to scan!")
            return
        self.status_dot.configure(text="● ANALYZING...", text_color="#007AFF")
        self.analyze_button.configure(state="disabled", text="SCANNING...")
        self.ai_results_box.delete("1.0", "end")
        self.ai_results_box.insert("1.0", "System is communicating with AI model...")
        threading.Thread(target=self.run_analysis, args=(text,), daemon=True).start()

    def run_analysis(self, text):
        result = analyzer.check_phishing_with_ai(text)
        self.after(0, self.update_ui, result)

    def update_ui(self, result):
        self.ai_results_box.delete("1.0", "end")
        self.ai_results_box.insert("1.0", result)
        self.analyze_button.configure(state="normal", text="START SCAN")
        res_up = result.upper()
        if any(word in res_up for word in ["DANGER", "ҚАУІП", "PHISHING", "⚠️"]):
            self.status_dot.configure(text="● THREAT DETECTED / HIGH RISK", text_color="#EF4444")
        else:
            self.status_dot.configure(text="● SYSTEM SECURE / NO THREAT", text_color="#22C55E")

if __name__ == "__main__":
    app = WardenXGUI()
    app.mainloop()