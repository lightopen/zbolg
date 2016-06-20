from app import create_app
from flask.ext.script import Manager


app = create_app("default")
manage = Manager(app)

if __name__ == "__main__":
    manage.run()
