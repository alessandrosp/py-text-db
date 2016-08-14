import os
import pandas as pd
from db_settings import *

def compare(operator, first_arg, second_arg):
    """It compares first_arg against second_arg using operator."""

    # Match the right operator to the right operation
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

def show_tables():
    """It returns all the table names as a list."""
    return os.listdir(db_name+"/")

def does_table_exist(table_name):
    """Return True if table exists, False otherwise."""
    return table_name in show_tables()

def check_number_columns(table_name):
    """It returns the number of columns for the table."""

    location = db_name+"/"+table_name
    with open(location, "r") as table:
        header = table.readline().strip("\n").split(delimeter)
        print(header)
        n_columns = len(header)
    return n_columns

def create_table(table_name, header_or_values, overwrite = False):
    """It creates a new table using."""

    # Check whether table exists
    if (does_table_exist(table_name) and overwrite == False):
        raise NameError("A table with that name already exists")
    else:
        location = db_name+"/"+table_name

        # If just the header has been passed (list)
        if isinstance(header_or_values, list):
            # Create the header
            header = ""
            for field in header_or_values:
                if field == header_or_values[-1]:
                    header += field
                else:
                    header += field+delimeter

            # The table is created and the header written
            with open(location, "w+") as table:
                table.write(header+"\n")

        # If Pandas DataFrame
        elif isinstance(header_or_values, pd.DataFrame):
            pass

        return None

def insert_into(table_name, values):
    """It inserts one or more new rows into table_name table"""

    # Check whether table exists
    if not does_table_exist(table_name):
        raise NameError("The table specified does not exist")

    # The location of the table
    location = db_name+"/"+table_name

    # If single row as list
    if isinstance(values, list):
        # Validate the list is the proper length
        if not check_number_columns(table_name) == len(values):
            raise ValueError("Input data do not match table columns")

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
        # Validate the DataFrame is the proper shape
        if not check_number_columns(table_name) == values.shape[1]:
            raise ValueError("Input data do not match table columns")

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

    # Check wether table exists
    if not does_table_exist(table_name):
        raise NameError("The table specified does not exist")

    os.remove(db_name+"/"+table_name)

    return None

def drop_database():
    """Use with caution: it deletes every table in the database."""

    for table in show_tables():
        drop_table(table)

    return None

def select_from(table_name, columns = [], where = None):
    """It returns one or more rows from the selected table."""

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

    # Select the columns to return
    if columns:
        results = results[columns]

    return results

def join(left_table, right_table, type = "inner", on = None):
    """It joins two tables."""
    return pd.merge(left_table, right_table, how = type, on = on)
