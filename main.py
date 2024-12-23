import json
from PIL import Image
import customtkinter as ctk
import psutil,subprocess

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
    
        self.DnsSJsonData = self.ReadConfig()
        self.DnsS = [i for i in self.DnsSJsonData.keys()]
        self.AdpS = ["All Adaptors"] + [adaptor for adaptor in self.GetAdaptors()]
        self.AdpComboBoxLabel = ctk.CTkLabel(self, text="Network Adaptor")
        self.AdpComboBoxLabel.place(relx=0.499, rely=0.05, anchor="center",)
        self.AdpComboBox = ctk.CTkOptionMenu(self, values=self.AdpS,dropdown_text_color="#ffffff",dropdown_fg_color="#C83833",dropdown_font=ctk.CTkFont("Arial",14,"bold"),command=self.ComboDnsFunc,fg_color="#C83833",button_color="#E56A50",button_hover_color="#342523",dropdown_hover_color="#342523")
        self.AdpComboBox.set(self.AdpS[0])
        self.AdpComboBox.place(relx=0.55, rely=0.1, anchor="center")



        self.DnsComboBoxLabel = ctk.CTkLabel(self, text="Dns Server")
        self.DnsComboBoxLabel.place(relx=0.79, rely=0.05, anchor="center")
        self.DnsComboBox = ctk.CTkOptionMenu(self, values=self.DnsS,dropdown_text_color="#ffffff",dropdown_fg_color="#C83833",dropdown_font=ctk.CTkFont("Arial",14,"bold"),command=self.ComboDnsFunc,fg_color="#C83833",button_color="#E56A50",button_hover_color="#342523",dropdown_hover_color="#342523")
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

        self.SetBt = ctk.CTkButton(self, text="Set Dns", command=self.SetDNSBut,border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.SetBt.place(relx=0.7, rely=0.55, anchor="center")
        self.ResetBt = ctk.CTkButton(self, text="Reset Dns", command=self.SetDNSBut,border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.ResetBt.place(relx=0.55, rely=0.25, anchor="center")
        self.FlushBt = ctk.CTkButton(self, text="Flush Dns", command=self.SetDNSBut,border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.FlushBt.place(relx=0.55, rely=0.4, anchor="center")



    def ComboDnsFunc(self,OptionSelected):
        if OptionSelected != "Custom":
            self.Dns1In.delete(0,ctk.END)
            self.Dns1In.insert(0,self.DnsSJsonData[OptionSelected]['Primary'])
            self.Dns2In.delete(0,ctk.END)
            self.Dns2In.insert(0,self.DnsSJsonData[OptionSelected]['Alternative'])


    def SetDNSBut(self):
        SelectedDns = self.DnsComboBox.get()
        PrimaryDns = self.Dns1In.get()
        AlternativeDns = self.Dns2In.get()
        Adaptor = self.AdpComboBox.get()
        if SelectedDns != "Custom":
            self.SetDns(Adaptor,self.DnsSJsonData[SelectedDns]['Primary'],self.DnsSJsonData[SelectedDns]['Alternative'])
        else:
            PrimaryDns = self.Dns1In.get()
            AlternativeDns = self.Dns2In.get()
            self.SetDns(Adaptor,PrimaryDns,AlternativeDns)




    def GetAdaptors(self):
        try:
            Adaptors = psutil.net_if_addrs()
            ActiveAdaptors = []
            for Ada in Adaptors.keys():
                if not (Ada.lower()).startswith("local") and not (Ada.lower()).startswith("vmware") and not (Ada.lower()).startswith("loopback") and not (Ada.lower()).startswith("bluetooth"):
                    ActiveAdaptors.append(Ada)
            return ActiveAdaptors if ActiveAdaptors else "No Adaptor Found ! :("
        except Exception as e:
            return f"Error: {e}"
    def ResetDNS(self,AdpName):

        try:
            Cmd = f'netsh interface ip set dns name="{AdpName}" source=dhcp'
            Res = subprocess.run(Cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            print(Res.stdout)
            print()
            if Res.stdout.replace("\n","").replace(" ","") != "":
                return False
            return True
        except Exception as e:
            return False

    def ReadConfig(self):
        with open("DnsS.json", 'r') as file:
            return json.load(file)
    

    def WriteConfig(self):
        with open("DnsS.json", 'w') as file:
            return json.dump(self.DnsSJsonData,file,indent=4)

            
    def SetDns(self, AdpName, PrimDns, AltDns=None):
        try:
            Cmd = f'netsh interface ip set dns name="{AdpName}" source=static addr={PrimDns} register=PRIMARY'
            Res = subprocess.run(Cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            
            if Res.stdout.replace("\n","").replace(" ","") != "":
                return False

            if AltDns:
                Cmd = f'netsh interface ip add dns name="{AdpName}" addr={AltDns} index=2'
                Res = subprocess.run(Cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
                
                if Res.stdout.replace("\n","").replace(" ","") != "":
                    return False
            return True
        except Exception as e:
            return False

        
        

if __name__ == "__main__":

    app = RedMoneky()
    app.mainloop()