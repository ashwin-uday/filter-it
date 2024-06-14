import json
from constants import RuleType,Rule,Action
from utils.query_utils import QueryBuilder
class RuleUtils:
    def __init__(self,rules_file="rules.json",mail_client="",db_instance="") -> None:
        self.config = json.load(open(rules_file)) 
        self.db = db_instance
        self.mail_client = mail_client
        self.query_builder = QueryBuilder()
    def parse_rules(self):
        rule_type = RuleType(self.config["type"])
        rules = []
        for cur_rule in self.config["rules"]:
            rules.append(Rule(cur_rule[0],cur_rule[1],cur_rule[2]))
        add_labels = self.config["action"]["move_to"]
        remove_labels = []
        if self.config["action"]["mark_as_read"]:
            remove_labels.append("UNREAD")
        elif self.config["action"]["mark_as_unread"]:
            add_labels.append("UNREAD")
        action = Action(add_labels,remove_labels)
        return rule_type,rules,action
    def apply_rules(self):
        rule_type,rules,action = self.parse_rules()
        rule_results = []
        for rule in rules:
            query = self.query_builder.build_query(rule)
            result = self.db.execute_query(query)
            rule_results.append(result)
        final_results = rule_results[0]
        for res in rule_results[1]:
            if rule_type.name == "any":
                final_results = set(final_results).union(set(res))
            else:
                final_results = set(final_results).intersection(set(res))
        self.mail_client.update_messages(list(final_results),action.add_labels,action.remove_labels)
        

def main():
    ru = RuleUtils()
    ru.apply_rules()
if __name__ == "__main__":
    main()




        

