import psycopg2
import re


# PostgreSQL
def postgre_exec(query, jdbc=None, **kwargs):
    # get user, password, host, port, database from kwargs
    user = kwargs.get("user", None)
    password = kwargs.get("password", None)
    host = kwargs.get("host", None)
    port = kwargs.get("port", None)
    database = kwargs.get("database", None)

    # if jdbc string is provided, extract connection details from it
    if jdbc is not None:
        match = re.match(
            # r"jdbc:postgresql://(?P<host>[\w\.]+):(?P<port>\d+)/(?P<database>\w+)\?user=(?P<user>\w+)&password=(?P<password>\w+)",
            r"jdbc:postgresql://(?P<host>[\w\.]+):(?P<port>\d+)/(?P<database>\w+)(\?user=(?P<user>\w+)&password=(?P<password>\w+))?",
            jdbc,
        )
        if match:
            # update only the values that are not already set in kwargs
            match_dict = match.groupdict()
            user = kwargs.get("user", match_dict.get("user"))
            password = kwargs.get("password", match_dict.get("password"))
            host = kwargs.get("host", match_dict.get("host"))
            port = kwargs.get("port", match_dict.get("port"))
            database = kwargs.get("database", match_dict.get("database"))
        else:
            raise ValueError("Invalid JDBC connection string")

    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            # if port exists use it, else use default
            port=port if port else "5432",
            database=database,
        )
        cursor = connection.cursor("back_tester")
        cursor.execute(query)
        cursor_data = cursor.fetchall()

        print(cursor_data)
        return cursor_data

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection is not None and cursor is not None:
            cursor.close()
            connection.close()
            print("\nPostgreSQL connection is closed")