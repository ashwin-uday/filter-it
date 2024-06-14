from utils.db_utils import DBUtils
from mail_client import EmailClient
from constants import VALID_LABELS

class EmailFetcher:
    def __init__(self,db_instance=None,mail_client=None) -> None:
        self.client = mail_client
        self.db = db_instance
    def fetch_emails(self):
        labels = self.client.fetch_labels()
        ids = self.client.fetch_messages()
        # Ignore existing emails from db and fetch only new emails via Gmail API
        existing_ids = self.db.fetch_ids()
        new_ids = list(set(ids) - set(existing_ids))
        new_data = []
        for id in new_ids:
            message_data = self.client.get_message(id)
            new_data.append(message_data)
        self.db.update_messages(new_data)
    def filter_emails(self,ids,target_label):
        self.client.update_messages(ids,[target_label],[])