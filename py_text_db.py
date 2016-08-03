import os
from db_settings import *

def create_table(table_name, fields):
    """It creates a table using *fields* as header."""
    # TODO(alessandrosp): Validate *fields*
    # TODO(alessandrosp): Check whether table exists, in case returns error
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
    # TODO(alessandrosp): Use Pandas instead of list of lists
    # TODO(alessandrosp): Implement where clause
    # Initilise results
    results = []

    # Check whether a where clause was specified
    if where:
        pass
    # If no where was specified all rows are returned
    else:
        # The location of the table
        location = db_name+"/"+table_name

        with open(location, "r") as table:
            for row in table:
                results.append(row.strip("\n").split(delimeter))

    return results

# TESTING
create_table("user",["name","age",])
insert_into("user",["John Benneth", "24"])
insert_into("user",["Adriano Meis", "31"])
test = select_from("user")

import pdb; pdb.set_trace()
