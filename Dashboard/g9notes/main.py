from app import app
from models import Note
from models import Task
from api import api
import views

api.setup()

if __name__ == '__main__':
    Note.create_table(True)
    Task.create_table(True)
    app.run()