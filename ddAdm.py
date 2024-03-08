import customtkinter
from CTkXYFrame import *
from db import *
from addPc import *
from editPc import *
from PhotoViewer import *
from repairs import *
from datetime import datetime
import concurrent.futures
import os
import threading
import subprocess

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


sql = SQL(server='DDLAPTOP\SQLEXPRESS', database='PC')
sql.connect()
sql.create_tables_if_not_exist()


class UpperFrame(customtkinter.CTkFrame):
    def __init__(self, master,downFrameInstance):
        super().__init__(master)
        self.downInstance=downFrameInstance
        self.toplevel_window = None
        self.downInstance.destroy_and_recreate()
        self.AddPcButton = customtkinter.CTkButton(
            master=self, text="Добавить ПК", command=lambda: self.AddPc())
        self.AddPcButton.grid(row=0, column=0, pady=10,
                              padx=10)
        #
        #
        self.EditPcButton = customtkinter.CTkButton(
            master=self, text="Редактировать данные о ПК", command=lambda: self.EditPc())
        self.EditPcButton.grid(row=0, column=1, pady=10,
                               padx=10)
        #
        #
        self.ExportPcButton = customtkinter.CTkButton(
            master=self, text="Отчет данных", command=lambda: self.ExportPc())
        self.ExportPcButton.grid(
            row=0, column=2, pady=10, padx=10)
        #
        #
        #
        #
        #
        self.ReloadDataButton = customtkinter.CTkButton(
            master=self, text="Обновить", command=lambda: self.downInstance.destroy_and_recreate())
        self.ReloadDataButton.grid(
            row=0, column=3, pady=10, padx=10)
        #
        #
        #
        #
        #
        self.FilterButton = customtkinter.CTkButton(
            master=self, text="Фильтрация", command=lambda: self.FilterPc())
        self.FilterButton.grid(
            row=0, column=4, pady=10, padx=10)
        #
        #
        #
        self.RepairsButton = customtkinter.CTkButton(
            master=self, text="Ремонты", command=lambda: self.Repairs(),fg_color="#FF8C19",hover_color="#4DFFFF",text_color="black")
        self.RepairsButton.grid(
            row=0, column=4, pady=10, padx=10)
        #
        #
        #
        self.AppearanceButton = customtkinter.CTkOptionMenu(
            self, values=["Light", "Dark"], command=self.change_appearance_mode_event)
        self.AppearanceButton.grid(
            row=0, column=5, padx=20, pady=(10, 10))

    def AddPc(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # create window if its None or destroyed
            self.toplevel_window = addPC(self)
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def EditPc(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # create window if its None or destroyed
            self.toplevel_window = editPC(self)
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def ReloadData(self):
        self.scroll_frame.destroy_and_recreate()
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        if new_appearance_mode == "Light":
            customtkinter.set_appearance_mode(new_appearance_mode)
        elif new_appearance_mode == "Dark":
            customtkinter.set_appearance_mode(new_appearance_mode)
            
    def FilterPc(self):
        pass
    
    def Repairs(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            # create window if its None or destroyed
            self.toplevel_window = Repairs(self)
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def ExportPc(self):
        pass
    


class DownFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master,height=400)

        self.tabview = customtkinter.CTkTabview(master=self)
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        data = sql.get_basic_info()
        ips=[] ##все айпищники
        qwe={''} ##все кабинетики (вкладочки)
        self.tabs={}
        labels_text = ["Ip", "Название в сети", "Место установки", "Описание", "Фото",
                           "Статус", "Последний ремонт","VNC"]
        for i in range(len(data)):
            qwe.add(data[i][3])
            ips.append(data[i][1])
        qwe.discard('')
        qwe = sorted(qwe)
        #DownFrame.check_connections(ips)

        for i in qwe:
            tab=self.tabview.add(i)
            self.tabs[i] = tab
            
            
        for iq in range(len(data)):
                p=data[iq][3]
                if(p==i):
                    qwe=data[iq]
                    self.create_str(self,tab, qwe ,iq)

    @staticmethod
    def create_lables(self,tab):
        labels_text = ["Ip", "Название в сети", "Место установки", "Описание", "Фото",
                           "Статус", "Последний ремонт","VNC"]
        
        for idx, text in enumerate(labels_text):
            tab.grid_columnconfigure((0,1,2,3,4,5,6,7),weight=1)
            label = customtkinter.CTkLabel(master=tab, text=text, font=("Arial", 14))
            label.grid(row=0, column=idx, padx=10, pady=10, sticky="ew")
            
            
            
    @staticmethod
    def create_str(self,tab,data,iq):
        label = customtkinter.CTkLabel(master=tab, text=data[1], font=("Arial", 12))
        label.grid(row=iq+2, column=0, padx=10, pady=10)
        label = customtkinter.CTkLabel(master=tab, text=data[2], font=("Arial", 12))
        label.grid(row=iq+2, column=1, padx=10, pady=10)
        label = customtkinter.CTkLabel(master=tab, text=data[3], font=("Arial", 12))
        label.grid(row=iq+2, column=2, padx=10, pady=10)
        ##descr
        self.DesPcButtonPcButton = customtkinter.CTkButton(master=tab, text="Описание")  #, command=lambda i=i+1: Description.DescrPC(self, i))
        self.DesPcButtonPcButton.grid(row=iq+2, column=3, pady=10,padx=10)
        ##photo
        self.PhotoPcButtonPcButton = customtkinter.CTkButton(master=tab, text="Фото",command=lambda: PhotoViewer.PhotoView(self,data[0]))  #, command=lambda i=i+1: Description.DescrPC(self, i))
        self.PhotoPcButtonPcButton.grid(row=iq+2, column=4, pady=10,padx=10)
        
        if data[7]==None:
            label = customtkinter.CTkLabel(master=tab, text="----", font=("Arial", 12))
            label.grid(row=iq+2, column=6, padx=10, pady=10)
        else:
            label = customtkinter.CTkLabel(master=tab, text=data[7], font=("Arial", 12))
            label.grid(row=iq+2, column=6, padx=10, pady=10)
            
        self.VNCPcButton = customtkinter.CTkButton(     #(subprocess.run(["VNC.exe", data[iq][1]]))
        master=tab, text="VNC",width=30, command=lambda: (subprocess.run(["VNC.exe", data[1]])))
        self.VNCPcButton.grid(row=iq+2, column=7, pady=10,padx=10)

        if(data[5]==True):
            label11 = customtkinter.CTkLabel(master=tab, text="          ", bg_color="green")
            label11.grid(row=iq+2, column=5, padx=10, pady=10)
        elif data[5]==False:
            label11 = customtkinter.CTkLabel(master=tab, text="          ", bg_color="red")
            label11.grid(row=iq+2, column=5, padx=10, pady=10) 
        else:
            print("Trubles!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
        
   
    @staticmethod
    def check_connection(ip):
        try:
            ping_file = f"ping_{ip}.txt"
            os.system(f'ping -n 1 {ip} > "{ping_file}"')
            with open(ping_file, 'r', encoding='cp866') as file:
                ping = file.read()

            if f"Ответ от {ip}:" in ping:
                sql.add_status(ip,True)
                #print(f"{ip}")
                os.remove(ping_file)
                return True
            else:
                #print(f"Устройство с IP {ip} не доступно.")
                sql.add_status(ip,False)
                os.remove(ping_file)
                return False
        except Exception as e:
            #print(f"Error: {e}")
            return False

    @staticmethod
    def check_connections(ip_list):
        # Создание пула потоков
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Запуск задач для каждого IP-адреса
            future_to_ip = {executor.submit(DownFrame.check_connection, ip): ip for ip in ip_list}
            # Ожидание завершения задач
            for future in concurrent.futures.as_completed(future_to_ip):
                ip = future_to_ip[future]
                try:
                    # Получение результата задачи (если есть)
                    result = future.result()
                    print(f"Task for IP {ip} completed successfully.")
                except Exception as e:
                    print(f"Task for IP {ip} encountered an error: {e}")
    
    def destroy_and_recreate(self):
    # Уничтожаем существующие виджеты во всех вкладках
        for tab_name, tab in self.tabs.items():
            for widget in tab.winfo_children():
                widget.destroy()
        data = sql.get_basic_info()
        ips=[] ##все айпищники
        for i in range(len(data)):
            ips.append(data[i][1])
        DownFrame.check_connections(ips)
        for i in self.tabs:
            tab = self.tabs[i]
            for iq in range(len(data)):
                p = data[iq][3]
                if p == i:
                    qwe = data[iq]
                    DownFrame.create_lables(self,tab)
                    DownFrame.create_str(self,tab, qwe, iq)
                    
                    

        
            
        
        

        




        
    

    











class App(customtkinter.CTk):
    WIDTH = 1038
    HEIGHT = 500

    def __init__(self):
        super().__init__()

        self.title("ddAdmin")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.grid_columnconfigure(0, weight=1)

        
        self.frame_down=DownFrame(self)
        self.frame_down.grid(row=1,column=0,padx=10,pady=10, sticky="ew")
        self.frame_left = UpperFrame(self,self.frame_down)
        self.frame_left.grid(row=0, column=0, padx=10, pady=10)

        
        
        

if __name__ == "__main__":
    app = App()
    app.mainloop()