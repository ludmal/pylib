__author__ = 'Ludmal.DESILVA'

import os, email, smtplib

path = os.path.dirname(__file__)
#modify this to change the Template Directory
TEMPLATE_DIR = '/templates/'


class EmailTemplate():
    def __init__(self, template_name='', values={}, html=True):
        self.template_name = template_name
        self.values = values
        self.html = html

    def render(self):
        content = open(path + TEMPLATE_DIR + self.template_name).read()

        for k,v in self.values.iteritems():
            content = content.replace('[%s]' % k,v)

        return content


class MailMessage(object):
    html = False

    def __init__(self, from_email='', to_emails=[], cc_emails=[], subject='', body=''):
        self.from_email = from_email
        self.to_emails = to_emails
        self.cc_emails = cc_emails
        self.subject = subject
        self.body = body

    def get_message(self):
        if isinstance(self.to_emails, str):
            self.to_emails = [self.to_emails]

        if isinstance(self.cc_emails, str):
            self.cc_emails = [self.cc_emails]

        if len(self.to_emails) == 0 or self.from_email == '':
            raise Exception('Invalid From or To email address(es)')

        msg = email.Message.Message()
        msg['To'] = ', '.join(self.to_emails)
        msg['Cc'] = ', '.join(self.cc_emails)
        msg['From'] = self.from_email
        msg['subject'] = self.subject
        #TODO - Add HTML/TEXT support to the Body
        msg.set_payload(self.body)
        return msg


class MailServer(object):
    msg = None

    def __init__(self, server_name='smtp.gmail.com', username='<username>', password='<password>', port=0, require_starttls=True):
        self.server_name = server_name
        self.username = username
        self.password = password
        self.port = port
        self.require_starttls = require_starttls


def send(mail_msg, mail_server=MailServer(), template=None):
    server = smtplib.SMTP(mail_server.server_name, 587)
    if mail_server.require_starttls:
        server.starttls()
    server.login(mail_server.username, mail_server.password)
    if template:
        mail_msg.body = template.render()
        mail_msg.html = template.html
    server.sendmail(mail_msg.from_email, ', '.join(mail_msg.to_emails), mail_msg.get_message().as_string())
    server.close()

