import re
from sqlparse import parse, format

def format_sql_code(sql_code):
    keywords = ['SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'GROUP BY', 'HAVING', 'ORDER BY', 'LIMIT', 'OFFSET']
    try:
        parsed = parse(sql_code)[0]
    except Exception as e:
        return e
    for token in parsed.tokens:
        if token.ttype is None:
            # Capitalize keywords
            for keyword in keywords:
                token.value = re.sub(keyword, keyword.upper(), token.value)
            # Convert snake_case to camelCase
            token.value = re.sub('(?<!^)(_)([a-zA-Z])', lambda x: x.group(2).upper(), token.value)
    # Use the sqlparse.format() function to format the indentation
    formatted_sql = format(str(parsed), reindent=True)
    print(formatted_sql)


sql = """

"""
format_sql_code(sql)