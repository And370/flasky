import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Role
import flask_uploads
from flask_uploads import configure_uploads, UploadSet, IMAGES, UploadConfiguration, uploads_mod
from flask import Blueprint

app = create_app(os.environ.get('FLASK_CONFIG', 'default'))  # create_app返回配置好的app
migrate = Migrate(app, db)
manager = Manager(app)

# flask_uploads.uploads_mod = Blueprint('user_content', __name__, url_prefix='/user_content')
# photos._config = UploadConfiguration('/user_content/')
# UploadConfiguration('H:/flasky/learning/flasky/DATA/Head_portrait', base_url='need/')

photos = UploadSet('PHOTO', IMAGES)
configure_uploads(app, photos)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


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
