import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from project import db
from run import app

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@localhost/doctor_appointment"

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()