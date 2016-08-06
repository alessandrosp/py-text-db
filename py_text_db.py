import os
import pandas as pd
from db_settings import *

# TODO(alessandrosp): Function to show all tables
# TODO(alessandrosp): Inner joins between tables

def compare(operator, first_arg, second_arg):
    """It compares first_arg against second_arg using operator."""
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
    # TODO(alessandrosp): Allows to create a table + inserting using DataFrame
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

def insert_into(table_name, values):
    """It inserts one or more new rows into table_name table"""
    # TODO(alessandrosp): Validate values match fields

    # The location of the table
    location = db_name+"/"+table_name

    # If single row as list
    if isinstance(values, list):
        # Create the row to insert into the table
        delimited_row = ""
        for element in values:
            if element == values[-1]: # Last element
                delimited_row += element
            else: # Not last element
                delimited_row += element+delimeter

        # Insert the row
        with open(location, "a") as table:
            table.write(delimited_row+"\n")

    # If Pandas DataFrame
    elif isinstance(values, pd.DataFrame):
        # For each row in the DataFrame...
        for row in values.iterrows():
            delimited_row = ""
            # ...We iterate through the individual elements...
            for index_element in range(row[1].shape[0]):
                # ...And we concatenate the elements into a row
                if index_element == (row[1].shape[0])-1: # Last element
                    delimited_row += row[1][index_element]
                else: # Not last element
                    delimited_row += row[1][index_element]+delimeter

            # Insert the row into the table
            with open(location, "a") as table:
                table.write(delimited_row+"\n")

    else:
        raise ValueError("Input data must be list or Pandas DataFrame")

    return None

def drop_table(table_name):
    """It drops (i.e. deletes) the specified table."""
    os.remove(db_name+"/"+table_name)

    return None

def drop_database():
    """Use with caution: it deletes every table in the database."""
    tables = os.listdir(db_name+"/")
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
                        # All where clauses must be met for row to be returned
                        if count_match == len(where.keys()):
                            results_list.append(values)

        # Results are converted to a Pandas DataFrame
        results = pd.DataFrame(results_list,
                               columns = header)


    # If no where clause was specified all rows are returned
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

def show_tables():
    """It returns all the table names as a list."""
    return os.listdir(db_name+"/")

def join(left_table, right_table, type = "inner"):
    """It joins two tables."""
    return pd.merge(left_table, right_table, how = type)
