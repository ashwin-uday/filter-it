from utils.db_utils import DBUtils
from mail_fetcher import EmailFetcher
from rule_parser import RuleParser
from mail_client import EmailClient
from constants import DEFAULT_RULES_FILENAME

DB_INSTANCE = DBUtils()
MAIL_CLIENT = EmailClient.get_client("GMAIL")


def main():
    # Fetch new emails and store them to database
    email_fetcher = EmailFetcher(DB_INSTANCE,MAIL_CLIENT)
    email_fetcher.fetch_emails()
    # Parse rules file, apply rules and perform action(s)
    rule_parser = RuleParser(DEFAULT_RULES_FILENAME,DB_INSTANCE,MAIL_CLIENT)
    rule_parser.apply_rules()

if __name__ == "__main__":
    main()