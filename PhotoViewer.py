import customtkinter
from db import *
import os
import shutil
from tkinter import filedialog
from ctkcomponents import *
from CTkMessagebox import CTkMessagebox
from hPyT import *
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

sql = SQL(server='DDLAPTOP\SQLEXPRESS', database='PC')
sql.connect()

class PhotoViewer(customtkinter.CTkToplevel):

    @staticmethod
    def get_image_paths(photo_data):
        return [os.path.join("images", photo[2]) for photo in photo_data]
    @staticmethod
    def update_carousel(self):
        images = sql.get_photos_by_basic_id(self.photo_id)
        image_paths = PhotoViewer.get_image_paths(images)
        my_carousel = CTkCarousel(master=self.additionalWIN.frame_p, img_list=image_paths, width=400, height=400, img_radius=25)
        my_carousel.grid(row=0, column=0, padx=20, pady=20, columnspan=3)
    @staticmethod
    def PhotoView(self, photo_id):
        try:
            if hasattr(self, 'additionalWIN') and self.additionalWIN.winfo_exists():
                self.additionalWIN.focus()
                return

            self.photo_id = photo_id
            self.additionalWIN = customtkinter.CTkToplevel(self)
            self.additionalWIN.geometry("460x730")
            self.additionalWIN.minsize(460,730)
            self.additionalWIN.maxsize(460,730)
            maximize_minimize_button.hide(self.additionalWIN)
            self.additionalWIN.title(f"Photo Viewer for {self.photo_id}")
            self.additionalWIN.focus()
            images = sql.get_photos_by_basic_id(self.photo_id)
            image_paths = PhotoViewer.get_image_paths(images)
            self.additionalWIN.rowconfigure(1, weight=1)
            self.additionalWIN.frame_p = customtkinter.CTkFrame(master=self.additionalWIN, width=300)
            self.additionalWIN.frame_p.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
            self.additionalWIN.frame_p.columnconfigure(0, weight=1)
            self.additionalWIN.frame_p.rowconfigure(0, weight=1)
            
            if images:
                PhotoViewer.update_carousel(self)


            label = customtkinter.CTkLabel(master=self.additionalWIN.frame_p, text="Добавить фото", fg_color="gray30", font=("Arial", 12))
            label.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

            AddPhotoButton = customtkinter.CTkButton(master=self.additionalWIN.frame_p, text="Выбрать и добавить", hover_color="green", command=lambda: PhotoViewer.AddPic(self))
            AddPhotoButton.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

            self.additionalWIN.frame_l = customtkinter.CTkFrame(master=self.additionalWIN, width=300)
            self.additionalWIN.frame_l.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
            self.additionalWIN.frame_l.columnconfigure(0, weight=1)

            label2 = customtkinter.CTkLabel(master=self.additionalWIN.frame_l, text="Удалить фото", fg_color="gray30", font=("Arial", 12))
            label2.grid(row=4, column=0, padx=10, columnspan=3, pady=10, sticky="ew")

            label3 = customtkinter.CTkLabel(master=self.additionalWIN.frame_l, text="Выберите фото", font=("Arial", 12))
            label3.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

            self.combobox1 = customtkinter.CTkComboBox(master=self.additionalWIN.frame_l, values=[" "], state="readonly")
            self.combobox1.grid(row=5, column=1, padx=10, pady=10, sticky="ew")
            PhotoViewer.FillComboBoxes(self)

            ViewPhotoButton = customtkinter.CTkButton(master=self.additionalWIN.frame_l, text="Просмотреть", command=lambda: PhotoViewer.OpenPic(self))
            ViewPhotoButton.grid(row=5, column=2, pady=10, padx=10, sticky="ew")

            DellPhotoButton = customtkinter.CTkButton(master=self.additionalWIN.frame_l, text="Удалить фото", hover_color="red", command=lambda: PhotoViewer.DelPic(self))
            DellPhotoButton.grid(row=6, column=0, pady=10, columnspan=3, padx=10, sticky="ew")

        except Exception as e:
            print(f"Exception in PhotoViewer: {e}")

    @staticmethod
    def OpenPic(self):
        curval = self.combobox1.get()
        path = os.path.join("images", curval)
        print(path)
        os.startfile(path)
        
    @staticmethod
    def AddPic(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Изображения", "*.jpg;*.jpeg;*.png")]
        )
        if file_path:
            try:
                print(file_path)
                file_name = os.path.basename(file_path)
                target_file_path = os.path.join("images", file_name)
                shutil.copy(file_path, "images")
                sql.add_photo(self.photo_id, file_name)
                PhotoViewer.FillComboBoxes(self)
                PhotoViewer.update_carousel(self)
            except Exception as e:
                print(f"Ошибка при открытии изображения: {e}")
        
    @staticmethod
    def DelPic(self):
        try:
            curval = self.combobox1.get()
            sql.delete_photo_by_path(curval)
            path = os.path.join("images", curval)
            os.remove(path)
            CTkMessagebox(title="Успех", message="Фото успешно удалено!", icon="check", option_1="Ok")
            PhotoViewer.FillComboBoxes(self)
            PhotoViewer.update_carousel(self)
        except IOError as e:
            CTkMessagebox(title="Ошибка", message="Во время удаления произошла ошибка!", icon="cancel")
            return False
    
    @staticmethod    
    def FillComboBoxes(self):
        
        ToComboBoxOne = sql.get_photos_by_basic_id(self.photo_id)
        if not ToComboBoxOne:
            # Если список пуст, установите пустое значение в combobox
            self.combobox1.configure(values=[" "])
            return

        sasha = [str(data[2]) for data in ToComboBoxOne]
        self.combobox1.configure(values=sasha)
        self.update()
