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
        
        customtkinter.CTkLabel(master=self.EditDataFrame,text="Открыть папку с документами к компьютеру").grid(row=3,columnspan=2, column=0, padx=10, pady=10, sticky="ew")
        self.OpenFolderRepairButton = customtkinter.CTkButton(master=self.EditDataFrame, text="Открыть папку", command=lambda: self.OpenFolder())
        self.OpenFolderRepairButton.grid(row=3, column=2, pady=5, padx=10, sticky="ew")
        
        
        self.ApplyDataFrame=customtkinter.CTkFrame(self.frame,fg_color="#242424")
        self.ApplyDataFrame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        self.ApplyDataFrame.columnconfigure((0,1,2),weight=1)
        
        
        self.AddRepairButton = customtkinter.CTkButton(master=self.ApplyDataFrame, text="Добавить",hover_color="green", command=lambda: self.AddRepair())
        self.AddRepairButton.grid(row=1, column=0, pady=5, padx=10, sticky="ew")
        
        self.SaveChangesRepairButton = customtkinter.CTkButton(master=self.ApplyDataFrame, text="Сохранить",hover_color="green", command=lambda: self.SaveChangesRepair())
        self.SaveChangesRepairButton.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
        
        self.DellRepairButton = customtkinter.CTkButton(master=self.ApplyDataFrame, text="Удалить",hover_color="red", command=lambda: self.DellRepair())
        self.DellRepairButton.grid(row=1, column=2, pady=5, padx=10, sticky="ew")
        
        
        
        
        
       
    def OpenFolder(self):
        currVal = self.combobox1.get()
        parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
        if len(parts) > 0:
            repair_id = parts[0].strip()  # Получить первую подстроку и удалить лишние пробелы

            try:
                repair_id = int(repair_id)  # Преобразовать строку в целое число
                # Формирование пути к папке ремонта
                repair_folder_path = os.path.join("repairs", str(repair_id))

                # Проверка существования папки
                if os.path.exists(repair_folder_path):
                    # Открытие папки в системном проводнике
                    os.startfile(repair_folder_path)
                else:
                    CTkMessagebox(title="Ошибка", message="Папка ремонта не существует!", icon="cancel")
                
            except ValueError:
                CTkMessagebox(title="Ошибка", message="Возможно папка была создана некорректно!", icon="cancel")
    def LoadRepair(self):
        currVal = self.combobox2.get()
        print(f"curval = {currVal}")
        parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
        if len(parts) > 0:
            repair_id = parts[0].strip() 
            try:
                repair_id = int(repair_id)  # Преобразовать строку в целое число
                repair_data = sql.get_repair_by__id(repair_id)  # Получить данные о ремонте по идентификатору
                if repair_data:
                    self.ClearData()
                    self.DecriptiontextBox.insert(tkinter.END, repair_data[2])      
                    self.DataOfRepaor_entry.insert(0, repair_data[3]) 
                else:
                    CTkMessagebox(title="Ошибка", message="Ремонт не найден!", icon="cancel")
            except ValueError:
                CTkMessagebox(title="Ошибка", message="Неверный формат идентификатора ремонта!", icon="cancel")

           
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
            print(sql.get_repairs_by_basic_id(numbers))
            if not ToComboBoxSec:
                self.combobox2.configure(values=[" "])
                CTkMessagebox(title="Ошибка",message="Не выбран компьютер! ", icon="cancel")
                return
            else:
                if not ToComboBoxSec[0] or ToComboBoxSec[0]=="":
                    CTkMessagebox(title="Ошибка",message="Не найдено ремонтов! ", icon="cancel")
                    return
                else:
                    third_elements = [[record[0], record[3]] for sublist in ToComboBoxSec for record in sublist]
                    sasha2=[]
                    print(third_elements)
                    sorted_third_elements = sorted(third_elements, key=lambda x: x[1])
                    print(sorted_third_elements)
                    for text in sorted_third_elements:
                        sasha2.append(str(text[0])+" | "+str(text[1]))
                        print(text[1])
                    self.combobox2.configure(values=sasha2)
                    self.update()
        else:
            return
    
    
    def create_repair_folder(self, repair_id):
        try:
            # Получите путь к папке repairs
            repairs_folder = "repairs"
            # Проверьте, существует ли папка repairs, и если нет, создайте ее
            if not os.path.exists(repairs_folder):
                os.makedirs(repairs_folder)
            # Создайте папку для нового ремонта на основе его ID
            repair_folder_path = os.path.join(repairs_folder, str(repair_id))
            if not os.path.exists(repair_folder_path):
                os.makedirs(repair_folder_path)
            print(f"Folder for repair {repair_id} created successfully.")
            return repair_folder_path
        except Exception as e:
            CTkMessagebox(title="Ошибка",message="Ошибка создания папки! ", icon="cancel")
            return None
        
    def AddRepair(self):
        try:
            descrRep=self.DecriptiontextBox.get("1.0", "end-1c")
            dateRep=self.DataOfRepaor_entry.get()
            currVal = self.combobox1.get()
            parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
            if len(parts) > 0:
                numbers = parts[0].strip() 
                qwe = int(numbers)
            else:
                qwe = 1
            
            pathRep=self.create_repair_folder(numbers)
            sql.insert_repair(numbers,descrRep,dateRep,pathRep)
            self.FillComboBox2()
        except Exception as e:
            CTkMessagebox(title="Ошибка",message="Ошибка добавления ремонта! ", icon="cancel")
            return None
        
        
    def SaveChangesRepair(self):
        try:
            currVal = self.combobox2.get()
            print(f"curval = {currVal}")
            parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
            if len(parts) > 0:
                repair_id = parts[0].strip() 
                repair_id = int(repair_id) 
                description=self.DecriptiontextBox.get("1.0", "end-1c")
                repair_date=self.DataOfRepaor_entry.get()
            else:
                return

            # Проверить, что все необходимые данные заполнены
            if repair_id and description and repair_date:
                # Попытаться обновить запись ремонта
                sql.update_repair(repair_id, description, repair_date)
                # Вывести сообщение об успешном обновлении
                CTkMessagebox(title="Успех", message="Ремонт успешно обновлен!", icon="info")
            else:
                # Вывести сообщение об ошибке, если не все данные заполнены
                CTkMessagebox(title="Ошибка", message="Пожалуйста, заполните все поля!", icon="warning")
        except Exception as e:
            # Вывести сообщение об ошибке при возникновении исключения
                CTkMessagebox(title="Ошибка", message=f"Ошибка при сохранении изменений: {e}", icon="error")
    def DellRepair(self):
        try:
            currVal = self.combobox2.get()
            print(f"curval = {currVal}")
            parts = currVal.split('|')  # Разделить строку на подстроки по символу '|'
            if len(parts) > 0:
                repair_id = parts[0].strip() 
                repair_id = int(repair_id) 
            else:
                return
            # Проверить, что все необходимые данные заполнены
            if repair_id:
                # Попытаться обновить запись ремонта
                sql.delete_repair(repair_id)
                # Вывести сообщение об успешном обновлении
                CTkMessagebox(title="Успех", message="Ремонт успешно удалён!", icon="info")
                self.ClearData()
            else:
                # Вывести сообщение об ошибке, если не все данные заполнены
                CTkMessagebox(title="Ошибка", message="Что-то пошло не так!", icon="warning")
        except Exception as e:
            # Вывести сообщение об ошибке при возникновении исключения
                CTkMessagebox(title="Ошибка", message=f"Ошибка при удалении ремонта: {e}", icon="error")
        
        
        

             
            
            
            
            
            

if __name__ == "__main__":
    root = tkinter.Tk()
    app = Repairs(root)
    root.mainloop()