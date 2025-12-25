import customtkinter as ctk
from analyzer import warden_scan

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WardenApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Warden-X AI v1.0")
        self.geometry("700x600")

        # Негізгі фрейм
        self.main_frame = ctk.CTkFrame(self, corner_radius=20)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Логотип пен Тақырып
        self.label = ctk.CTkLabel(self.main_frame, text="🛡️ WARDEN-X AI", font=("Roboto", 28, "bold"))
        self.label.pack(pady=(20, 10))

        self.sub_label = ctk.CTkLabel(self.main_frame, text="Фишингке қарсы ИИ детекторы", font=("Roboto", 14))
        self.sub_label.pack(pady=(0, 20))

        # Мәтін енгізу
        self.textbox = ctk.CTkTextbox(self.main_frame, width=600, height=200, corner_radius=10, font=("Roboto", 14))
        self.textbox.pack(pady=10, padx=40)
        self.textbox.insert("0.0", "Тексеретін хабарламаны осында көшіріп сал...")

        # Батырма
        self.button = ctk.CTkButton(self.main_frame, text="АНАЛИЗ ЖАСАУ", height=45, font=("Roboto", 16, "bold"), command=self.analyze)
        self.button.pack(pady=20)

        # Нәтижелер блогы
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.result_frame.pack(pady=10, fill="x", padx=40)

        self.status_label = ctk.CTkLabel(self.result_frame, text="Статус: Күтуде...", font=("Roboto", 18, "bold"))
        self.status_label.pack()

        self.score_label = ctk.CTkLabel(self.result_frame, text="Қауіп деңгейі: 0%", font=("Roboto", 14))
        self.score_label.pack()

        self.alerts_label = ctk.CTkLabel(self.result_frame, text="", font=("Roboto", 12), justify="left")
        self.alerts_label.pack(pady=10)

    def analyze(self):
        text = self.textbox.get("1.0", "end-1c")
        res = warden_scan(text)

        # Статусқа қарай түсті өзгерту
        color = "white"
        if "ҚАУІПТІ" in res['status']: color = "#FF4B4B" # Қызыл
        elif "КҮМӘНДІ" in res['status']: color = "#FFB84D" # Сары
        else: color = "#4BB543" # Жасыл

        self.status_label.configure(text=f"Статус: {res['status']}", text_color=color)
        self.score_label.configure(text=f"Қауіп деңгейі: {res['score']}%")
        
        # Қауіптің себептерін шығару
        alerts_text = "\n".join([f"• {a}" for a in res['alerts']])
        self.alerts_label.configure(text=f"Анықталған факторлар:\n{alerts_text}")

if __name__ == "__main__":
    app = WardenApp()
    app.mainloop()