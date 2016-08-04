import os
import pandas as pd
from db_settings import *

def compare(operator, first_arg, second_arg):
    if operator == "=":
        return first_arg == second_arg
    elif operator == "!=":
        return first_arg != second_arg
    elif operator == ">":
        return first_arg > second_arg
    elif operator == ">=":
        return first_arg >= second_arg
    elif operator == "<":
        return first_arg < second_arg
    elif operator == "<=":
        return first_arg <= second_arg
    else:
        raise ValueError("No valid operator was specified")

def create_table(table_name, fields):
    """It creates a table using *fields* as header."""
    # TODO(alessandrosp): Validate *fields*
    # TODO(alessandrosp): Check whether table exists, in case returns error,
    #                     unless a overwrite is set to True
    # Note: Currently if a table with the same exists it's over-written
    location = db_name+"/"+table_name

    # Create the header
    header = ""
    for field in fields:
        if field == fields[-1]:
            header += field
        else:
            header += field+delimeter

    # The table is created and the header written
    with open(location, "w+") as table:
        table.write(header+"\n")

    return None

def insert_into(table_name, row):
    """It inserts a new row into table_name table"""
    # TODO(alessandrosp): Validate row match fields
    # The location of the table
    location = db_name+"/"+table_name

    # Create the row to insert into the table
    delimited_row = ""
    for element in row:
        if element == row[-1]:
            delimited_row += element
        else:
            delimited_row += element+delimeter

    # Insert the row
    with open(location, "a") as table:
        table.write(delimited_row+"\n")

    return None

def drop_table(table_name):
    """It drops (i.e. deletes) the specified table."""
    os.remove(db_name+"/"+table_name)

    return None

def drop_database():
    """Use with caution: it deletes every table in the database."""
    db_location = os.path.dirname(os.path.abspath(__file__))+"/"+db_name
    tables = os.listdir(db_location)
    for table in tables:
        drop_table(table)

    return None

def select_from(table_name, where = None):
    """It returns one or more rows from the selected table."""
    # TODO(alessandrosp): Specify which columns to return

    # The location of the table
    location = db_name+"/"+table_name

    # Initialise results as a list
    results_list = []

    # Check whether a where clause was specified
    if where:
        # TODO(alessandrosp): Implement where clause
        # e.g. where = {"name": ["=","John Benneth"]}
        # e.g. where = {"age": [">","25"]}
        # e.g. where = {"name": ["!=","Cat Stevens"],
        #               "age": ["<","50"]}

        first_row = True
        with open(location, "r") as table:
            for row in table:
                if first_row:
                    header = row.strip("\n").split(delimeter)
                    first_row = False
                elif not first_row:
                    values = row.strip("\n").split(delimeter)
                    count_match = 0
                    for key in where.keys():
                        if compare( operator = where[key][0],
                                    first_arg = values[header.index(key)],
                                    second_arg = where[key][1]):
                            count_match += 1
                        if count_match == len(where.keys()):
                            results_list.append(values)

        # Results are converted to a Pandas DataFrame
        results = pd.DataFrame(results_list,
                               columns = header)


    # If no where was specified all rows are returned
    else:
        # Results are written into a list of lists first
        with open(location, "r") as table:
            for row in table:
                values = row.strip("\n").split(delimeter)
                results_list.append(values)

        # Results are converted to a Pandas DataFrame
        results = pd.DataFrame(results_list[1:],
                               columns = results_list[0])

    return results

# TESTING
if __name__ == "__main__":
    create_table("user",["name","age",])
    insert_into("user",["John Benneth", "24"])
    insert_into("user",["Adriano Meis", "31"])
    insert_into("user",["Nicholas Corbyn", "53"])
    insert_into("user",["Jonathan Redsmith", "18"])
    test1 = select_from("user", where = {"name": ["=","John Benneth"]})
    test2 = select_from("user", where = {"name": [">=","B"]})
    test3 = select_from("user", where = {"age": ["!=","18"]})
    test4 = select_from("user", where = {   "name": ["<=","L"],
                                            "age": [">","20"]})

    import pdb; pdb.set_trace()
