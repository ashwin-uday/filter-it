import psycopg2
import os
from utils.config import DB_CONFIG as DEFAULT_CONFIG
class DBUtils:
    def __init__(self,config=os.environ.get("db_config",DEFAULT_CONFIG)) -> None:
        self.conn = psycopg2.connect(
                        database=config["db_name"],
                        user=config["db_user"],
                        password=config["db_password"]
                    )
        self.cursor = self.conn.cursor()
        self.create_tables()
    def update_messages(self,data):
        query = """
            Insert into email(sender,receiver,subject,received_at,id) values (%s,%s,%s,%s,%s);
        """
        for row in data:
            try:
                self.cursor.execute(query,(row['From'],row['To'],row['Subject'],row['Date'],row['id']))
            except Exception as e:
                print(e)
        self.conn.commit()
    def fetch_ids(self):
        query = """
            select id from email;
        """
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(e)
        ids = self.cursor.fetchall()
        return [id[0] for id in ids]
    def create_tables(self):
        query = """
            CREATE TABLE IF NOT EXISTS email (
            sender VARCHAR NOT NULL,
            receiver VARCHAR NOT NULL,
            received_at TIMESTAMP NOT NULL,
            subject VARCHAR NOT NULL,
            id VARCHAR primary key);
        """
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(e)
    def execute_query(self,query):
        try:
            self.cursor.execute(query)
        except Exception as e:
            print(e)
        ids = self.cursor.fetchall()
        return [id[0] for id in ids]
        


        
        
            
        
    

