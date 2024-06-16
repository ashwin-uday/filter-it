import unittest
from constants import * 
from unittest import mock
from rule_parser import RuleParser
from mail_fetcher import EmailFetcher
from mail_client import GmailClient
from utils.db_utils import DBUtils

class JsonValidationTest(unittest.TestCase):
    def test_invalid_json(self):
        rule_parser = RuleParser(TEST_DATA_DIR+INVALID_JSON_STRUCTURE_FILE_NAME)
        self.assertRaises(ValueError,rule_parser.parse_rules)
    def test_invalid_keys(self):
        rule_parser = RuleParser(TEST_DATA_DIR+INVALID_JSON_KEYS_FILE_NAME)
        self.assertRaises(KeyError,rule_parser.parse_rules)
    def test_invalid_values(self):
        rule_parser = RuleParser(TEST_DATA_DIR+INVALID_JSON_VALUES_FILE_NAME)
        args = rule_parser.parse_rules()
        self.assertRaises(ValueError,rule_parser.validate_rules,*args)

@mock.patch('mail_client.GmailClient.get_message')
@mock.patch('mail_client.GmailClient.fetch_messages')
@mock.patch('mail_client.GmailClient.fetch_labels')
@mock.patch('utils.db_utils.DBUtils.fetch_ids')
@mock.patch('utils.db_utils.DBUtils.update_messages')
class MailFetchTest(unittest.TestCase):
    def test_fetch_mail_with_existing(self,*args):
        args[4].return_value = {}
        args[3].return_value = [1,2,3,4]
        args[2].return_value = ["one","two","three"]
        args[1].return_value = [1,2]
        args[0].return_value = None
        new_messages = EmailFetcher(DBUtils(),GmailClient()).fetch_emails()
        self.assertEqual(new_messages,[3,4])
    def test_fetch_mail_without_existing(self,*args):
        args[4].return_value = {}
        args[3].return_value = [1,2,3,4]
        args[2].return_value = ["one","two","three"]
        args[1].return_value = []
        args[0].return_value = None
        new_messages = EmailFetcher(DBUtils(),GmailClient()).fetch_emails()
        self.assertEqual(new_messages,[1,2,3,4])
    def test_fetch_mail_without_newids(self,*args):
        args[4].return_value = {}
        args[3].return_value = []
        args[2].return_value = ["one","two","three"]
        args[1].return_value = [1,2,3,4]
        args[0].return_value = None
        new_messages = EmailFetcher(DBUtils(),GmailClient()).fetch_emails()
        self.assertEqual(new_messages,[])


if __name__ == '__main__':
    unittest.main()