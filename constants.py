from collections import namedtuple

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
SUPPORTED_CLIENTS_MAP = {"GMAIL": "GmailClient"}
FIELD_MAP = {
    "FROM": "sender",
    "TO": "receiver",
    "CONTAINS": "LIKE",
    "NOT CONTAINS": "NOT LIKE",
    "EQUAL": "=",
    "NOT EQUAL": "<>",
    "LESS THAN": ">",
    "GREATER THAN": "<",
    "DATE RECEIVED": "received_at",
    "SUBJECT": "subject"
}
RuleType = namedtuple("RuleType", ["name"])
Action = namedtuple("Action", ["add_labels", "remove_labels"])
Rule = namedtuple("Rule", ["field", "predicate", "value"])
DEFAULT_RULES_FILENAME = "rules.json"

# Constants for validation
VALID_LABELS = ["IMPORTANT", "INBOX", "STARRED", "UNREAD"]
RULES_VALIDATION_MAP = {
    "FROM": {"PREDICATE": ["CONTAINS", "NOT EQUAL","NOT CONTAINS","EQUAL"]},
    "TO": {"PREDICATE": ["CONTAINS", "NOT EQUAL","NOT CONTAINS","EQUAL"]},
    "SUBJECT": {"PREDICATE": ["CONTAINS", "NOT EQUAL","NOT CONTAINS","EQUAL"]},
    "DATE RECEIVED": {"PREDICATE": ["LESS THAN", "GREATER THAN"]}
}
VALID_RULE_TYPES = ["ALL","ANY"]

# Test constants
TEST_DATA_DIR = "tests/data/"
# Rules json tests
INVALID_JSON_STRUCTURE_FILE_NAME = "invalid_file.json"
INVALID_JSON_KEYS_FILE_NAME = "invalid_keys.json"
INVALID_JSON_VALUES_FILE_NAME = "invalid_values.json"




