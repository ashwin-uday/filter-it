import json
from constants import RuleType,Rule,Action,VALID_LABELS,RULES_VALIDATION_MAP,VALID_RULE_TYPES
from utils.query_utils import QueryBuilder
class RuleParser:
    def __init__(self,rules_file="rules.json",db_instance="",mail_client="") -> None:
        self.config = json.load(open(rules_file)) 
        self.db = db_instance
        self.mail_client = mail_client
        self.query_builder = QueryBuilder()
    def parse_rules(self):
        # Parses rules and actions, and converts them to a named tuple
        try:
            rule_type = RuleType(self.config["type"])
            rules = []
            for cur_rule in self.config["rules"]:
                rules.append(Rule(cur_rule[0],cur_rule[1],cur_rule[2]))
            add_labels = self.config["action"]["move_to"]
            remove_labels = self.config["action"]["move_from"]
            if self.config["action"]["mark_as_read"]:
                remove_labels.append("UNREAD")
            elif self.config["action"]["mark_as_unread"]:
                add_labels.append("UNREAD")
            action = Action(add_labels,remove_labels)
            return rule_type,rules,action
        except Exception as e:
            raise Exception("Error while parsing rules json ",e)
    def validate_rules(self,rule_type,rules,action):
        # Validates the rules and action for right values and associations
        if rule_type.name not in VALID_RULE_TYPES:
            raise ValueError("Rules validation failed. Invalid rule type")
        for rule in rules:
            if rule.field not in RULES_VALIDATION_MAP:
                raise ValueError("Rules validation failed. Invalid rule name {}".format(rule.field))
            if rule.predicate not in RULES_VALIDATION_MAP[rule.field]["PREDICATE"]:
                raise ValueError("Rules validation failed. Invalid predicte for field {}".format(rule.field))
        if set(action.add_labels) - set(VALID_LABELS) or set(action.remove_labels) - set(VALID_LABELS):
            raise ValueError("Rules validation failed. Invalid labels")
        
    def apply_rules(self):
        # Builds a query using the named tuples for actions and rules.
        # Execute the query to fetch the list of ids that statisfy the rule.
        try:
            print("Parsing entries from rules file...")
            rule_type,rules,action = self.parse_rules()
            print("Validating rules...")
            self.validate_rules(rule_type,rules,action)
            rule_results = []
            for rule in rules:
                query = self.query_builder.build_query(rule)
                result = self.db.execute_query(query)
                rule_results.append(result)
            # Performs a union of ids for "Any" and an intersection for "All"
            final_ids = rule_results[0]
            for res in rule_results[1:]:
                if rule_type.name == "any":
                    final_ids = set(final_ids).union(set(res))
                else:
                    final_ids = set(final_ids).intersection(set(res))
            if not final_ids:
                print("No messages found statisfying the condition")
                return
            # Applies action on the final set of ids after union/interesection
            self.mail_client.update_messages(list(final_results),action.add_labels,action.remove_labels)
        except (ValueError,Exception) as e:
            print(e)
        




        

