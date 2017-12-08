import os
from flask_script import Manager, Shell
<< << << < Updated
upstream
from flask_migrate import Migrate,MigrateCommand
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')#create_app返回配置好的app
== == == =
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # create_app返回配置好的app
>> >> >> > Stashed
changes
migrate = Migrate(app, db)
manager = Manager(app)

<< << << < Updated
upstream
#@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

== == == =
# @app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

>> >> >> > Stashed
changes
'''
@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
'''
if __name__ == '__main__':
    manager.run()