import psycopg2
import os,json
from utils.config import DB_CONFIG as DEFAULT_CONFIG

# fetch username and password from environment, if not present use default config
ENV_CONFIG = json.loads(os.environ.get("DB_CONFIG","{}"))
if not ENV_CONFIG:
    ENV_CONFIG = DEFAULT_CONFIG
ENV = os.environ.get("ENV","DEV")
CONFIG = ENV_CONFIG[ENV]

class DBUtils:
    def __init__(self) -> None:
        self.conn = psycopg2.connect(
                        database=CONFIG["db_name"],
                        user=CONFIG["db_user"],
                        password=CONFIG["db_password"]
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
        


        
        
            
        
    

