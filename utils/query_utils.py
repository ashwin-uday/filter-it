from constants import FIELD_MAP


class QueryBuilder:
    def __init__(self) -> None:
        self.field_map = FIELD_MAP

    def build_query(self, rule):
        raw_query = """
            select id from email where {} {} {};
        """
        updated_value = ""
        if "date" in rule.field.lower():
            days = False
            value = int(rule.value[:-1])
            if rule.value.endswith("D"):
                days = True 
            metric = "day" if days else "month"
            updated_value = "now() - interval '{} {}'".format(value,metric)
        query = raw_query.format(
            self.field_map[rule.field],
            self.field_map[rule.predicate],
            rule.value if not updated_value else updated_value
        )
        print(query)
        return query
