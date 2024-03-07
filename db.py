import pyodbc
from datetime import datetime
class SQL:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;')
            self.cursor = self.connection.cursor()
            print("Connection established successfully.")
        except Exception as e:
            print(f"Error establishing connection: {str(e)}")
    
    
    def create_trigger(self):
        try:
            # Создание триггера trg_StatusUpdate (если нету таблички)
            self.cursor.execute('''
                CREATE TRIGGER trg_StatusUpdate
                ON basic_info
                AFTER INSERT, UPDATE
                AS
                BEGIN
                    DECLARE @ip VARCHAR(15)
                    DECLARE @last_status BIT
                    DECLARE @data_status DATETIME

                    SELECT @ip = inserted.ip, @last_status = inserted.last_status, @data_status = inserted.data_status
                    FROM inserted

                    INSERT INTO statuses (basic_info_id, status_, status_date)
                    SELECT id, @last_status, @data_status
                    FROM basic_info
                    WHERE ip = @ip
                END
            ''')
            self.connection.commit()
            print("Trigger trg_StatusUpdate created successfully.")
        except Exception as e:
            print(f"Error creating trigger: {str(e)}")



    
    def create_tables_if_not_exist(self):
        try:
            self.create_trigger()
            #Проверка на наличие basic_info и ее создание
            self.cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'basic_info'")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('''
                    CREATE TABLE basic_info (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        ip VARCHAR(15),
                        network_name VARCHAR(50),
                        place_of_installation VARCHAR(50),
                        description VARCHAR(100),
                        last_status BIT,
                        data_status DATETIME,
                        last_repair DATE DEFAULT '-----'
                                            )
                ''')
                
                self.cursor.execute('''
                INSERT INTO basic_info (ip, network_name, place_of_installation, description, last_status, data_status, last_repair)
                VALUES ('192.168.1.1', 'Network1', 'Location1', 'Description1', 0, GETDATE(), GETDATE())
            ''')
                self.connection.commit()
                print("Table basic_info created.")

            

            # Проверка на наличие statuses и ее создание
            self.cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'statuses'")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('''
                    CREATE TABLE statuses (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        basic_info_id INT,
                        status_ BIT,
                        status_date DATETIME,
                        FOREIGN KEY (basic_info_id) REFERENCES basic_info(id) ON DELETE CASCADE
                    )
                ''')
                self.connection.commit()               
                print("Table statuses created.")

            # Проверка наличия repairs и ее создание
            self.cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'repairs'")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('''
                    CREATE TABLE repairs (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        basic_info_id INT,
                        description VARCHAR(100),
                        repair_date DATE,
                        document_path VARCHAR(100),
                        FOREIGN KEY (basic_info_id) REFERENCES basic_info(id) ON DELETE CASCADE
                    )
                ''')
                self.connection.commit()
                print("Table repairs created.")
                
            # Проверка наличия components и ее создание
            self.cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'components'")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('''
                    CREATE TABLE components (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        processor NVARCHAR(max) DEFAULT '-----',
                        ram NVARCHAR(max) DEFAULT '-----',
                        motherboard NVARCHAR(max) DEFAULT '-----',
                        graphicCard NVARCHAR(max) DEFAULT '-----',
                        psu NVARCHAR(max) DEFAULT '-----',
                        networkCard NVARCHAR(max) DEFAULT '-----',
                        cooler NVARCHAR(max) DEFAULT '-----',
                        chasis NVARCHAR(max) DEFAULT '-----',
                        hdd NVARCHAR(max) DEFAULT '-----',
                        ssd NVARCHAR(max) DEFAULT '-----',
                        monitor NVARCHAR(max) DEFAULT '-----',
                        keyboard NVARCHAR(max) DEFAULT '-----',
                        mouse NVARCHAR(max) DEFAULT '-----',
                        audio NVARCHAR(max) DEFAULT '-----'
                    )
                ''')
                self.connection.commit()
                print("Table components created.")
                
                
                # Проверка на наличие detail_info и ее создание
            self.cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'detail_info'")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('''
                    CREATE TABLE detail_info (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        basic_info_id INT,
                        components_id INT,
                        inventory_number VARCHAR(MAX),
                        serial_number VARCHAR(MAX),
                        mac_address VARCHAR(MAX),
                        wake_on_lan VARCHAR(MAX),
                        vnc_password VARCHAR(MAX),
                        FOREIGN KEY (basic_info_id) REFERENCES basic_info(id) ON DELETE CASCADE,
                        FOREIGN KEY (components_id) REFERENCES components(id) ON DELETE CASCADE
                    )
                ''')
                self.connection.commit()
                print("Table detail_info created.")
                
                
                # Проверка на наличие photo и ее создание
            self.cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'photo'")
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('''
                    CREATE TABLE photo (
                        id INT IDENTITY(1,1) PRIMARY KEY,
                        basic_id INT,
                        path VARCHAR(MAX),
                        FOREIGN KEY (basic_id) REFERENCES basic_info(id)
                    )
                ''')
                self.connection.commit()
                print("Table photo created.")
          
                
                
            
            print("All tables checked and created if necessary.")
        except Exception as e:
            print(f"Error creating tables: {str(e)}")

    def get_basic_info(self):
       try:
           #Дёргаем всю таблицу basic_info
           self.cursor.execute("SELECT * FROM basic_info")
           rows = self.cursor.fetchall()
           if rows:
               return rows
           else:
               return "No data found in basic_info table."
       except Exception as e:
           print(f"Error fetching data from basic_info table: {str(e)}")   
    
    def get_detail_info(self):
       try:
           #Дёргаем всю таблицу detail_info
           self.cursor.execute("SELECT * FROM detail_info")
           rows = self.cursor.fetchall()
           if rows:
               return rows
           else:
               return "No data found in detail_info table."
       except Exception as e:
           print(f"Error fetching data from detail_info table: {str(e)}")   

    def get_repairs(self):
       try:
           #Дёргаем всю таблицу repairs
           self.cursor.execute("SELECT * FROM repairs")
           rows = self.cursor.fetchall()
           if rows:
               return rows
           else:
               return "No data found in repairs table."
       except Exception as e:
           print(f"Error fetching data from repairs table: {str(e)}")            

    def get_statuses(self):
       try:
           #Дёргаем всю таблицу statuses
           self.cursor.execute("SELECT * FROM statuses")
           rows = self.cursor.fetchall()
           if rows:
               return rows
           else:
               return "No data found in statuses table."
       except Exception as e:
           print(f"Error fetching data from statuses table: {str(e)}")
           
    def add_status(self, ip_address, last_status):
        try:
            # Выполняем SQL-запрос для добавления нового статуса
            query = f'''
            UPDATE basic_info
            SET last_status = {int(last_status)}, data_status = GETDATE()
            WHERE ip = '{ip_address}'
            '''
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Status for IP {ip_address} updated successfully.")
            self.connection.commit()
        except Exception as e:
            print(f"Error adding status: {str(e)}")
            
    def add_basic_info(self, ip, network_name, place_of_installation, description):
        try:
            # Выполняем SQL-запрос для добавления новой записи
            query = f'''
            INSERT INTO basic_info (ip, network_name, place_of_installation, description, last_status, data_status,last_repair)
            VALUES ('{ip}', '{network_name}', '{place_of_installation}', '{description}', 0, GETDATE(), GETDATE())
            '''
            self.cursor.execute(query)
            print("New record added successfully.")
            self.connection.commit()
        except Exception as e:
            print(f"Error adding new record: {str(e)}")



    def add_component(self, processor, ram, motherboard, graphicCard, psu, networkCard, cooler, chasis, hdd, ssd, monitor, keyboard, mouse, audio):
        try:
            # Выполняем SQL-запрос для добавления записи в таблицу components
            self.cursor.execute('''
                INSERT INTO components (processor, ram, motherboard, graphicCard, psu, networkCard, cooler, chasis, hdd, ssd, monitor, keyboard, mouse, audio)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (processor, ram, motherboard, graphicCard, psu, networkCard, cooler, chasis, hdd, ssd, monitor, keyboard, mouse, audio))
            self.connection.commit()
            print("Record added to components successfully.")
        except Exception as e:
            print(f"Error adding record to components: {str(e)}")

    def add_detail_info(self, basic_info_id, components_id, inventory_number, serial_number, mac_address, wake_on_lan, vnc_password):
        try:
            # Выполняем SQL-запрос для добавления записи в таблицу detail_info
            self.cursor.execute('''
                INSERT INTO detail_info (basic_info_id, components_id, inventory_number, serial_number, mac_address, wake_on_lan, vnc_password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (basic_info_id, components_id, inventory_number, serial_number, mac_address, wake_on_lan, vnc_password))
            self.connection.commit()
            print("Record added to detail_info successfully.")
        except Exception as e:
            print(f"Error adding record to detail_info: {str(e)}")
            
 
    def get_last_basic_info_id(self):
        try:
            # Получаем последний добавленный идентификатор
            self.cursor.execute("SELECT IDENT_CURRENT('basic_info')")
            last_id = self.cursor.fetchone()[0]
            return last_id
        except Exception as e:
            print(f"Error retrieving last basic_info id: {str(e)}")
            return None

    def get_last_components_id(self):
        try:
            # Получаем последний добавленный идентификатор
            self.cursor.execute("SELECT IDENT_CURRENT('components')")
            last_id = self.cursor.fetchone()[0]
            return last_id
        except Exception as e:
            print(f"Error retrieving last components id: {str(e)}")
            return None



    def get_basic_info_by_id(self, id):
        try:
            # Выполнение SQL-запроса для выбора информации о базовом объекте по его ID
            query = f"SELECT * FROM basic_info WHERE id = {id}"
            self.cursor.execute(query)
            basic_info = self.cursor.fetchone()  # Получение одной записи (если она есть)

            # Если запись найдена, возвращаем ее
            if basic_info:
                return basic_info
            else:
                print(f"No basic info found with ID: {id}")
                return None

        except Exception as e:
            print(f"Error retrieving basic info by ID: {str(e)}")
            return None
        
    def get_detail_info_by_id(self, id):
        try:
            # Выполнение SQL-запроса для выбора информации о детальной информации по ее ID
            query = f"SELECT * FROM detail_info WHERE basic_info_id = {id}"
            self.cursor.execute(query)
            detail_info = self.cursor.fetchone()  # Получение одной записи (если она есть)

            # Если запись найдена, возвращаем ее
            if detail_info:
                return detail_info
            else:
                print(f"No detail info found with ID: {id}")
                return None

        except Exception as e:
            print(f"Error retrieving detail info by ID: {str(e)}")
            return None

    def get_components_by_id(self, id):
        try:
            # Выполнение SQL-запроса для выбора информации о компонентах по их ID
            query = f"SELECT * FROM components WHERE id = {id}"
            self.cursor.execute(query)
            components = self.cursor.fetchone()  # Получение одной записи (если она есть)

            # Если запись найдена, возвращаем ее
            if components:
                return components
            else:
                print(f"No components found with ID: {id}")
                return None

        except Exception as e:
            print(f"Error retrieving components by ID: {str(e)}")
            return None
    
    
    
    
    
    
    def update_basic_info(self,id, ip_address, network_name, place_of_installation, description):
        try:
            query = f'''
            UPDATE basic_info
            SET 
                ip = '{ip_address}',
                network_name = '{network_name}',
                place_of_installation = '{place_of_installation}',
                description = '{description}'
            WHERE id = '{int(id)}'
            '''
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Basic info for IP {ip_address} updated successfully.")
        except Exception as e:
            print(f"Error updating basic info: {str(e)}")


    def update_component_info(self, component_id, processor, ram, motherboard, graphicCard, psu, networkCard, cooler, chasis, hdd, ssd, monitor, keyboard, mouse, audio):
        try:
            query = f'''
            UPDATE components
            SET processor = '{processor}',
                ram = '{ram}',
                motherboard = '{motherboard}',
                graphicCard = '{graphicCard}',
                psu = '{psu}',
                networkCard = '{networkCard}',
                cooler = '{cooler}',
                chasis = '{chasis}',
                hdd = '{hdd}',
                ssd = '{ssd}',
                monitor = '{monitor}',
                keyboard = '{keyboard}',
                mouse = '{mouse}',
                audio = '{audio}'
            WHERE id = {component_id}
            '''
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Component with ID {component_id} updated successfully.")
        except Exception as e:
            print(f"Error updating component: {str(e)}")

    def update_detail_info(self, detail_id, basic_info_id, components_id, inventory_number, serial_number, mac_address, wake_on_lan, vnc_password):
        try:
            query = f'''
            UPDATE detail_info
            SET basic_info_id = {basic_info_id},
                components_id = {components_id},
                inventory_number = '{inventory_number}',
                serial_number = '{serial_number}',
                mac_address = '{mac_address}',
                wake_on_lan = '{wake_on_lan}',
                vnc_password = '{vnc_password}'
            WHERE id = {detail_id}
            '''
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Detail info with ID {detail_id} updated successfully.")
        except Exception as e:
            print(f"Error updating detail info: {str(e)}")
    
    
    
    
    def delete_basic_info(self, id):
        try:
            query = f"DELETE FROM basic_info WHERE id = '{id}'"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Basic info with ID {id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting basic info: {str(e)}")

    def delete_component_info(self, id):
        try:
            query = f"DELETE FROM components WHERE id = '{id}'"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Component info with ID {id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting component info: {str(e)}")

    def delete_detail_info(self, id):
        try:
            query = f"DELETE FROM detail_info WHERE id = {id}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Detail info with ID {id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting detail info: {str(e)}")
    def delete_statuses_by_basic_info_id(self,basic_info_id):
        try:
            
            query = f"DELETE FROM statuses WHERE basic_info_id = {basic_info_id}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Detail info with ID {id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting detail info: {str(e)}")
      
      
      
          
    def get_photos_by_basic_id(self, basic_id):
        try:
            query = f"SELECT * FROM photo WHERE basic_id = {basic_id}"
            self.cursor.execute(query)
            photos = self.cursor.fetchall()
            return photos
        except Exception as e:
            print(f"Error fetching photos: {str(e)}")
            return None
    def add_photo(self, basic_id, path):
        try:
            query = "INSERT INTO photo (basic_id, path) VALUES (?, ?)"
            self.cursor.execute(query, (basic_id, path))
            self.connection.commit()
            print("Photo added successfully.")
        except Exception as e:
            print(f"Error adding photo: {str(e)}")
    def delete_photo_by_path(self, path):
        try:
            query = f"DELETE FROM photo WHERE path = '{path}'"  # Добавляем одинарные кавычки вокруг переменной path
            self.cursor.execute(query)
            self.connection.commit()
            print(f"Photo with name {path} deleted successfully.")
        except Exception as e:
            print(f"Error deleting photo: {str(e)}")


    def delete_photos_by_basic_id(self, basic_id):
        try:
            query = f"DELETE FROM photo WHERE basic_id = {basic_id}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f"All photos with basic_id {basic_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting photos: {str(e)}")





  



if __name__ == "__main__":
    sql = SQL(server='DDLAPTOP\SQLEXPRESS', database='PC')
    sql.connect()
    sql.create_tables_if_not_exist()
