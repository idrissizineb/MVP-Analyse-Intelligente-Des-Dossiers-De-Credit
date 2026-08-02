from app.text2sql.sql_validator import SQLValidator


validator = SQLValidator()


queries = [

    "SELECT * FROM client",

    "DELETE FROM client",

    "DROP TABLE client",

    "SELECT * FROM sqlite_master",

    "SELECT * FROM client; DELETE FROM client",

]


for query in queries:

    valid, reason = validator.validate(query)

    print()

    print(query)

    print("Valid :", valid)

    print("Reason:", reason)