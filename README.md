## What's py-text-db?
It's just an attempt at creating a simple text database in Python. I am sure many other similar projects exist, this is something I am doing purely for fun.

## Ten minutes to py-text-db
Pytd is an extremely simple Python3 library to write and retrieve data to/from text files. Most of the syntax used in py-text-db is mutuated from SQL: create_table, insert_into, drop_database and so forth.

To start using py-text-db in your application you only need to drop **py_text_db.py**, **db_settings.py** and **db/** into your folder application. Once you imported pytd you can start play with your new database, for example creating and populating a *user* table:

    import py_text_db as pytd

    pytd.create_table("user", ["id", "name"," email"])

    pytd.insert_into("user", ["001", "John Bennoth", "john@example.com"])
    pytd.insert_into("user", ["002", "Bela Lugosi", "dracula@example.com"])

If you look into your db/ folder you'll see a new text file has been created, *user*. Each row represents a user with the first row representing the header of the table. Values are separeated via tabs by default (this case be changed in the db_settings.py file).

As a matter of fact, you don't need to check the db/ folder, as you have two methods to explore the database and its tables: **show_tables()** and **select_from**, see:

    for table in pytd.show_tables():
        print(table) # It prints: user

    pytd.select_from("user") # It returns the whole table without storing it

As we have not specified any *where* clause for the select_from, the whole table is returned. Tables are always returned as Pandas DataFrame.

| id | name | email |
| :------------- | :------------- | :------------- |
| 001 | John Bennoth | john@example.com |
| 002 | Bela Lugosi | dracula@example.com |

Let's populate the database some more, so that we can do more intersting stuff. We can start by creating some additional users:

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
