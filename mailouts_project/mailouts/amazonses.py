from email.utils import COMMASPACE
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from boto.ses import SESConnection
from django.conf import settings
from django.template import Template, Context
import boto.ses

def render(template_string, context_dict):
    t = Template(template_string)
    c = Context(context_dict)
    return t.render(c)

class SESMessage(object):

    def __init__(self, source, to_addresses, subject, body_html, body_text, context_dict, **kw):
        #self.ses = SESConnection.connect_to_region('us-west-2', settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)

        self.ses = boto.ses.connect_to_region('us-west-2',aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        self._source = source
        self._to_addresses = to_addresses
        self._cc_addresses = None
        self._bcc_addresses = None

        self.subject = subject
        self.text = body_html
        self.html = body_text
        self.context_dict = context_dict
        self.attachments = []

    def send(self):
        if not self.ses:
            raise Exception, 'No connection found'

        if (self.text and not self.html and not self.attachments) or\
           (self.html and not self.text and not self.attachments):
            return self.ses.send_email(self._source, self.subject,
                self.text or self.html,
                self._to_addresses, self._cc_addresses,
                self._bcc_addresses,
                format='text' if self.text else 'html')
        else:
            if not self.attachments:
                message = MIMEMultipart('alternative')

                message['Subject'] = self.subject
                message['From'] = self._source
                if isinstance(self._to_addresses, (list, tuple)):
                    message['To'] = COMMASPACE.join(self._to_addresses)
                else:
                    message['To'] = self._to_addresses

                message.attach(MIMEText(render(self.text, self.context_dict), 'plain'))
                message.attach(MIMEText(render(self.html, self.context_dict), 'html'))
            else:
                raise NotImplementedError, 'Attachments are not currently supported.'

            return self.ses.send_raw_email(message.as_string(), source=self._source,
                destinations=self._to_addresses)

    def preview(self, type):
        if type=='text':
            return render(self.text, self.context_dict)
        else:
            return render(self.html, self.context_dict)
