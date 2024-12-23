import json,pyuac,dns.resolver
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
        self.DnsS = [i for i in self.DnsSJsonData.keys()] + ['Custom']
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
        self.ResetBt = ctk.CTkButton(self, text="Reset Dns", command=self.ResetDNSBut,border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.ResetBt.place(relx=0.55, rely=0.25, anchor="center")
        self.FlushBt = ctk.CTkButton(self, text="Flush Dns", command=self.SetDNSBut,border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.FlushBt.place(relx=0.55, rely=0.4, anchor="center")


        self.SetUp()


    def SetUp(self):
        CurrentDns = self.CurrentDns()
        self.DisEnEntrys(False)
        self.Dns1In.delete(0,ctk.END)
        self.Dns1In.insert(0,CurrentDns[0])
        self.Dns2In.delete(0,ctk.END)
        self.Dns2In.insert(0,CurrentDns[1])
        self.DisEnEntrys(True)
        for Name,DnsS in self.DnsSJsonData.items():
            print(Name,DnsS,str(CurrentDns[0]) == DnsS['Primary'],str(CurrentDns[1]) == DnsS['Alternative'])
            if str(CurrentDns[0]) == DnsS['Primary'] and str(CurrentDns[1]) == DnsS['Alternative']:
                self.DnsComboBox.set(Name)
                break
            else:
                self.DnsComboBox.set('Custom')



    def DisEnEntrys(self,Disable):
        if Disable:
            self.Dns1In.configure(state = "disabled")
            self.Dns2In.configure(state = "disabled")
        else:
            self.Dns1In.configure(state = "normal")
            self.Dns2In.configure(state = "normal")


    def ComboDnsFunc(self,OptionSelected):
        if OptionSelected != "Custom":
            self.DisEnEntrys(False)
            self.Dns1In.delete(0,ctk.END)
            self.Dns1In.insert(0,self.DnsSJsonData[OptionSelected]['Primary'])
            self.Dns2In.delete(0,ctk.END)
            self.Dns2In.insert(0,self.DnsSJsonData[OptionSelected]['Alternative'])
            self.DisEnEntrys(True)
        else :
            self.DisEnEntrys(False)
            self.Dns1In.delete(0,ctk.END)
            self.Dns2In.delete(0,ctk.END)


    def SetDNSBut(self):
        SelectedDns = self.DnsComboBox.get()
        PrimaryDns = self.Dns1In.get()
        AlternativeDns = self.Dns2In.get()
        Adaptor = [self.AdpComboBox.get()]  if self.AdpComboBox.get() != "All Adaptors" else [Adaptor for Adaptor in self.GetAdaptors()]
        if SelectedDns != "Custom":
            for Adp in Adaptor:
                self.SetDns(Adp,self.DnsSJsonData[SelectedDns]['Primary'],self.DnsSJsonData[SelectedDns]['Alternative'])
        else:
            
            PrimaryDns = self.Dns1In.get()
            AlternativeDns = self.Dns2In.get()
            for Adp in Adaptor:
                self.SetDns(Adp,PrimaryDns,AlternativeDns)


    def ResetDNSBut(self):
        Adaptor = [self.AdpComboBox.get()]  if self.AdpComboBox.get() != "All Adaptors" else [Adaptor for Adaptor in self.GetAdaptors()]
        for Adp in Adaptor:
            self.ResetDNS(Adp)





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

    def CurrentDns(self):
        DnsS = dns.resolver.Resolver()
        return DnsS.nameservers
            
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
    # Run As Adminnn ;D
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
    else:        
        app = RedMoneky()
        app.mainloop()