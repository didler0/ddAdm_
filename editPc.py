import customtkinter
import tkinter
import re
from db import *
from CTkMessagebox import CTkMessagebox
from hPyT import *
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


sql = SQL(server='DDLAPTOP\SQLEXPRESS', database='PC')
sql.connect()
sql.create_tables_if_not_exist()

def switch_event(switch_var):
        print("switch toggled, current value:", switch_var.get())

class editPC(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_widgets()
        
    
    def create_widgets(self):
        self.title("Edit Computer")
        self.geometry("600x730")
        self.minsize  (600, 730)
        self.maxsize  (600, 730)
        maximize_minimize_button.hide(self)
        self.frame = customtkinter.CTkScrollableFrame(self,height=620)
        self.grid_columnconfigure(0,weight=1)
        self.frame.rowconfigure(0,weight=1)
        self.frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        
        
        self.combobox1= customtkinter.CTkComboBox(master=self.frame,values=[" "], state="readonly")
        self.combobox1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.FillComboBoxes()
        self.AddPcBasicButton = customtkinter.CTkButton(master=self.frame, text="Загрузить", command=lambda: self.LoadData())
        self.AddPcBasicButton.grid(row=0, column=1, pady=5, padx=10, sticky="ew")
        
        
        self.tabview = customtkinter.CTkTabview(master=self.frame,height=515,width=550)
        self.tabview.grid(row=2, column=0,columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.AddPcBasicButton = customtkinter.CTkButton(master=self, text="Сохранить",hover_color="green" ,command=lambda: self.SaveData())
        self.AddPcBasicButton.grid(row=3, column=0, pady=5, padx=10, sticky="ew")
        
        self.AddPcBasicButton = customtkinter.CTkButton(master=self, text="Удалить",hover_color="red", command=lambda: self.DellData())
        self.AddPcBasicButton.grid(row=4, column=0, pady=5, padx=10, sticky="ew")
        
        
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
        ###
        ###
        self.widgetsDescription=[]
        ###
        ###
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
                
        #делаем делатьное описание
        labels_text_detail_ru=["Инв. №","Серийный №","MAC-адрес","Wake on LAN","Пороль VNC"]
        labels_text_detail = ["detailed_information","inventory_number","serial_number","mac_address","wake_on_lan","vnc_password"]
        ###
        ###
        self.widgetsDetailDescription=[]
        ###
        ###
        for i,text in enumerate(labels_text_detail_ru):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Детальное описание"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            if text=="Wake on LAN":
                self.switch_var = customtkinter.StringVar(value="off")
                switch=customtkinter.CTkSwitch(master=self.tabview.tab("Детальное описание"),text='',command=lambda:switch_event(self.switch_var),
                                 variable=self.switch_var,onvalue="on", offvalue="off")
                switch.grid(row=i, column=1, padx=10, pady=10, sticky="ew") 
                self.widgetsDetailDescription.append(switch) 
            
            else:                              
                entry = customtkinter.CTkEntry(master=self.tabview.tab("Детальное описание"), placeholder_text=text)
                entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")       
                self.widgetsDetailDescription.append(entry)   
        #делаем компоненты
        labels_text_components_ru=["Процессор","ОЗУ","Материнская плата","Видеокарта","Блок питания","Сетевая карта","Куллер","Корпус","HDD","SSD","Монитор","Клавиатура","Мышь","Аудио"]
        labels_text_components=["processor","ram","motherboard","graphicCard","psu","networkCard","cooler","chasis","hdd","ssd","monitor","keyboard","mouse","audio"]
        ###
        ###
        self.widgetsComponents=[]
        ###
        ###
        for i,text in enumerate(labels_text_components_ru):
            label = customtkinter.CTkLabel(master=self.tabview.tab("Компоненты"), text=text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
            entry = customtkinter.CTkEntry(master=self.tabview.tab("Компоненты"), placeholder_text=text)
            entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")       
            self.widgetsComponents.append(entry)   
    
    
    def LoadData(self):
        self.ClearData()
        currVal = self.combobox1.get()
        parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
        if len(parts) > 0:
            numbers = parts[0].strip()  # Получить первую подстроку и удалить лишние пробелы
        else:
            pass
            
        data_basic=sql.get_basic_info_by_id(numbers)
        data_basic_filtred=[]
        data_basic_filtred = data_basic[1:5]
        self.data_detail=sql.get_detail_info_by_id(numbers)
        self.data_detail_filtred = self.data_detail[3:8]
        self.data_comp=sql.get_components_by_id(self.data_detail[2])
        data_comp_filyted=self.data_comp[1:15]
        # Установка данных в виджеты базовой информации
        for i, value in enumerate(data_basic_filtred):
                if isinstance(self.widgetsDescription[i], customtkinter.CTkEntry):
                    
                    self.widgetsDescription[i].insert(0, value)  # Установить значение в CTkEntry
                elif isinstance(self.widgetsDescription[i], customtkinter.CTkTextbox):
                    self.widgetsDescription[i].delete("1.0", tkinter.END)
                    self.widgetsDescription[i].insert(tkinter.END, value)  # Установить значение в CTkTextbox
                    
        # Установка данных в виджеты детальной информации
        for i, value in enumerate(self.data_detail_filtred):
                if isinstance(self.widgetsDetailDescription[i], customtkinter.CTkEntry):

                    self.widgetsDetailDescription[i].insert(0, value)  # Установить значение в CTkEntry
                elif isinstance(self.widgetsDetailDescription[i], customtkinter.CTkTextbox):

                    self.widgetsDetailDescription[i].insert(tkinter.END, value)  # Установить значение в CTkTextbox
                elif isinstance(self.widgetsDetailDescription[i], customtkinter.CTkSwitch):
                    self.switch_var.set(value)

        # Установка данных в виджеты компонентов
        for i, value in enumerate(data_comp_filyted):

            self.widgetsComponents[i].insert(0, value)  # Установить значение в CTkEntry
                    

        
        
        
        
        
        
    def SaveData(self):
        currVal = self.combobox1.get()
        parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
        if len(parts) > 0:
            numbers = parts[0].strip()  # Получить первую подстроку и удалить лишние пробелы
        #
        #   BASIC
        #
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
        sql.update_basic_info(numbers,*values_basic)
        #
        # COMPONENTS
        #
        values_component=[]
        for widget in self.widgetsComponents:
            if isinstance(widget, customtkinter.CTkEntry):
                value = widget.get()
                widget.delete(0,customtkinter.END)
            else:
                value = None
            values_component.append(value)
        sql.update_component_info(self.data_comp[0],*values_component)
        #
        #   Details
        #
        values_detail = []
        for i, widget in enumerate(self.widgetsDetailDescription):
            if isinstance(widget, customtkinter.CTkEntry):
                val = widget.get()
                widget.delete(0,customtkinter.END)
            elif isinstance(widget, customtkinter.CTkSwitch):
                val = widget.get()
            elif isinstance(widget, customtkinter.CTkTextbox):
                val = widget.get("1.0", "end-1c")
                widget.delete("1.0", tkinter.END)
            values_detail.append(val)
        sql.update_detail_info(self.data_detail[0],numbers,self.data_comp[0],*values_detail)
        self.FillComboBoxes()
        
        
        
        
    def DellData(self):
        id_basic=self.data_detail[1]
        id_comp=self.data_detail[2]
        id_details=self.data_detail[0]
        sql.delete_statuses_by_basic_info_id(id_basic)
        sql.delete_detail_info(id_details)
        sql.delete_photos_by_basic_id(id_basic)
        sql.delete_basic_info(id_basic)
        sql.delete_component_info(id_comp)
        
        self.FillComboBoxes()

    def ClearData(self):
        # Очистка виджетов описания
        for widget in self.widgetsDescription:
            if isinstance(widget, customtkinter.CTkEntry):
                widget.delete(0, tkinter.END)
            elif isinstance(widget, customtkinter.CTkTextbox):
                widget.delete("1.0", tkinter.END)
    
        # Очистка виджетов детального описания
        for widget in self.widgetsDetailDescription:
            if isinstance(widget, customtkinter.CTkEntry):
                widget.delete(0, tkinter.END)
            elif isinstance(widget, customtkinter.CTkTextbox):
                widget.delete("1.0", tkinter.END)
           
    
        # Очистка виджетов компонентов
        for widget in self.widgetsComponents:
            if isinstance(widget, customtkinter.CTkEntry):
                widget.delete(0, tkinter.END)

        
    
    
    def FillComboBoxes(self):
        ToComboBoxOne = sql.get_basic_info()
        sasha = [str(data[0]) + " | " + str(data[1]) for data in ToComboBoxOne]
        self.combobox1.configure(values=sasha)
        self.update()
        
             
            
            
            
            
            

if __name__ == "__main__":
    root = tkinter.Tk()
    app = editPC(root)
    root.mainloop()