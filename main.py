import customtkinter as ctk
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class RedMoneky(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Red.Monkey")
        self.geometry("500x450")
        self.resizable(False, False)
        self.iconbitmap("Main.ico")

        
        self.ImgP = ctk.CTkImage(Image.open("Main.ico"), size=(100, 100))
        self.ImgLb = ctk.CTkLabel(self, image=self.ImgP, text="")
        self.ImgLb.place(relx=0.2, rely=0.23, anchor="center")
    
        
        self.DnsS = ["ٍElectro","Radar","Google"]
        self.AdpS = ["All Adaptors"] + ["Wi-Fi","Ethernet"]
        self.AdpComboBoxLabel = ctk.CTkLabel(self, text="Network Adaptor")
        self.AdpComboBoxLabel.place(relx=0.499, rely=0.05, anchor="center",)
        self.AdpComboBox = ctk.CTkOptionMenu(self, values=self.AdpS,dropdown_text_color="#ffffff",dropdown_fg_color="#C83833",dropdown_font=ctk.CTkFont("Arial",14,"bold"),fg_color="#C83833",button_color="#E56A50",button_hover_color="#342523",dropdown_hover_color="#342523")
        self.AdpComboBox.set(self.AdpS[0])
        self.AdpComboBox.place(relx=0.55, rely=0.1, anchor="center")



        self.DnsComboBoxLabel = ctk.CTkLabel(self, text="Dns Server")
        self.DnsComboBoxLabel.place(relx=0.79, rely=0.05, anchor="center")
        self.DnsComboBox = ctk.CTkOptionMenu(self, values=self.DnsS,dropdown_text_color="#ffffff",dropdown_fg_color="#C83833",dropdown_font=ctk.CTkFont("Arial",14,"bold"),fg_color="#C83833",button_color="#E56A50",button_hover_color="#342523",dropdown_hover_color="#342523")
        self.DnsComboBox.set("Radar")
        self.DnsComboBox.place(relx=0.85, rely=0.1, anchor="center")

        self.Dns1Label = ctk.CTkLabel(self, text="Primary Dns")
        self.Dns1Label.place(relx=0.79, rely=0.2, anchor="center")
        self.Dns1In = ctk.CTkEntry(self, placeholder_text="Enter Primary DNS",fg_color="#C83833",border_color="#FCE6DE",border_width=1,text_color="#FCE6DE",placeholder_text_color="#FFFFFF")
        self.Dns1In.place(relx=0.85, rely=0.25, anchor="center")

        self.Dns2Lb = ctk.CTkLabel(self, text="Alternative Dns")
        self.Dns2Lb.place(relx=0.808, rely=0.35, anchor="center")
        self.Dns2In = ctk.CTkEntry(self, placeholder_text="Enter Alternative DNS",fg_color="#C83833",border_color="#FCE6DE",border_width=1,text_color="#FCE6DE",placeholder_text_color="#FFFFFF")
        self.Dns2In.place(relx=0.85, rely=0.4, anchor="center")

        self.SetBt = ctk.CTkButton(self, text="Set Dns",border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.SetBt.place(relx=0.7, rely=0.55, anchor="center")
        self.ResetBt = ctk.CTkButton(self, text="Reset Dns",border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.ResetBt.place(relx=0.55, rely=0.25, anchor="center")
        self.FlushBt = ctk.CTkButton(self, text="Flush Dns",border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.FlushBt.place(relx=0.55, rely=0.4, anchor="center")

        
        

if __name__ == "__main__":

    app = RedMoneky()
    app.mainloop()