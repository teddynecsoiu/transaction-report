import sys
import sqlite3
import csv
from uuid import UUID, uuid4
import datetime

CSV_FILE_PATH = './seed/backend-exercise-data.csv'
DB_FILE_PATH = 'transactions.sqlite'

def open_csv_file(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        data = list()
        for row in reader:
            data.append(row)

        return data

def validate_date(date_text: str):
    if not isinstance(date_text, str):
        raise TypeError

    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD.")

def validate_id(customer_id: str):
    try:
        UUID(customer_id).version
    except ValueError:
        raise ValueError("Incorrect data format, string should be valid UUID.")

def create_connection(db_file):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(db_file)
        cursor = sqlite_connection.cursor()
        print("Successfully Connected to SQLite.")
        return sqlite_connection

    except sqlite3.Error as error:
        print("Error while connecting to sqlite.", error)

        if sqlite_connection is not None:
            sqlite_connection.close()
            print("The SQLite connection is closed.")


def create_transactions_table():
    sqlite_connection = create_connection(DB_FILE_PATH)
    try:
        cursor = sqlite_connection.cursor()
        print("Successfully Connected to SQLite.")

        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS transactions
                                    (id TEXT PRIMARY KEY, date DATE, expense_type TEXT, 
                                    amount BOOL, account_id TEXT)'''
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("SQLite table created.")

        sqlite_create_index_query = '''CREATE INDEX IF NOT EXISTS idx_user_daily
                                    ON transactions (account_id, date)'''
        cursor.execute(sqlite_create_index_query)
        sqlite_connection.commit()
        print("SQLite index created.")

        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table.", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("The SQLite connection is closed.")

def insert_multipe_records(recordList):
    sqlite_connection = create_connection(DB_FILE_PATH)
    try:
        cursor = sqlite_connection.cursor()
        print("Connected to SQLite")

        sqlite_insert_query = 'INSERT INTO transactions VALUES (?, ?, ?, ?, ?);'
        cursor.executemany(sqlite_insert_query, recordList)
        sqlite_connection.commit()
        cursor.close()
        print("Total", cursor.rowcount, "Records inserted successfully into transactions table.")

    except sqlite3.Error as error:
        print("Failed to insert multiple records into sqlite table.", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("The SQLite connection is closed.")

def get_transaction_breakdown(customer_id, start_date = None, end_date = None):
    sqlite_connection = create_connection(DB_FILE_PATH)
    try:
        validate_id(customer_id)
        argument_list = [customer_id]
        sqlite_query = '''SELECT account_id, expense_type, ROUND(SUM(amount),
                        2) AS breakdown, COUNT(id) AS sum FROM transactions t2
                        WHERE account_id = ? '''

        if isinstance(start_date, str):
            validate_date(start_date)
            argument_list.append(start_date)
            sqlite_query = sqlite_query + 'AND  date >= ? '

        if isinstance(end_date, str):
            validate_date(end_date)
            argument_list.append(end_date)
            sqlite_query = sqlite_query + 'AND  date <= ? '

        sqlite_query = sqlite_query + 'GROUP BY account_id, expense_type;'


        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_query, argument_list)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    except sqlite3.Error as error:
        print("Failed to fetch the account ID transaction breakdown.", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("The SQLite connection is closed.")

def delete_transaction(transaction_id):
    sqlite_connection = create_connection(DB_FILE_PATH)
    try:
        validate_id(transaction_id)
        sqlite_query = '''DELETE from transactions where id = ?'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_query, (transaction_id, ))
        sqlite_connection.commit()
        print("Transaction deleted successfully")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from the transactions table.", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("The SQLite connection is closed.")

def insert_transaction(account_id, date, expense_type, amount):
    sqlite_connection = create_connection(DB_FILE_PATH)
    try:
        validate_id(account_id)
        validate_date(date)
        record_id = str(uuid4())
        value_tuple = (record_id, date, account_id, expense_type, amount)
        sqlite_query = '''INSERT INTO transactions (id, date, account_id,
                        expense_type, amount) VALUES (?, ?, ?, ?, ?)'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_query, value_tuple)
        sqlite_connection.commit()
        cursor.close()
        return record_id

    except sqlite3.Error as error:
        print("Failed to insert transaction record.", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("The SQLite connection is closed.")

def db_init():
    create_transactions_table()
    data = open_csv_file(CSV_FILE_PATH)
    insert_multipe_records(data)
