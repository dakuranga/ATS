import os
from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    help = 'Migrate all tenant databases'

    def handle(self, *args, **options):
        # Path to the directory containing tenant databases
        databases_directory = 'databases'  # Change this to your actual directory path

        # List all files (assuming each file corresponds to a tenant database)
        tenant_database_files = [filename for filename in os.listdir(databases_directory) if filename.endswith('.sqlite3')]

        for database_file in tenant_database_files:
            # Remove the '.sqlite3' extension to get the database name
            database_name = os.path.splitext(database_file)[0]

            # Set the schema name for the current tenant
            self.set_schema_name(connections[database_name], database_name)

            # Run migrations for the current tenant
            self.stdout.write(self.style.SUCCESS(f'Migrating database {database_name}'))
            self.run_migrations(database_name)

    def set_schema_name(self, connection, schema_name):
        """
        Set the schema name for the specified database connection.
        """
        if connection.vendor == 'postgresql':
            # For PostgreSQL, use the schema name
            connection.settings_dict['OPTIONS']['options'] = f"-c search_path={schema_name}"
        elif connection.vendor == 'mysql':
            # For MySQL, use the database name
            connection.settings_dict['NAME'] = schema_name

    def run_migrations(self, database_name):
        from django.core.management import call_command
        call_command('migrate', database=database_name)
