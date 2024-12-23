import customtkinter as ctk


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class RedMoneky(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Red.Monkey")
        self.geometry("500x450")
        self.resizable(False, False)
        self.iconbitmap("Main.ico")

        
        

if __name__ == "__main__":

    app = RedMoneky()
    app.mainloop()