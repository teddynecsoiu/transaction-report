import logging
import csv
from db_utils import create_connection, create_transactions_table, insert_multipe_records

# Both these values should either be passed as command line parameters
# or be handled by a packate like python-dotenv...
CSV_FILE_PATH = './seed/backend-exercise-data.csv'
DB_FILE_PATH = 'transactions.sqlite'

# This loads the entire CSV file in memeory
# It could be improved either with streaming or using the pandas package and
# load the file in chunks
def open_csv_file(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        data = list()
        for row in reader:
            data.append(row)

        return data

if __name__ == '__main__':
    # This will simply generate the inital db/table and 
    # seed it using the CSV however a package like Alembic
    # could be used to manage actual migration
    try:
        sqlite_connection = create_connection(DB_FILE_PATH)
        create_transactions_table(sqlite_connection)

        data = open_csv_file(CSV_FILE_PATH)
        insert_multipe_records(sqlite_connection, data)

    except sqlite3.Error as error:
        # This is not enough since there are several stages that could fail
        logging.error("Part of initialization failed", error)

    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            logging.info("The SQLite connection is closed.")

