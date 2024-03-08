import customtkinter
from db import *
import os
import shutil
from tkinter import filedialog
import tkinter
from ctkcomponents import *
from CTkMessagebox import CTkMessagebox
from hPyT import *
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

sql = SQL(server='DDLAPTOP\SQLEXPRESS', database='PC')
sql.connect()

class DescriptionViewer(customtkinter.CTkToplevel):

    @staticmethod
    def DescriptionView(self, pc_id):
        try:
            if hasattr(self, 'additionalWIN') and self.additionalWIN.winfo_exists():
                self.additionalWIN.focus()
                return

            self.pc_id = pc_id
            
            self.additionalWIN = customtkinter.CTkToplevel(self)
            self.additionalWIN.geometry("600x555")
            self.additionalWIN.minsize  (600,555)
            self.additionalWIN.maxsize  (600,555)
            
            maximize_minimize_button.hide(self.additionalWIN)
            self.additionalWIN.title(f"Description {self.pc_id}")
            self.additionalWIN.focus()
            
            
            
            self.frame = customtkinter.CTkScrollableFrame(self.additionalWIN,height=520,)
            self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
            self.additionalWIN.grid_columnconfigure(0,weight=1)
            
            #self.frame.grid_columnconfigure(0,weight=1)
            
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


                #делаем делатьное описание
                labels_text_detail_ru=["Инв. №","Серийный №","MAC-адрес","Wake on LAN","Пароль VNC"]
                labels_text_detail = ["inventory_number","serial_number","mac_address","wake_on_lan","vnc_password"]

                self.widgetsDetailDescription=[]

                for i,text in enumerate(labels_text_detail_ru):
                    label = customtkinter.CTkLabel(master=self.tabview.tab("Детальное описание"), text=text, font=("Arial", 12))
                    label.grid(row=i, column=0, padx=10, pady=10, sticky="ew")
                    if text=="Wake on LAN":
                        entry = customtkinter.CTkEntry(master=self.tabview.tab("Детальное описание"), placeholder_text=text)
                        entry.grid(row=i, column=1, padx=10, pady=10, sticky="ew")       
                        self.widgetsDetailDescription.append(entry)
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
            DescriptionViewer.LoadData(self,pc_id)
            
                    
                





        except Exception as e:
            print(f"Exception in PhotoViewer: {e}")
            
    @staticmethod     
    def LoadData(self,idd):
        numbers=idd
            
        data_basic=sql.get_basic_info_by_id(numbers)
        data_basic_filtred=[]
        data_basic_filtred = data_basic[1:5]
        self.data_detail=sql.get_detail_info_by_id(numbers)
        self.data_detail_filtred = self.data_detail[3:8]
        self.data_comp=sql.get_components_by_id(self.data_detail[2])
        data_comp_filyted=self.data_comp[1:15]
        #self.widgetsDescription
        #self.widgetsComponents
        #self.widgetsDetailDescription
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

        # Установка данных в виджеты компонентов
        for i, value in enumerate(data_comp_filyted):

            self.widgetsComponents[i].insert(0, value)  # Установить значение в CTkEntry

