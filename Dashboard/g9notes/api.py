from flask import render_template
from flask_peewee.rest import Authentication
from flask_peewee.rest import RestAPI
from flask_peewee.rest import RestResource

from g9notes import app
from g9notes.models import Note, Task

# Allow GET and POST requests without requiring authentication.
auth = Authentication(protected_methods=['PUT', 'DELETE'])
api = RestAPI(app, default_auth=auth)

class NoteResource(RestResource):
    fields = ('id', 'content', 'timestamp', 'status')
    paginate_by = 30

    def get_query(self):
        return Note.public()

    def prepare_data(self, obj, data):
        data['rendered'] = render_template('note.html', note=obj)
        return data

class TaskResource(RestResource):
    paginate_by = 50

api.register(Note, NoteResource)
api.register(Task, TaskResource)
