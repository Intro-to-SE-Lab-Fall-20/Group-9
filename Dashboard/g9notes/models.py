import datetime

from flask import Markup
from markdown import markdown
from micawber import parse_html
from peewee import *

from g9notes import db, huey, oembed

def rich_content(content, maxwidth=300):
    html = parse_html(
        markdown(content),
        oembed,
        maxwidth=maxwidth,
        urlize_all=True)
    return Markup(html)

class Note(Model):
    STATUS_VISIBLE = 1
    STATUS_ARCHIVED = 2
    STATUS_DELETED = 9

    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    status = IntegerField(default=STATUS_VISIBLE, index=True)
    reminder = DateTimeField(null=True)
    reminder_task_created = BooleanField(default=False)
    reminder_sent = BooleanField(default=False)

    class Meta:
        database = db

    def html(self):
        return rich_content(self.content)

    def is_finished(self):
        if self.tasks.exists():
            return not self.tasks.where(Task.finished == False).exists()

    def get_tasks(self):
        return self.tasks.order_by(Task.order)

    def parse_content_tasks(self):
        # Split the list of tasks from the surrounding content, returning both.
        content = []
        tasks = []
        for line in self.content.splitlines():
            if line.startswith('@'):
                tasks.append(line[1:].strip())
            else:
                content.append(line)
        return '\n'.join(content), tasks

    def save(self, *args, **kwargs):
        # Split out the text content and any tasks.
        self.content, tasks = self.parse_content_tasks()

        # Determine if we need to set a reminder.
        set_reminder = self.reminder and not self.reminder_task_created
        self.reminder_task_created = True

        # Save the note.
        ret = super(Note, self).save(*args, **kwargs)

        if set_reminder:
            # Set a reminder to go off by enqueueing a task with huey.
            send_note_reminder.schedule(args=(self.id,), eta=self.reminder)
        if tasks:
            # Store the tasks.
            Task.delete().where(Task.note == self).execute()
            for idx, title in enumerate(tasks):
                Task.create(note=self, title=title, order=idx)
        return ret

    @classmethod
    def public(cls):
        return (Note
                .select()
                .where(Note.status == Note.STATUS_VISIBLE)
                .order_by(Note.timestamp.desc()))


class Task(Model):
    note = ForeignKeyField(Note, related_name='tasks')
    title = CharField(max_length=255)
    order = IntegerField(default=0)
    finished = BooleanField(default=False)

    class Meta:
        database = db

    def html(self):
        return rich_content(self.title)


@huey.task(retries=3, retry_delay=60)
def send_note_reminder(note_id):
    with database.transaction():
        try:
            note = Note.get(Note.id == note_id)
        except Note.DoesNotExist:
            app.logger.info(
                'Attempting to send reminder for note id=%s, but note '
                'was not found in the database.', note_id)
            return

        if note.status == Note.STATUS_DELETED:
            app.logger.info('Attempting to send a reminder for a deleted '
                            'note id=%s. Skipping.', note_id)
            return

        try:
            mailer.send(
                to=app.config['REMINDER_EMAIL'],
                subj='[notes] reminder',
                body=note.content)
        except:
            app.logger.info('Sending reminder failed for note id=%s.', note_id)
            raise
        else:
            note.reminder_sent = True
            note.save()
