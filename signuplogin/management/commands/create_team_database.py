# signuplogin/management/commands/create_team_database.py

from django.core.management.base import BaseCommand
import sqlite3
import os
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates a database for a new team'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--domain',
            dest='domain',
            help='Specify the domain for the team',
        )

    def handle(self, *args, **options):
        domain = options['domain']
        if not domain:
            self.stdout.write(self.style.ERROR('Please provide a domain for the team.'))
            return
        
        safe_domain = domain.replace('.', '_')
        db_name = f'team_{safe_domain}.sqlite3'
        db_path = os.path.join(settings.BASE_DIR, 'databases', db_name)
        
        if not os.path.exists(db_path):
            self.stdout.write(f'Creating database for domain {domain}')
            # Ensure the databases directory exists
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            # Create the SQLite database file
            sqlite3.connect(db_path).close()
            self.stdout.write(self.style.SUCCESS(f'Database {db_name} created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Database {db_name} already exists.'))

        try:
            databases_config_path = os.path.join(settings.BASE_DIR, 'tenant_databases.json')
            if os.path.exists(databases_config_path):
                with open(databases_config_path, 'r') as f:
                    databases_config = json.load(f)
            else:
                databases_config = {}

            config_key = db_name.rsplit('.', 1)[0]
            relative_db_path = os.path.join('databases', db_name).replace('\\', '/')
            databases_config[config_key] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': relative_db_path,
            }

            with open(databases_config_path, 'w') as f:
                json.dump(databases_config, f, indent=4)
            
            logger.info(f"Database configuration for {domain} added to {databases_config_path}")

        except Exception as e:
            logger.error(f"An error occurred while updating the tenant databases configuration: {e}")
            raise