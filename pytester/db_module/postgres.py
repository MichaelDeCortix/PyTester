import psycopg2
import re


# PostgreSQL
def postgre_exec(query, conn_str=None, **kwargs):
    # get user, password, host, port, database from kwargs
    user = kwargs.get("user", None)
    password = kwargs.get("password", None)
    host = kwargs.get("host", None)
    port = kwargs.get("port", None)
    database = kwargs.get("database", None)

    # setup connection details
    patterns = [
        r"postgresql://(?P<user>[^:]*):(?P<password>[^@]*)@(?P<host>[^:]*):(?P<port>\d+)/(?P<database>.*)",
        r"jdbc:postgresql://(?P<host>[^:]*):(?P<port>\d+)/(?P<database>.*)(\?user=(?P<user>[^&]*)&password=(?P<password>.*))?",
        r"postgres://(?P<user>[^:]*):(?P<password>[^@]*)@(?P<host>[^:]*):(?P<port>\d+)/(?P<database>.*)"
    ]

    # if a connection string is provided, extract connection details from it
    if conn_str is not None:
        for pattern in patterns:
            match = re.match(pattern, conn_str)
            if match:
                # update only the values that are not already set in kwargs
                match_dict = match.groupdict()
                user = kwargs.get("user", match_dict.get("user"))
                password = kwargs.get("password", match_dict.get("password"))
                host = kwargs.get("host", match_dict.get("host"))
                port = kwargs.get("port", match_dict.get("port"))
                database = kwargs.get("database", match_dict.get("database"))
                break
        else:
            raise ValueError("Invalid connection string")

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
        cursor = connection.cursor()

        # check the type of SQL command
        if query.strip().upper().startswith("SELECT"):
            cursor.execute(query)
            cursor_data = cursor.fetchall()
            print(cursor_data)
            return cursor_data
        elif query.strip().upper().startswith(("UPDATE", "DELETE")):
            cursor.execute(query)
            connection.commit()
            rows_affected = cursor.rowcount
            print(f"{rows_affected} rows affected.")
            return rows_affected
        else:
            raise ValueError(f"Unsupported SQL command in query: {query}")

    except (Exception, psycopg2.Error) as error:
        print("Error while interacting with PostgreSQL", error)

    finally:
        # closing database connection.
        if connection is not None and cursor is not None:
            cursor.close()
            connection.close()
            print("\nPostgreSQL connection is closed")
