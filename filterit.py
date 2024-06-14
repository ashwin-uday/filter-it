from utils.db_utils import DBUtils
from filter import EmailFetcher
from rules import RuleUtils
from mail_client import EmailClient
def main():
    db = DBUtils()
    mail_client = EmailClient().get_client()
    email_fetcher = EmailFetcher(db,mail_client)
    email_fetcher.fetch_emails()
    ru = RuleUtils("rules.json",db,mail_client)
    ru.apply_rules()
if __name__ == "__main__":
    main()