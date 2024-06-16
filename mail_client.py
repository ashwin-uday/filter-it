import os.path
from googleapiclient.errors import HttpError
from utils.auth import GmailAuthenticator
from constants import SCOPES,SUPPORTED_CLIENTS_MAP


class EmailClient:
    @staticmethod
    def get_client(client_type):
        # Returns the instance of the mail client if the client type is supported
        try:
            if client_type not in SUPPORTED_CLIENTS_MAP:
                raise Exception("Client not supported")
            return globals()[SUPPORTED_CLIENTS_MAP[client_type]]()
        except Exception as e:
            print(e)

class GmailClient(EmailClient):
    def __init__(self) -> None:
        auth = GmailAuthenticator(SCOPES)
        self.client = auth.init_client()
    def fetch_labels(self):
        labels = self.client.users().labels().list(userId="me").execute().get("labels",[])
        return labels
    def get_message(self,id):
        # Gets the email content and headers for a mail id. Gets called only for new emails
        # that are not in the database. 
        try:
            result = self.client.users().messages().get(userId="me",id=id).execute()
            message = result.get("snippet", [])
            labels = result["labelIds"]
            message_data = {}
            headers = result["payload"]["headers"]
            for header in headers:
                if header["name"].lower() in ["from","to","subject","date"]:
                    message_data[header["name"]] = header["value"]
            message_data["id"] = id
            message_data["labels"] = labels
            return message_data
        except HttpError as error:
            print(f"An error occurred: {error}")
    def fetch_messages(self):
        # Fetches ids of all emails which can be used to get individual emails
        try:
            results = self.client.users().messages().list(userId="me").execute()
            messages = results.get("messages", [])
            ids = [msg["id"] for msg in messages]
            return ids
        except HttpError as error:
            print(f"An error occurred: {error}")
    def update_messages(self,message_ids,addlabel_ids,removelabel_ids):
        # Updates the labels for a batch of emails to move them to and from a particular folder
        try:
            body = {
                "ids":message_ids,
                "addLabelIds":addlabel_ids,
                "removeLabelIds":removelabel_ids
            }
            self.client.users().messages().batchModify(userId="me",body=body).execute()
            print("Updated labels for ids ", message_ids)
        except HttpError as error:
            print(f"An error occurred: {error}")