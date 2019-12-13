"""
This file contains helper methods that gets data from the database
"""

import sqlite3
from sqlite3 import Error


def get_all_decks_of_commander(commander):
    """
    Takes in a string of a commander's name then searches the database for every deck that contains
    that commander and returns it as
    :param commander: A string of the commander's name to be searched
    :return: An sql cursor that contains all the decks of the commander
    """

    con = sql_connection()
    crs = con.cursor()
    decks = crs.execute("""SELECT * FROM (
    SELECT deckID, cardName, mana_cost, type_line, color_identity
        FROM decks
        INNER JOIN cards ON decks.cardName = cards.name
        )a
        INNER JOIN commander ON commander.deckID = a.deckID
        WHERE commander.commanderName = '%s'""" % commander)
    con.commit()
    print(type(decks))
    return decks


def sql_connection():
    """
    Connects to the database and returns a connection object as long as
    no errors are encountered
    :return: A sql connection object
    """

    try:
        con = sqlite3.connect('DeckDB.db')
        return con
    except Error:
        print(Error)


def create_decks():
    """
    Creates the decks table in the database unless there is a table already
    called decks then it deletes the table and makes a fresh one
    :return: None
    """

    con = sql_connection()
    crs = con.cursor()
    crs.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='decks'")
    if crs.fetchone()[0] != 1:
        crs = con.cursor()
        crs.execute("CREATE TABLE decks(cardName text, deckID integer)")
        con.commit()
    else:
        crs = con.cursor()
        crs.execute("DROP TABLE decks")
        crs.execute("CREATE TABLE decks(cardName text, deckID integer)")
        con.commit()
    con.close()


def create_commander():
    """
    Creates the commander table in the database unless there is a table already
    called decks then it deletes the table and makes a fresh one
    :return: None
    """

    con = sql_connection()
    crs = con.cursor()
    crs.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='commander'")
    if crs.fetchone()[0] != 1:
        crs = con.cursor()
        crs.execute("CREATE TABLE commander(commanderName text, deckID integer)")
        con.commit()
    else:
        crs = con.cursor()
        crs.execute("DROP TABLE commander")
        crs.execute("CREATE TABLE commander(commanderName text, deckID integer)")
        con.commit()
    con.close()


def get_all_table(table_name):
    """
    Gets all the rows from a given table and returns a cursor object containing all the entries
    :param table_name: A string of the table to be pulled from
    :return: A cursor object containing all the rows
    """

    con = sql_connection()
    crs = con.cursor()
    rows = crs.execute("SELECT * FROM %s" % table_name)
    con.commit()
    return rows
