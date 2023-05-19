import cx_Oracle
import re


# Oracle
def oracle_exec(query, jdbc=None, **kwargs):
    # get user, password, host, port, database from kwargs
    user = kwargs.get("user", None)
    password = kwargs.get("password", None)
    host = kwargs.get("host", None)
    port = kwargs.get("port", None)
    service_name = kwargs.get("service_name", None)
    
    # if jdbc string is provided, extract connection details from it
    if jdbc is not None:
        match = re.match(
            r"jdbc:oracle:thin:(?P<user>\w+)/(?P<password>\w+)@(?P<host>[\w\.]+):(?P<port>\d+)/(?P<service_name>\w+)",
            jdbc,
        )
        if match:
            # update only the values that are not already set in kwargs
            match_dict = match.groupdict()
            user = kwargs.get("user", match_dict.get("user"))
            password = kwargs.get("password", match_dict.get("password"))
            host = kwargs.get("host", match_dict.get("host"))
            port = kwargs.get("port", match_dict.get("port"))
            service_name = kwargs.get("service_name", match_dict.get("service_name"))
        else:
            raise ValueError("Invalid JDBC connection string")

    dsn = cx_Oracle.makedsn(host, port if port else "1521", service_name=service_name)
    connection = None
    cursor = None
    try:
        connection = cx_Oracle.connect(user, password, dsn)
        cursor = connection.cursor("back_tester")
        cursor.execute(query)
        cursor_data = cursor.fetchall()

        print(cursor_data)
        return cursor_data

    except cx_Oracle.Error as error:
        print("Error while fetching data from Oracle", error)

    finally:
        # closing database connection.
        if connection is not None and cursor is not None:
            cursor.close()
            connection.close()
            print("\nOracle connection is closed")
