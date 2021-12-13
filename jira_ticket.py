"""
This utility cretae jira tickets from help form
"""
from jira.client import JIRA
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import smtplib
import urllib
import yaml
import os


def send_email(jira_issue, subject, body):
    subject = f'''DESDM Help Request [{jira_issue}]: {subject}'''
    toemail = 'desaccess-admins@lists.ncsa.illinois.edu'
    fromemail = 'devnull@ncsa.illinois.edu'
    s = smtplib.SMTP('smtp.ncsa.uiuc.edu')
    text = f'''
    <html>
        <p><a href="https://opensource.ncsa.illinois.edu/jira/browse/{jira_issue}">Jira Issue: {jira_issue}</a></p>
        <pre style="white-space: pre-wrap;">{body}</pre>
    </html>
    '''
    MP1 = MIMEText(text, 'html')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = formataddr((str(Header('DESRELEASE JIRA', 'utf-8')), fromemail))
    msg['To'] = toemail
    msg.attach(MP1)
    s.sendmail(fromemail, toemail, msg.as_string())
    s.quit()


def create_ticket(first, last, email, topics, subject, question):
    with open('config/desaccess.yaml', 'r') as cfile:
        conf = yaml.load(cfile, Loader=yaml.FullLoader)['jira']
    my_string_u = base64.b64decode(conf['uu']).decode().strip()
    my_string_p = base64.b64decode(conf['pp']).decode().strip()
    """
    This function creates the ticket coming form the help form
    """

    jira = JIRA(
        server="https://opensource.ncsa.illinois.edu/jira/",
        basic_auth=(my_string_u, my_string_p))

    body = """
    *ACTION ITEMS*
    - Please ASSIGN this ticket if it is unassigned.
    - PLEASE SEND AN EMAIL TO  *%s* to reply to this ticket
    - COPY the answer in the comments section and ideally further communication.
    - PLEASE close this ticket when resolved


    *Name*: %s %s

    *Email*: %s

    *Topics*:
    %s

    *Question*:
    %s

    """ % (email, first, last, email, topics, question)

    issue = {
        'project': {'key': 'DESRELEASE'},
        'issuetype': {'name': 'Task'},
        'summary': 'Q: %s' % subject,
        'description': body,
    }
    try:
        new_jira_issue = jira.create_issue(fields=issue)
        assignment_success = False
        try:
            assignment_success = jira.assign_issue(new_jira_issue, os.environ['JIRA_DEFAULT_ASSIGNEE'])
        except:
            pass
    except:
        new_jira_issue = 'JIRA ERROR'
    try:
        send_email(jira_issue=new_jira_issue, subject=subject, body=body)
    except:
        pass
