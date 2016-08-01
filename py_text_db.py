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

# TESTING
create_table("user",["name","age",])
insert_into("user",["John Benneth", "24"])

import pdb; pdb.set_trace()
