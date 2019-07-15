import os
from flask_script import Manager  # The Manager class keeps track of all the commands and handles how they are called
from flask_migrate import Migrate, MigrateCommand

from src.app import create_app, db

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

migrate = Migrate(app=app, db=db)  # creating migrate instance

manager = Manager(app=app)  # creating manager instance

manager.add_command('db', MigrateCommand)  # adding "db" as the command to manager instance

if __name__ == '__main__':
    manager.run()  # calling manager.run() so Manager instance can receive input from the command line.