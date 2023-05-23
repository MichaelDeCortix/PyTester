import cx_Oracle
import re


# Oracle
def oracle_exec(query, conn_str=None, **kwargs):
    # get user, password, host, port, service_name from kwargs
    user = kwargs.get("user", None)
    password = kwargs.get("password", None)
    host = kwargs.get("host", None)
    port = kwargs.get("port", None)
    service_name = kwargs.get("service_name", None)

    # setup connection details
    patterns = [
        r"oracle://(?P<user>\w+):(?P<password>\w+)@(?P<host>[\w\.]+):(?P<port>\d+)/(?P<service_name>\w+)",
        r"jdbc:oracle:thin:(?P<user>\w+)/(?P<password>\w+)@(?P<host>[\w\.]+):(?P<port>\d+)/(?P<service_name>\w+)",
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
                service_name = kwargs.get("service_name", match_dict.get("service_name"))
                break
        else:
            raise ValueError("Invalid connection string")

    dsn = cx_Oracle.makedsn(host, port if port else "1521", service_name=service_name)

    connection = None
    cursor = None
    try:
        connection = cx_Oracle.connect(user, password, dsn)
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

    except cx_Oracle.Error as error:
        print("Error while interacting with Oracle", error)

    finally:
        # closing database connection.
        if connection is not None and cursor is not None:
            cursor.close()
            connection.close()
            print("\nOracle connection is closed")