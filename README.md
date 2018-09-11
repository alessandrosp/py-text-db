## What's py-text-db?
It's just an attempt at creating a simple text database in Python. I am sure similar projects exist, this is something I am doing mostly for fun. Feedback is always welcome!

## Ten minutes to py-text-db
### Installation
Pytd is an extremely simple Python 3 library to write and retrieve data from text files. Most of the syntax mutuated from SQL: create_table, insert_into, drop_database, to name a few. To start using py-text-db in your application you only need to drop three files - **py_text_db.py**, **db_settings.py** and the directory **db/** - into your folder application.

### Create and select from tables
 Once you imported pytd, you can start play with your new database; you can use the **create_table()** and **insert_into()** functions to create and populate a *user* table:

    import py_text_db as pytd

    pytd.create_table("user", ["id", "name"," email"])

    pytd.insert_into("user", ["001", "John Bennoth", "john@example.com"])
    pytd.insert_into("user", ["002", "Bela Lugosi", "dracula@example.com"])

If you look into your db/ folder you will see that a new text file has been created, *user*. The first row represents the header and each additional row represents a user. Values are separeated via tabs by default (this can be easily changed in the db_settings.py file).

As a matter of fact, you do not need to check the db/ folder directly, as you have two methods to explore the database and its tables: **show_tables()** and **select_from()**, see:

    for table in pytd.show_tables():
        print(table) # It prints: 'user'

    pytd.select_from("user") # It returns the whole table

As we have not specified any *columns* or *where* clause for the select_from(), the whole table is returned. Tables are always returned as Pandas DataFrame.

| id | name | email |
| :------------- | :------------- | :------------- |
| 001 | John Bennoth | john@example.com |
| 002 | Bela Lugosi | dracula@example.com |

Let's populate the database some more, so that we can do more interesting stuff. We can start by creating some additional users:

    pytd.insert_into("user", ["003", "Claude Shannon", "entropy@example.com"])
    pytd.insert_into("user", ["004", "Alan Turing", "machine@example.com"])

Now we can select_from again, this time specyfing some where clauses. Where clauses are simple conditions that tell the database which rows to return. For a row to be returned it must met all conditions. We can start with a simple example:

    pytd.select_from("user",
                     where = {"name": ["=", "Alan Turing"]})

Will return a one-row table, as there's only one user who goes by the name *Alan Turing*.

| id | name | email |
| :------------- | :------------- | :------------- |
| 004 | Alan Turing | machine@example.com |

We can use all simple logic operations (=, !=, >, >=, <, <=) as part of a where clause. For example we may want to look at all users with *id* lower than 004.

    pytd.select_from("user",
                     where = {"id": ["<", "004"]}) # Note: everything's a string!

This will return the following DataFrame:

| id | name | email |
| :------------- | :------------- | :------------- |
| 001 | John Bennoth | john@example.com |
| 002 | Bela Lugosi | dracula@example.com |   
| 003 | Claude Shannon | entropy@example.com |           

Lastly, we can use as many where clauses as we want, for example we may want to look at all users who name start with A, B or C whose email address begins with a letter higher or equal than "e", see:

    pytd.select_from("user",
                     where = {"name": ["<", "D"],
                              "email": [">=", "e"]})

Which will return the last two rows of our dummy database:

| id | name | email |
| :------------- | :------------- | :------------- |
| 003 | Claude Shannon | entropy@example.com |
| 004 | Alan Turing | machine@example.com |

### Create and insert from DataFrame, joins
So far we have been inserting and creating table starting from lists. We can however also use Pandas DataFrame for the purpose. As we said select_from() does return a DataFrame, so if you want to create a backup table for our *user* table we can simply do:

    users = pytd.select_from("user") # Users is a DataFrame containins all the users
    pytd.create_table("user_backup", users)

Now we have a new table (aka, text file) that is a copy of our *user* table. The same logic also applies to insert_into(), so that the following commands are indentical to the previous ones:

    pytd.create_table("user_backup", ["id", "name"," email"]) # Create a backup table
    pytd.insert_into("user_backup", select_from("user"))

Lastly, we can also join two table SQL-style using the **join()** function. Imagining we have a table *name* containing only the user names:

| id | name |
| :------------- | :------------- |
| 001 | John Bennoth |
| 002 | Bela Lugosi |
| 003 | Claude Shannon |
| 004 | Alan Turing |

And one *email* containing only the email addresses:

| id | email |
| :------------- | :------------- |
| 001 | john@example.com |
| 002 | dracula@example.com |   
| 003 | entropy@example.com |  
| 004 | machine@example.com |

You can create a new table containing both by doing:

    names = pytd.select_from("name")
    emails = pytd.select_from("email")
    names_and_emails = pytd.join(names, emails, on = "id") # As always, case sensitive
    pytd.create_table("user", names_and_emails)

Which is going to contain all the information:

| id | name | email |
| :------------- | :------------- | :------------- |
| 001 | John Bennoth | john@example.com |
| 002 | Bela Lugosi | dracula@example.com |   
| 003 | Claude Shannon | entropy@example.com |
| 004 | Alan Turing | machine@example.com |

### Drop and delete
You have two functions to delete tables when you don't need them anymore: drop_table() and drop_database(). The former deletes a table, the latter the whole database. Let's imagine we have three tables, *user*, *product* and *location*:

    pytd.show_tables() # Returns ['user', 'product', 'location']
    pytd.drop_table("product")
    pytd.show_tables() # Returns ['user', 'location']
    pytd.drop_database()
    pytd.show_tables() # Returns ['']
