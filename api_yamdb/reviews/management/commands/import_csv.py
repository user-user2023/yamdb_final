import csv
import logging
import sqlite3
from django.core.management.base import BaseCommand, CommandError
from api_yamdb.settings import BASE_DIR, STATICFILES_DIRS


CSV_FILES_DIR = f"{STATICFILES_DIRS[0]}/data"
FILES_DICT = {
    "titles": "reviews_title",
    "category": "reviews_category",
    "comments": "reviews_comments",
    "genre_title": "reviews_title_genre",
    "genre": "reviews_genre",
    "review": "reviews_review",
    "users": "users_user"
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def read_db(prefix):
    """Function for read data from db table."""
    db_table = FILES_DICT[prefix]
    con = sqlite3.connect(f"{BASE_DIR}/db.sqlite3")
    cur = con.cursor()
    cur.execute(f'''
    SELECT *
    FROM {db_table};
    ''')
    logging.info(f"Trying to read data from {db_table}")
    if cur:
        logging.info(f'Successfully read db table {db_table}')
        db_column_names = tuple(i[0] for i in cur.description)
        print(f"Данные в таблице - {db_table}:")
        print(db_column_names)
        return cur


def write_to_db(filename, prefix):
    """Function for write data from csv to db table."""
    db_table = FILES_DICT[prefix]
    con = sqlite3.connect(f"{BASE_DIR}/db.sqlite3")
    cur = con.cursor()
    with open(
            f'{CSV_FILES_DIR}/{filename}', 'r'
    ) as source_csv_file:
        csv_data = csv.DictReader(source_csv_file)
        for number, data in enumerate(csv_data):
            placeholder = ", ".join(["?"] * len(data))
            sql_cmd = (
                "INSERT INTO {table} ({columns}) VALUES({values});".format(
                    table=db_table,
                    columns=",".join(data.keys()), values=placeholder)
            )
            cur.execute(sql_cmd, list(data.values()))
            logging.info(
                f'Successfully write row {number} '
                f'from 'f'{filename} to table {db_table}!'
            )
            con.commit()


def delete_table(prefix):
    """Function for delete data in table from csv."""
    db_table = FILES_DICT[prefix]
    con = sqlite3.connect(f"{BASE_DIR}/db.sqlite3")
    cur = con.cursor()
    cur.execute(f"DELETE FROM {db_table}")
    logging.info(f"Data was deleted from {db_table}")
    con.commit()


def db_action(filename, options, prefix):
    """Run one of function read, write or delete."""
    if options["write"]:
        write_to_db(filename, prefix)
    if options["read"]:
        for data in read_db(prefix):
            print(data)
    if options["delete"]:
        delete_table(prefix)


class Command(BaseCommand):
    help = 'Read from db, or write to db from csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)
        parser.add_argument(
            '--read',
            action='store_true',
            help='read from database',
        )
        parser.add_argument(
            '--write',
            action='store_true',
            help='write to database',
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='write to database',
        )

    def handle(self, **options):
        if not (options.get("read") or options.get("write")
                or options.get("delete")):
            raise CommandError("Use --read, --write or --delete argument")
        filename = options.get("filename")[0]
        prefix = filename.split('.')[0]

        try:
            db_action(filename, options, prefix)
        except FileNotFoundError as error:
            logging.error(error)
            raise CommandError(
                f"There is no {filename} in {CSV_FILES_DIR}"
            )
        except sqlite3.IntegrityError as error:
            logging.error(
                f"{CSV_FILES_DIR} {error}"
            )
        except sqlite3.OperationalError as error:
            logging.error(
                f"{error}"
            )
        except KeyError as error:
            logging.error(
                f"Bad args or file not found in {error}"
            )
