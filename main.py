import json,dns.resolver,winsound,pyuac,ipaddress,psutil,subprocess
from CustomTkinterMessagebox import CTkMessagebox
from PIL import Image
import customtkinter as Ctk

Ctk.set_appearance_mode("Dark")
Ctk.set_default_color_theme("dark-blue")

class RedMoneky(Ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Red.Monkey")

        # Window Size <width>x<height> -> Split With x
        WindowSize = "500x450"

        #Set Window In Center Of Screen -> Size = WindowSize
        self.geometry(f"{int(WindowSize.split("x")[0])}x{int(WindowSize.split("x")[1])}+{(self.winfo_screenwidth() // 2) - (int(WindowSize.split("x")[0]) // 2)}+{(self.winfo_screenheight() // 2) - (int(WindowSize.split("x")[1]) // 2)}")

        self.resizable(False, False)
        self.iconbitmap("Main.ico")
        self.ImgP = Ctk.CTkImage(Image.open("Main.ico"), size=(100, 100))
        self.ImgLb = Ctk.CTkLabel(self, image=self.ImgP, text="")
        self.ImgLb.place(relx=0.2, rely=0.23, anchor="center")
    
        self.DnsSJsonData = self.ReadConfig()
        self.DnsS = [i for i in self.DnsSJsonData.keys()] + ['Custom']
        self.AdpS = ["All Adaptors"] + [adaptor for adaptor in self.GetAdaptors()]
        self.AdpComboBoxLabel = Ctk.CTkLabel(self, text="Network Adaptor")
        self.AdpComboBoxLabel.place(relx=0.499, rely=0.05, anchor="center",)
        self.AdpComboBox = Ctk.CTkOptionMenu(self, values=self.AdpS,dropdown_text_color="#ffffff",dropdown_fg_color="#C83833",dropdown_font=Ctk.CTkFont("Arial",14,"bold"),fg_color="#C83833",button_color="#E56A50",button_hover_color="#342523",dropdown_hover_color="#342523")
        self.AdpComboBox.set(self.AdpS[0])
        self.AdpComboBox.place(relx=0.55, rely=0.1, anchor="center")

        

        self.DnsComboBoxLabel = Ctk.CTkLabel(self, text="Dns Server")
        self.DnsComboBoxLabel.place(relx=0.79, rely=0.05, anchor="center")
        self.DnsComboBox = Ctk.CTkOptionMenu(self, values=self.DnsS,dropdown_text_color="#ffffff",dropdown_fg_color="#C83833",dropdown_font=Ctk.CTkFont("Arial",14,"bold"),command=self.ComboDnsFunc,fg_color="#C83833",button_color="#E56A50",button_hover_color="#342523",dropdown_hover_color="#342523")
        self.DnsComboBox.set("Radar")
        self.DnsComboBox.place(relx=0.85, rely=0.1, anchor="center")

        self.Dns1Label = Ctk.CTkLabel(self, text="Primary Dns")
        self.Dns1Label.place(relx=0.79, rely=0.2, anchor="center")
        self.Dns1In = Ctk.CTkEntry(self, placeholder_text="Enter Primary DNS",fg_color="#C83833",border_color="#FCE6DE",border_width=1,text_color="#FCE6DE",placeholder_text_color="#FFFFFF")
        self.Dns1In.place(relx=0.85, rely=0.25, anchor="center")

        self.Dns2Lb = Ctk.CTkLabel(self, text="Alternative Dns")
        self.Dns2Lb.place(relx=0.808, rely=0.35, anchor="center")
        self.Dns2In = Ctk.CTkEntry(self, placeholder_text="Enter Alternative DNS",fg_color="#C83833",border_color="#FCE6DE",border_width=1,text_color="#FCE6DE",placeholder_text_color="#FFFFFF")
        self.Dns2In.place(relx=0.85, rely=0.4, anchor="center")

        self.SetBt = Ctk.CTkButton(self, text="Set Dns", command=self.SetDNSBut,border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.SetBt.place(relx=0.7, rely=0.55, anchor="center")
        self.ResetBt = Ctk.CTkButton(self, text="Reset Dns", command=self.ResetDNSBut,border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.ResetBt.place(relx=0.55, rely=0.25, anchor="center")
        self.FlushBt = Ctk.CTkButton(self, text="Flush Dns", command=self.FlushDnsBut,border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        self.FlushBt.place(relx=0.55, rely=0.4, anchor="center")


        self.SetUp()


    def SetUp(self):
        CurrentDns = self.CurrentDns()
        self.DisEnEntrys(False)
        self.Dns1In.delete(0,Ctk.END)
        self.Dns1In.insert(0,CurrentDns[0])
        self.Dns2In.delete(0,Ctk.END)
        self.Dns2In.insert(0,CurrentDns[1])
        self.DisEnEntrys(True)
        for Name,DnsS in self.DnsSJsonData.items():
            if str(CurrentDns[0]) == DnsS['Primary'] and str(CurrentDns[1]) == DnsS['Alternative']:
                self.DnsComboBox.set(Name)
                self.DisEnEntrys(True)
                break
            else:
                self.DnsComboBox.set('Custom')
                self.DisEnEntrys(False)


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
            self.Dns1In.delete(0,Ctk.END)
            self.Dns1In.insert(0,self.DnsSJsonData[OptionSelected]['Primary'])
            self.Dns2In.delete(0,Ctk.END)
            self.Dns2In.insert(0,self.DnsSJsonData[OptionSelected]['Alternative'])
            self.DisEnEntrys(True)
        else :
            self.DisEnEntrys(False)
            self.Dns1In.delete(0,Ctk.END)
            self.Dns2In.delete(0,Ctk.END)


    def SetDNSBut(self):
        SelectedDns = self.DnsComboBox.get()
        PrimaryDns = self.Dns1In.get()
        AlternativeDns = self.Dns2In.get()
        Adaptor = [self.AdpComboBox.get()]  if self.AdpComboBox.get() != "All Adaptors" else [Adaptor for Adaptor in self.GetAdaptors()]
        if SelectedDns != "Custom":
            WhichSeted = {}
            for Adp in Adaptor:
                if self.SetDns(Adp,self.DnsSJsonData[SelectedDns]['Primary'],self.DnsSJsonData[SelectedDns]['Alternative']):
                    WhichSeted[Adp] = True
                else:
                    WhichSeted[Adp] = False
            OkAdpS = [i for i in WhichSeted.keys() if WhichSeted[i] == True]
            BadAdpS = [i for i in WhichSeted.keys() if WhichSeted[i] == False]
            self.MsgBox("Set Dns Report", 
                (f"Successful Set : {''.join([f' {i}' for i in OkAdpS])}\n" if len(OkAdpS) > 0 else "") + 
                (f"Not Set : {''.join([f' {i}' for i in BadAdpS])}\n" if len(BadAdpS) > 0 else ""))
        else:
            WhichSeted = {}
            PrimaryDns = self.Dns1In.get()
            AlternativeDns = self.Dns2In.get()
            # Valid Check
            if self.CheckDns(PrimaryDns):
                if AlternativeDns and not self.CheckDns(AlternativeDns):
                    self.MsgBox("Invalid Custom Dns !",
                        "The Alternate Dns is not valid.")
                    return
            else:
                self.MsgBox("Invalid Custom Dns !",
                        "The Primary Dns is not valid.")
                return
            #-------------------------------------------------------------------------------------------------
            # Is A Saved Dns ?
            for Name,DnsS in self.DnsSJsonData.items():
                if str(PrimaryDns) == DnsS['Primary'] and str(AlternativeDns) == DnsS['Alternative']:
                    self.DnsComboBox.set(Name)
                    SelectedDns = Name
                    break
                else:
                    SelectedDns = 'Custom'
                    self.DisEnEntrys(False)
            #-------------------------------------------------------------------------------------------------
            # Save And NewName
            if SelectedDns == 'Custom' :
                if self.YesOrNo("New Dns !","Do You Want This DNS to be Saved?"):
                    IsName,Name = self.InputDialog("Dns Name","Type Valid Name !")
                    if IsName :
                        if not Name in [i for i in self.DnsSJsonData.keys()]:
                            self.DnsSJsonData[Name] = {}
                            self.DnsSJsonData[Name]["Primary"] = PrimaryDns
                            self.DnsSJsonData[Name]["Alternative"] = AlternativeDns
                            self.SaveConfig()
                            self.ReadConfig()
                            self.DnsS = [i for i in self.DnsSJsonData.keys()] + ['Custom']
                            self.DnsComboBox.configure(values=self.DnsS)
                        else:
                            self.MsgBox("Invalid Dns Name !",
                                "Try Again !")
                            return
            #-------------------------------------------------------------------------------------------------


            # Set
            for Adp in Adaptor:
                if self.SetDns(Adp,PrimaryDns,AlternativeDns):
                    WhichSeted[Adp] = True
                else:
                    WhichSeted[Adp] = False
            OkAdpS = [i for i in WhichSeted.keys() if WhichSeted[i] == True]
            BadAdpS = [i for i in WhichSeted.keys() if WhichSeted[i] == False]
            self.MsgBox("Set Dns Report", 
            (f"Successful Set : {''.join([f' {i}' for i in OkAdpS])}\n" if len(OkAdpS) > 0 else "") + 
            (f"Not Set : {''.join([f' {i}' for i in BadAdpS])}\n" if len(BadAdpS) > 0 else ""))
                        


    def ResetDNSBut(self):
        Adaptor = [self.AdpComboBox.get()]  if self.AdpComboBox.get() != "All Adaptors" else [Adaptor for Adaptor in self.GetAdaptors()]
        WhichSeted = {}
        for Adp in Adaptor:
            
            if self.ResetDNS(Adp):
                WhichSeted[Adp] = True
            else:
                WhichSeted[Adp] = False
        OkAdpS = [i for i in WhichSeted.keys() if WhichSeted[i] == True]
        BadAdpS = [i for i in WhichSeted.keys() if WhichSeted[i] == False]
        self.MsgBox("Reset Dns Report", 
        (f"Successful Reset : {''.join([f' {i}' for i in OkAdpS])}\n" if len(OkAdpS) > 0 else "") + 
        (f"Not Reset : {''.join([f' {i}' for i in BadAdpS])}\n" if len(BadAdpS) > 0 else ""))

    def FlushDnsBut(self):
        self.FlushDNS()
        winsound.PlaySound("C:\\Windows\\Media\\Windows Ding.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)



    #Master Set MsgBox Center OF Master Form And Screen Set Form In The Center Of Screen 
    def MsgBox(Master, Title: str, Text: str, Sound=True, ButtonText="OK", Size='200x150', Center = "Master" , TopWindow=True):
        MsgBox = Ctk.CTkToplevel(Master)
        MsgBox.geometry(Size)
        MsgBox.title(Title)
        MsgBox.resizable(False, False)
        MsgBox.attributes('-toolwindow', True, '-topmost', TopWindow)
        MsgBox.grab_set()
        def Close():
            MsgBox.destroy()
            return
        if Center == "Master":
            MsgBox.update_idletasks()
            X = Master.winfo_x() + (Master.winfo_width() - int(Size.split("x")[0])) // 2
            Y = Master.winfo_y() + (Master.winfo_height() - int(Size.split("x")[1])) // 2
            MsgBox.geometry(f"{Size}+{X}+{Y}")
        elif Center == "Screen":
            MsgBox.update_idletasks()
            MsgBox.geometry(f"+{(MsgBox.winfo_screenwidth()) // 2}+{(MsgBox.winfo_screenheight()) // 2}")

        TextLabel = Ctk.CTkLabel(MsgBox, text=Text)
        TextLabel.pack(pady=30)

        MsgFrame = Ctk.CTkFrame(MsgBox, height=1)
        MsgFrame.pack(side="bottom", fill="x")

        But = Ctk.CTkButton(MsgFrame, text=ButtonText, command=Close,border_color="#FCE6DE",border_width=1,fg_color="#C83833",hover_color="#342523",text_color="#ffffff",text_color_disabled="#B3A39D")
        But.pack(pady=15)
        
        if Sound:
            winsound.PlaySound("C:\\Windows\\Media\\Windows Notify System Generic.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    
    

    def YesOrNo(Master, Title: str, Text: str, Sound=True, ButtonText: list = ["Ok", "No"], Size='230x170', Center="Master", TopWindow=True):
        result = None
        MsgBox = Ctk.CTkToplevel(Master)
        MsgBox.geometry(Size)
        MsgBox.title(Title)
        MsgBox.resizable(False, False)
        MsgBox.attributes('-toolwindow', True, '-topmost', TopWindow)
        MsgBox.grab_set()

        def OkBut():
            nonlocal result
            result = True
            MsgBox.destroy()

        def NoBut():
            nonlocal result 
            result = False
            MsgBox.destroy()

        if Center == "Master":
            MsgBox.update_idletasks()
            X = Master.winfo_x() + (Master.winfo_width() - int(Size.split("x")[0])) // 2
            Y = Master.winfo_y() + (Master.winfo_height() - int(Size.split("x")[1])) // 2
            MsgBox.geometry(f"{Size}+{X}+{Y}")
        elif Center == "Screen":
            MsgBox.update_idletasks()
            MsgBox.geometry(f"+{(MsgBox.winfo_screenwidth()) // 2}+{(MsgBox.winfo_screenheight()) // 2}")

        TextLabel = Ctk.CTkLabel(MsgBox, text=Text)
        TextLabel.pack(pady=30)

        MsgFrame = Ctk.CTkFrame(MsgBox, height=1)
        MsgFrame.pack(side="bottom", fill="x")

        But1 = Ctk.CTkButton(MsgFrame, text=ButtonText[0], command=OkBut, border_color="#FCE6DE", border_width=1, fg_color="#C83833", hover_color="#342523", text_color="#ffffff", text_color_disabled="#B3A39D")
        But1.pack(pady=3)
        But2 = Ctk.CTkButton(MsgFrame, text=ButtonText[1], command=NoBut, border_color="#FCE6DE", border_width=1, fg_color="#C83833", hover_color="#342523", text_color="#ffffff", text_color_disabled="#B3A39D")
        But2.pack(pady=3)

        if Sound:
            winsound.PlaySound("C:\\Windows\\Media\\Windows Notify System Generic.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

        MsgBox.wait_window(MsgBox)
        
        return result
    
    def InputDialog(Master, Title: str, Text: str, Sound=True, ButtonText: list = ["Ok", "Cancel"], Size='200x170', Center="Master", TopWindow=True):
        result = None
        TextOut = None

        MsgBox = Ctk.CTkToplevel(Master)
        MsgBox.geometry(Size)
        MsgBox.title(Title)
        MsgBox.resizable(False, False)
        MsgBox.attributes('-toolwindow', True, '-topmost', TopWindow)
        MsgBox.grab_set()

        def OkBut():
            nonlocal result, TextOut
            result = True
            TextOut = Entry.get()
            MsgBox.destroy()

        def NoBut():
            nonlocal result
            result = False
            MsgBox.destroy()

        if Center == "Master":
            MsgBox.update_idletasks()
            X = Master.winfo_x() + (Master.winfo_width() - int(Size.split("x")[0])) // 2
            Y = Master.winfo_y() + (Master.winfo_height() - int(Size.split("x")[1])) // 2
            MsgBox.geometry(f"{Size}+{X}+{Y}")
        elif Center == "Screen":
            MsgBox.update_idletasks()
            MsgBox.geometry(f"+{(MsgBox.winfo_screenwidth()) // 2}+{(MsgBox.winfo_screenheight()) // 2}")


        Entry = Ctk.CTkEntry(MsgBox,placeholder_text = Text, width = int((int(Size.split("x")[0]) * 70) / 100),fg_color="#C83833",border_color="#FCE6DE",border_width=1,text_color="#FCE6DE",placeholder_text_color="#FFFFFF")
        Entry.place(relx=0.50, rely=0.3, anchor="center")

        MsgFrame = Ctk.CTkFrame(MsgBox, height=1)
        MsgFrame.pack(side="bottom", fill="x")

        But1 = Ctk.CTkButton(MsgFrame, text=ButtonText[0], command=OkBut, border_color="#FCE6DE", border_width=1, fg_color="#C83833", hover_color="#342523", text_color="#ffffff", text_color_disabled="#B3A39D")
        But1.pack(pady=3)

        But2 = Ctk.CTkButton(MsgFrame, text=ButtonText[1], command=NoBut, border_color="#FCE6DE", border_width=1, fg_color="#C83833", hover_color="#342523", text_color="#ffffff", text_color_disabled="#B3A39D")
        But2.pack(pady=3)

        if Sound:
            winsound.PlaySound("C:\\Windows\\Media\\Windows Notify System Generic.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

        MsgBox.wait_window(MsgBox)

        return result, TextOut


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
            if Res.stdout.replace("\n","").replace(" ","") != "":
                return False
            return True
        except Exception as e:
            return False
    def FlushDNS(self):
        subprocess.run('ipconfig /flushdns', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        return True

    def ReadConfig(self):
        with open("DnsS.json", 'r') as file:
            return json.load(file)
    

    def SaveConfig(self):
        with open("DnsS.json", 'w') as file:
            return json.dump(self.DnsSJsonData,file,indent=4)

    def CurrentDns(self):
        DnsS = dns.resolver.Resolver()
        return DnsS.nameservers
            


    def CheckDns(self,DNS):
        try:
            ipaddress.ip_address(DNS)
            return True
        except:
            return False
        

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
        except Exception:
            return False







if __name__ == "__main__":
    # if not pyuac.isUserAdmin():
    #     pyuac.runAsAdmin()
    # else:        
    #     app = RedMoneky()
    #     app.mainloop()
    app = RedMoneky()
    app.mainloop()