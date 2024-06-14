from collections import namedtuple
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
SUPPORTED_CLIENTS_MAP = {"GMAIL": "GmailClient"}
VALID_LABELS = ["IMPORTANT", "INBOX", "STARRED"]
RULES_VALIDATION_MAP = {
    "FROM" : {
        "PREDICATE" : ["CONTAINS","NOT_EQUAL"],
        "VALUE" : lambda x: x.isalnum()
    },
    "TO" : {
        "PREDICATE" : ["CONTAINS","NOT_EQUAL"],
        "VALUE" : lambda x: x.isalnum()
    },
    "RECEIVED_AT" : {
        "PREDICATE": ["<",">"]
    }
}
FIELD_MAP = {
    "from" : "sender",
    "to" : "receiver",
    "contains" : "LIKE",
    "not contains": "NOT",
    "equal" : "=",
    "not equal": "<>",
    "less than" : ">",
    "greater than": "<",
    "date received": "received_at"
}
RuleType = namedtuple("RuleType",["name"])
Action = namedtuple("Action",["add_labels","remove_labels"])
Rule = namedtuple("Rule",["field","predicate","value"])

