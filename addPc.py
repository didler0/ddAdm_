import customtkinter
import tkinter
import re
from db import *
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


sql = SQL(server='DDLAPTOP\SQLEXPRESS', database='PC')
sql.connect()

def switch_event(switch_var):
        print("switch toggled, current value:", switch_var.get())

class addPC(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_widgets()
        
    
    def create_widgets(self):
        self.title("Add Computer")
        self.geometry("600x595")
        #self.minsize  (600, 555)
        #self.maxsize  (600, 555)

        self.frame = customtkinter.CTkScrollableFrame(self,height=520)
        self.grid_columnconfigure(0,weight=1)
        
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.tabview = customtkinter.CTkTabview(master=self.frame,height=515,width=550)
        self.tabview.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        self.tabview.add("Базовая информация")  
        self.tabview.add("Детальное описание") 
        self.tabview.add("Компоненты")

        
        
        #делаем описание
        labels_text = ["ip", "network_name", "place_of_installation","description"]
        labels_text_ru = ["IP Адрес", "Сетевое имя", "Место установки","Описание"]

        

        size = len(labels_text)
        self.tabview.tab("Базовая информация").grid_columnconfigure((1),weight=1)
        self.tabview.tab("Базовая информация").grid_rowconfigure((0,1,2,3),weight=1)
        self.tabview.tab("Детальное описание").grid_columnconfigure((1),weight=1)
        self.tabview.tab("Детальное описание").grid_rowconfigure((0,1,2,3,4,5,6),weight=1)
        self.tabview.tab("Компоненты").grid_columnconfigure((1),weight=1)
        self.tabview.tab("Компоненты").grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13),weight=1)
        self.widgetsDescription=[]
        
        for i, text in enumerate(labels_text_ru):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Базовая информация"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            
            if text=="IP Адрес":
                entry = customtkinter.CTkEntry(master=self.tabview.tab("Базовая информация"), placeholder_text="IP Адрес")
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsDescription.append(entry)
            elif text=="Сетевое имя":
                entry = customtkinter.CTkEntry(master=self.tabview.tab("Базовая информация"), placeholder_text="Сетевое имя")
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")       
                self.widgetsDescription.append(entry)         
            else:                
                textBox=customtkinter.CTkTextbox(master=self.tabview.tab("Базовая информация"),height=90)
                textBox.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsDescription.append(textBox)
                
        
        
        self.AddPcBasicButton = customtkinter.CTkButton(master=self, text="Добавить", command=lambda: self.AddPcAll())
        self.AddPcBasicButton.grid(row=2, column=0,columnspan=2, pady=5, padx=10, sticky="ew")
            

        
        
        
        #делаем делатьное описание
        labels_text_detail_ru=["Инв. №","Серийный №","MAC-адрес","Wake on LAN","Пароль VNC"]
        labels_text_detail = ["inventory_number","serial_number","mac_address","wake_on_lan","vnc_password"]
        
        self.widgetsDetailDescription=[]
        
        for i,text in enumerate(labels_text_detail_ru):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Детальное описание"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            if text=="Wake on LAN":
                switch_var = customtkinter.StringVar(value="off")
                switch=customtkinter.CTkSwitch(master=self.tabview.tab("Детальное описание"),text='',command=lambda:switch_event(switch_var),
                                 variable=switch_var,onvalue="on", offvalue="off")
                switch.grid(row=i, column=1, padx=10, pady=10, sticky="ew") 
                self.widgetsDetailDescription.append(switch) 
            elif text=="Детальное описание":
                textBox=customtkinter.CTkTextbox(master=self.tabview.tab("Детальное описание"),height=90)
                textBox.grid(row=i, column=1, padx=10, pady=10, sticky="ew")
                self.widgetsDetailDescription.append(textBox)
            else:                              
                entry = customtkinter.CTkEntry(master=self.tabview.tab("Детальное описание"), placeholder_text=text)
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")       
                self.widgetsDetailDescription.append(entry)   
                
        labels_text_components_ru=["Процессор","ОЗУ","Материнская плата","Видеокарта","Блок питания","Сетевая карта","Куллер","Корпус","HDD","SSD","Монитор","Клавиатура","Мышь","Аудио"]
        labels_text_components=["processor","ram","motherboard","graphicCard","psu","networkCard","cooler","chasis","hdd","ssd","monitor","keyboard","mouse","audio"]
        self.widgetsComponents=[]
        for i,text in enumerate(labels_text_components_ru):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Компоненты"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            entry = customtkinter.CTkEntry(master=self.tabview.tab("Компоненты"), placeholder_text=text)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")       
            self.widgetsComponents.append(entry)   
                
                
                   
    def AddPcAll(self):

        if self.AddPcBasic() and self.AddPcComponents() :
            self.AddPcDetail()
            CTkMessagebox(title="Успех", message="Компьютер успешно добавлен!\n Если была добавлена новая категория - перезапустите приложение",icon="check", option_1="Ok")
        else:
            print("ploho")
            
            
            
        
            
        
    def AddPcComponents(self):
        values_component=[]
        
        for widget in self.widgetsComponents:
            if isinstance(widget, customtkinter.CTkEntry):
                value = widget.get()
                widget.delete(0,customtkinter.END)
            else:
                value = None
            values_component.append(value) 
        
        sql.add_component(*values_component)
        return True

    def AddPcBasic(self):
        values_basic = []
        for widget in self.widgetsDescription:
            if isinstance(widget, customtkinter.CTkEntry):
                value = widget.get()  # Получение значения из CTkEntry
                widget.delete(0,customtkinter.END)
            elif isinstance(widget, customtkinter.CTkTextbox):
                value = widget.get("1.0", "end-1c")  # Получение значения из CTkTextbox
                widget.delete("1.0", "end-1c")
            else:
                value = None
            values_basic.append(value)   
        try:
            for text in values_basic:
                if(text!=''):
                    pass
                else:
                    raise IOError("Не заполнены поля в вкладке \"Базовая информация\" ")

            if self.check_ip_address(values_basic[0])==True:
                pass
            else:
                raise ValueError("Неправильный формат IP-адреса") 
            sql.add_basic_info(*values_basic)
            return True

        except ValueError as e:
            CTkMessagebox(title="Ошибка",message="Неправильный формат IP-адреса.", icon="cancel")
            return False
        except IOError as e:
            CTkMessagebox(title="Ошибка",message="Не заполнены поля в вкладке \"Базовая информация\" ", icon="cancel")
            return False






    def AddPcDetail(self):
        values_detail = []
        for i, widget in enumerate(self.widgetsDetailDescription):
            if isinstance(widget, customtkinter.CTkEntry):
                val = widget.get()
                values_detail.append(val)
                widget.delete(0,customtkinter.END)
            elif isinstance(widget, customtkinter.CTkSwitch):
                val = widget.get()
                values_detail.append(val)
            elif isinstance(widget, customtkinter.CTkTextbox):
                val = widget.get("1.0", "end-1c")
                values_detail.append(val)
                widget.delete("1.0", tkinter.END)
        try:
            for text in values_detail:
                if text != '':
                    pass
                else:
                    raise IOError("Не заполнены поля в вкладке \"Детальная информация\" ")
                
            bas=sql.get_last_basic_info_id()
            com=sql.get_last_components_id()
            print(bas)
            print(com)
            print(values_detail)
            sql.add_detail_info(bas,com,*values_detail)
            
            return True
             
                
            
        except IOError as e:
            CTkMessagebox(title="Ошибка", message="Не заполнены поля в вкладке \"Детальная информация\" ", icon="cancel")
            return False

        
        
        
    @staticmethod  
    def check_ip_address(ip_str):
        pattern = r'^(25[0-6]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-6]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-6]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-6]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        if re.match(pattern, ip_str):
            return True
        else:
            return False


            
            

            





#CTkMessagebox(title="Ошибка",
#                              message="Заполните все поля.", icon="cancel")
#CTkMessagebox(title="УРА", message="Компьютер успешно добавлен!",
#                          icon="check", option_1="Ok")
#CTkMessagebox(title="ОШИБКА", message=f"Не удалось добавит компьютер: {
#                          e}", icon="cancel")



if __name__ == "__main__":
    root = tkinter.Tk()
    app = addPC(root)
    root.mainloop()
    