import customtkinter
import tkinter
import re
from db import *
from CTkMessagebox import CTkMessagebox
from hPyT import *
from PIL import Image
import os
from tkcalendar import Calendar
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from datetime import datetime
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


sql = SQL(server='DDLAPTOP\SQLEXPRESS', database='PC')
sql.connect()



class Reports(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_widgets()
        
    
    def create_widgets(self):
        self.title("Edit Computer")
        self.geometry("350x  450")
        self.minsize  (350,  450)
        self.maxsize  (350,  450)
        maximize_minimize_button.hide(self)
        self.grid_columnconfigure((1),weight=1)
        self.grid_rowconfigure((0,1),weight=1)
        self.create_frame1()
        self.create_frame2()
        #self.create_frame3()

        
        
        
        
        
    def create_frame1(self):
        self.frame1 = customtkinter.CTkFrame(self,height=320)
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.frame1.grid_columnconfigure((0,1,2,3),weight=1)
        customtkinter.CTkLabel(master=self.frame1,text="Отчет по статусам работы",fg_color="gray30", font=("Arial", 14)).grid(row=0,columnspan=4, column=0, padx=10, pady=10, sticky="ew")
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        
        customtkinter.CTkLabel(master=self.frame1,text="Выберите дату начала периода").grid(row=1, column=0, padx=10,columnspan=4, pady=10, sticky="ew")
        self.DataStart_entry = customtkinter.CTkEntry(master=self.frame1, placeholder_text="ГГГГ-ММ-ДД")
        self.DataStart_entry.grid(row=2, column=1,columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "calendarICO.png")), size=(20, 20))
        self.CalendarOpenButton = customtkinter.CTkButton(master=self.frame1, text="Выбрать дату",image=self.image_icon_image, command=lambda: [self.select_date1()])
        self.CalendarOpenButton.grid(row=2, column=3, pady=5, padx=10, sticky="ew")
        
        
        customtkinter.CTkLabel(master=self.frame1,text="Выберите дату начала конца").grid(row=3, column=0, padx=10,columnspan=4, pady=10, sticky="ew")
        self.DataEnd_entry = customtkinter.CTkEntry(master=self.frame1, placeholder_text="ГГГГ-ММ-ДД")
        self.DataEnd_entry.grid(row=4, column=1,columnspan=2, padx=10, pady=10, sticky="ew")
        
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "calendarICO.png")), size=(20, 20))
        self.CalendarOpenButton = customtkinter.CTkButton(master=self.frame1, text="Выбрать дату",image=self.image_icon_image, command=lambda: [self.select_date2()])
        self.CalendarOpenButton.grid(row=4, column=3, pady=5, padx=10, sticky="ew")
        
        
        self.MakeReport1Button = customtkinter.CTkButton(master=self.frame1, text="Сформировать и открыть отчет", command=lambda: self.MakeReport1())
        self.MakeReport1Button.grid(row=5, column=0,columnspan=4, pady=5, padx=10, sticky="ew")
    

      
    def create_frame2(self):
        self.frame2 = customtkinter.CTkFrame(self,height=520)
        self.frame2.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.frame2.grid_columnconfigure((0,1,2,3),weight=1)
        customtkinter.CTkLabel(master=self.frame2,text="Отчет по месту установки",fg_color="gray30", font=("Arial", 14)).grid(row=0,columnspan=4, column=0, padx=10, pady=10, sticky="ew")
        
        self.combobox1= customtkinter.CTkComboBox(master=self.frame2,values=[" "], state="readonly")
        self.combobox1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.FillComboBoxes()
        
        self.MakeReport2Button = customtkinter.CTkButton(master=self.frame2, text="Сформировать и открыть отчет", command=lambda: self.MakeReport2())
        self.MakeReport2Button.grid(row=2, column=0,columnspan=4, pady=5, padx=10, sticky="ew")
    def MakeReport2(self):
        currVal = self.combobox1.get()
        data=sql.get_device_info_by_location(currVal)
        
        try:
            # Создание нового документа
            doc = Document()

            # Заголовок документа
            title = doc.add_heading('Device Location Report', level=1)
            title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

            # Добавление таблицы с данными
            table = doc.add_table(rows=1, cols=4)
            table.style = 'Table Grid'

            # Заголовки столбцов
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = 'IP'
            hdr_cells[1].text = 'Location'
            hdr_cells[2].text = 'Last Repair'
            hdr_cells[3].text = 'Last Status'

            # Форматирование текста
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        run = paragraph.runs[0]
                        font = run.font
                        font.name = 'Arial'  # Название шрифта
                        font.size = Pt(11)    # Размер шрифта
                        font.bold = True      # Жирный шрифт
                        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # Выравнивание по центру

            # Добавление данных из списка в таблицу
            for ip, location, last_repair, status in data:
                row_cells = table.add_row().cells
                row_cells[0].text = ip
                row_cells[1].text = location
                row_cells[2].text = str(last_repair)
                status_text = 'On' if status else 'Off'
                row_cells[3].text = status_text
                # Установка цвета текста в ячейке в зависимости от статуса
                if status:
                    color = RGBColor(0, 128, 0)  # Зеленый цвет для "On"
                else:
                    color = RGBColor(255, 0, 0)  # Красный цвет для "Off"
                for paragraph in row_cells[3].paragraphs:
                    for run in paragraph.runs:
                        run.font.color.rgb = color

            file_path = 'Device_Location_Report.docx'
            # Удаление файла, если он существует
            if os.path.exists(file_path):
                os.remove(file_path)
            # Сохранение документа
            doc.save(file_path)
            # Открытие файла с помощью программы по умолчанию
            os.startfile(file_path)

        except Exception as e:
            print(f"Error creating report: {str(e)}")
        
        
    
        
        
    #def create_frame3(self):
    #    self.frame3 = customtkinter.CTkScrollableFrame(self, height=920, width=650)
    #    self.frame3.grid(row=0, rowspan=3, column=2, padx=10, pady=10, sticky="ew")
    #    self.frame3.grid_columnconfigure((0,1,2,3), weight=1)
    #    customtkinter.CTkLabel(master=self.frame3, text="Отчет по параметрам", fg_color="gray30", font=("Arial", 14)).grid(row=0, columnspan=4, column=0, padx=10, pady=10, sticky="ew")

    
        
        
        
    def select_date1(self):
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
                self.DataStart_entry.delete(0, 'end')  
                self.DataStart_entry.insert(0, selected_date)  
                self.additionalWIN.destroy() 
            cal.pack() 
            cal.bind('<<CalendarSelected>>', lambda event: set_date())
        except Exception as e:
            print(f"Exception in SelecTData: {e}")       
            
    def select_date2(self):
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
                self.DataEnd_entry.delete(0, 'end')  
                self.DataEnd_entry.insert(0, selected_date)  
                self.additionalWIN.destroy() 
            cal.pack() 
            cal.bind('<<CalendarSelected>>', lambda event: set_date())
        except Exception as e:
            print(f"Exception in SelecTData: {e}")        

    def FillComboBoxes(self):
        ToComboBoxOne = sql.get_basic_info()
        qwe={''} ##все кабинетики (вкладочки)
        for i in range(len(ToComboBoxOne)):
            qwe.add(ToComboBoxOne[i][3])

        qwe.discard('')
        qwe = sorted(qwe)
        sasha = [str(data) for data in qwe]
        self.combobox1.configure(values=sasha)
        self.update()
    def MakeReport1(self):
        date_start = self.DataStart_entry.get()
        date_end = self.DataEnd_entry.get()
        data = sql.call_PCStatusDuringPeriod_procedure(date_start, date_end)

        # Создание нового документа
        doc = Document()

        # Заголовок документа
        title = doc.add_heading('PC Status Report', level=1)
        title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Добавление таблицы с данными
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'

        # Заголовки столбцов
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'IP'
        hdr_cells[1].text = 'Location'
        hdr_cells[2].text = 'Status'
        hdr_cells[3].text = 'Date'

        # Форматирование текста
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    run = paragraph.runs[0]
                    font = run.font
                    font.name = 'Arial'  # Название шрифта
                    font.size = Pt(11)    # Размер шрифта
                    font.bold = True      # Жирный шрифт
                    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # Выравнивание по центру

        # Добавление данных из списка в таблицу
        for ip, location, status, date in data:
            row_cells = table.add_row().cells
            row_cells[0].text = ip
            row_cells[1].text = location
            status_text = 'On' if status else 'Off'
            row_cells[2].text = status_text
            # Установка цвета текста в ячейке в зависимости от статуса
            if status:
                color = RGBColor(0, 128, 0)  # Зеленый цвет для "On"
            else:
                color = RGBColor(255, 0, 0)  # Красный цвет для "Off"
            for paragraph in row_cells[2].paragraphs:
                for run in paragraph.runs:
                    run.font.color.rgb = color

            row_cells[3].text = str(date)
        file_path = 'PC_Status_Report.docx'
        # Удаление файла, если он существует
        if os.path.exists(file_path):
            os.remove(file_path)
        # Сохранение документа
        doc.save(file_path)
        # Открытие файла с помощью программы по умолчанию
        os.startfile(file_path)

if __name__ == "__main__":
    root = tkinter.Tk()
    app = Reports(root)
    root.mainloop()