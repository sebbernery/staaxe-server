import argparse

from playhouse.migrate import SqliteMigrator, SqliteDatabase, CharField, migrate

parser = argparse.ArgumentParser(description='Migration: add ip_address field to ConnectionInfo.')
parser.add_argument("dbfile")

args = parser.parse_args()

my_db = SqliteDatabase(args.dbfile)
migrator = SqliteMigrator(my_db)

ipfield = CharField(default='')

with my_db.transaction():
    migrate(
        migrator.add_column('ConnectionInfo', 'ip_address', ipfield),
    )
