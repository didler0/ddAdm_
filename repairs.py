import customtkinter
import tkinter
import re
from db import *
from tkcalendar import Calendar
from CTkMessagebox import CTkMessagebox
from hPyT import *
from PIL import Image
import os
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


sql = SQL(server='DDLAPTOP\SQLEXPRESS', database='PC')
sql.connect()
sql.create_tables_if_not_exist()

def switch_event(switch_var):
        print("switch toggled, current value:", switch_var.get())

class Repairs(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_widgets()
        
    
    def create_widgets(self):
        self.title("Repairs")
        self.geometry("600x520")
        self.minsize  (600, 520)
        self.maxsize  (600, 520)
        maximize_minimize_button.hide(self)
        #self.frame = customtkinter.CTkScrollableFrame(self,height=490)
        self.frame = customtkinter.CTkFrame(self,height=490)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.grid_columnconfigure(0,weight=1)
        self.frame.grid_columnconfigure(0,weight=1)
        self.LoadDataFrame=customtkinter.CTkFrame(self.frame,fg_color="#242424")
        self.LoadDataFrame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.LoadDataFrame.columnconfigure((0,1,2),weight=1)
        
        
        customtkinter.CTkLabel(master=self.LoadDataFrame,text="Загрузка данных",fg_color="gray30", font=("Arial", 14)).grid(row=0,columnspan=3, column=0, padx=10, pady=10, sticky="ew")
        
        customtkinter.CTkLabel(master=self.LoadDataFrame,text="Выберите ПК").grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.combobox1= customtkinter.CTkComboBox(master=self.LoadDataFrame,values=[" "], state="readonly")
        self.combobox1.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.FillComboBox1()
        self.AddPcBasicButton = customtkinter.CTkButton(master=self.LoadDataFrame, text="Загрузить ремонты", command=lambda: self.LoadData())
        self.AddPcBasicButton.grid(row=1, column=2, pady=5, padx=10, sticky="ew")
        customtkinter.CTkLabel(master=self.LoadDataFrame,text="Выберите ремонт").grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.combobox2= customtkinter.CTkComboBox(master=self.LoadDataFrame,values=[" "], state="readonly")
        self.combobox2.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        self.LoadRepaiesButton = customtkinter.CTkButton(master=self.LoadDataFrame, text="Загрузить ремонт", command=lambda: self.LoadRepair())
        self.LoadRepaiesButton.grid(row=2, column=2, pady=5, padx=10, sticky="ew")

        
        self.EditDataFrame=customtkinter.CTkFrame(self.frame,fg_color="#242424")
        self.EditDataFrame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.EditDataFrame.columnconfigure((0,1,2),weight=1)
        
        customtkinter.CTkLabel(master=self.EditDataFrame,text="Ремонты",fg_color="gray30", font=("Arial", 14)).grid(row=0,columnspan=3, column=0, padx=10, pady=10, sticky="ew")
        
        customtkinter.CTkLabel(master=self.EditDataFrame,text="Описание").grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.DecriptiontextBox=customtkinter.CTkTextbox(master=self.EditDataFrame,height=90)
        self.DecriptiontextBox.grid(row=1, column=1,columnspan=2, padx=10, pady=10, sticky="ew")

        
        customtkinter.CTkLabel(master=self.EditDataFrame,text="Дата ремонта").grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.DataOfRepaor_entry = customtkinter.CTkEntry(master=self.EditDataFrame, placeholder_text="ГГГГ-ММ-ДД")
        self.DataOfRepaor_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "calendarICO.png")), size=(20, 20))
        self.CalendarOpenButton = customtkinter.CTkButton(master=self.EditDataFrame, text="Выбрать дату",image=self.image_icon_image, command=lambda: [self.select_date(),self.select_date()])
        self.CalendarOpenButton.grid(row=2, column=2, pady=5, padx=10, sticky="ew")
        
        customtkinter.CTkLabel(master=self.EditDataFrame,text="Открыть папку с документами к ремонту").grid(row=3,columnspan=2, column=0, padx=10, pady=10, sticky="ew")
        self.OpenFolderRepairButton = customtkinter.CTkButton(master=self.EditDataFrame, text="Открыть папку", command=lambda: print(self.combobox2.get()))
        self.OpenFolderRepairButton.grid(row=3, column=2, pady=5, padx=10, sticky="ew")
        
        
        self.ApplyDataFrame=customtkinter.CTkFrame(self.frame,fg_color="#242424")
        self.ApplyDataFrame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.ApplyDataFrame.columnconfigure((0,1,2),weight=1)
        
        
        self.AddRepairButton = customtkinter.CTkButton(master=self.ApplyDataFrame, text="Добавить",hover_color="green", command=lambda: print(self.combobox2.get()))
        self.AddRepairButton.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
        
        self.SaveChangesRepairButton = customtkinter.CTkButton(master=self.ApplyDataFrame, text="Сохранить",hover_color="green", command=lambda: print(self.combobox2.get()))
        self.SaveChangesRepairButton.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        self.DellRepairButton = customtkinter.CTkButton(master=self.ApplyDataFrame, text="Удалить",hover_color="red", command=lambda: print(self.combobox2.get()))
        self.DellRepairButton.grid(row=1, column=2, pady=5, padx=10, sticky="ew")
        
        
        
        
        
       
       
    def LoadRepair(self):
        currVal = self.combobox2.get()
        parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
        if len(parts) > 0:
            numbers = parts[0].strip() 
        data=sql.get_repairs_by_basic_id(numbers)
        print(data)
        try:
            self.ClearData()
            self.DecriptiontextBox.insert(tkinter.END, data[0][2])      
            self.DataOfRepaor_entry.insert(0,data[0][3]) 
        except Exception as e:
            CTkMessagebox(title="Ошибка",message="Не выбран ремонт! ", icon="cancel")
           
    def select_date(self):
        try:
            if hasattr(self, 'additionalWIN') and self.additionalWIN.winfo_exists():
                self.additionalWIN.focus()
                return
            self.additionalWIN = customtkinter.CTkToplevel(self)
            self.additionalWIN.geometry("260x200")
            self.additionalWIN.focus()
            self.additionalWIN.title(f"Calendar")
            self.additionalWIN.focus()
            maximize_minimize_button.hide(self.additionalWIN)
            cal = Calendar(self.additionalWIN, selectmode='day',date_pattern="yyyy-mm-dd")
            def set_date():
                selected_date = cal.get_date()
                self.DataOfRepaor_entry.delete(0, 'end')  
                self.DataOfRepaor_entry.insert(0, selected_date)  
                self.additionalWIN.destroy() 
            cal.pack() 
            cal.bind('<<CalendarSelected>>', lambda event: set_date())
        except Exception as e:
            print(f"Exception in SelecTData: {e}")

            
            
            
    def LoadData(self):
        self.FillComboBox2()
        
        
    def ClearData(self):
        # Очистка виджетов описания
        self.DataOfRepaor_entry.delete(0, tkinter.END)
        self.DecriptiontextBox.delete("1.0", tkinter.END)
        
        
   
        
        

        
    
    
    def FillComboBox1(self):
        ToComboBoxOne = sql.get_basic_info()
        
        if not ToComboBoxOne:
            # Если список пуст, установите пустое значение в combobox
            self.combobox1.configure(values=[" "])
            return
        else:
            sasha = [str(data[0]) + " | " + str(data[1]) for data in ToComboBoxOne]
            self.combobox1.configure(values=sasha)
            self.update()
            
    def FillComboBox2(self):
        currVal = self.combobox1.get()
        parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
        if len(parts) > 0:
            numbers = parts[0].strip()  # Получить первую подстроку и удалить лишние пробелы
            ToComboBoxSec = sql.get_repairs_by_basic_id(numbers)
            if not ToComboBoxSec:
                self.combobox2.configure(values=[" "])
                CTkMessagebox(title="Ошибка",message="Не выбран компьютер! ", icon="cancel")
                return
            else:
                sasha2 = [str(data[0]) + " | " + str(data[3]) for data in ToComboBoxSec if data is not None]
                self.combobox2.configure(values=sasha2)
                self.update()
        else:
            return
        
        
        
        

             
            
            
            
            
            

if __name__ == "__main__":
    root = tkinter.Tk()
    app = Repairs(root)
    root.mainloop()