import imaplib
import email as EMAIL
from email.header import decode_header
import webbrowser
import os
from g9client import db
from g9client.models import Emails

def syncMail(username, password, imap_server):
     # username = current_user.email
     # password = current_user.password # can't use hashed password - need encryption for security
     imap = imaplib.IMAP4_SSL(imap_server)

     # authenticate
     imap.login(username, password)

     status, messages = imap.select("INBOX")

     # total number of emails
     N = int(messages[0])

     for i in range(N, 0, -1):
         # fetch the email message by ID
         res, msg = imap.fetch(str(i), "(RFC822)")
         for response in msg:
             if isinstance(response, tuple):
                 # parse a bytes email into a message object
                 msg = EMAIL.message_from_bytes(response[1])
                 # decode the email subject
                 subject = decode_header(msg["Subject"])[0][0]
                 if isinstance(subject, bytes):
                     # if it's a bytes, decode to str
                     subject = subject.decode()
                 sender = msg.get("From") # email sender
                 date = msg.get("Date")

                 # Check if email is stored in the database already
                 email_stored = Emails.query.filter_by(user=username, sender = sender, date_received = date).first()

                 if not email_stored: # If the email is not in the database...
                    # if the email message is multipart
                     if msg.is_multipart():
                         # iterate over email parts
                         for part in msg.walk():
                             # extract content type of email
                             content_type = part.get_content_type()
                             content_disposition = str(part.get("Content-Disposition"))
                             try:
                                 # get the email body
                                 body = part.get_payload(decode=True).decode()
                             except:
                                 pass
                     else:
                         # extract content type of email
                         content_type = msg.get_content_type()
                         # get the email body
                         body = msg.get_payload(decode=True).decode()

                     if content_type == "text/html":
                         body_is_html = True
                     else:
                         body_is_html = False

                     email = Emails(
                        user = username,
                        sender = sender,
                        subject = subject,
                        date_received = date,
                        body = body,
                        body_is_html = body_is_html
                     )

                     db.session.add(email)
                     db.session.commit()

     imap.close()
     imap.logout()