import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from project import db
from run import app

# MYSQL_USER = os.getenv("MYSQL_USER")
# MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
# MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{MYSQL_USER}:{MYSQL_DATABASE}@db/{MYSQL_DATABASE}"

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@db/doctor_appointment"

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()