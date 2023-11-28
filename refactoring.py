import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, login, password):
        self.connect = {'login': login, 'password': password}

    def sending_message(self, server, port, recipients, subject, body):
        try:
            email_message = MIMEMultipart()
            email_message['From'] = self.connect['login']
            email_message['To'] = ', '.join(recipients)
            email_message['Subject'] = subject
            email_message.attach(MIMEText(body))
            sendmail_ex = smtplib.SMTP(server, port)
            sendmail_ex.ehlo()
            sendmail_ex.starttls()
            sendmail_ex.ehlo()
            sendmail_ex.login(self.connect['login'], self.connect['password'])
            res = sendmail_ex.sendmail(email_message['From'], email_message['To'], email_message.as_string())
            sendmail_ex.quit()
            return res
        except Exception as ex:
            return f'Error sending the message: {ex}'

    def receiving_mail(self, server, mailbox, header=None):
        receiving_mail_ex = imaplib.IMAP4_SSL(server)
        try:
            receiving_mail_ex.login(self.connect['login'], self.connect['password'])
            receiving_mail_ex.list()
            receiving_mail_ex.select(mailbox)
            criterion = '(HEADER Subject "%s")' % header if header else 'ALL'
            result, data = receiving_mail_ex.uid('search', None, criterion)
            assert data[0], 'There are no letters with current header'
            latest_email_uid = data[0].split()[-1]
            print(latest_email_uid.decode('utf-8'))
            result, data = receiving_mail_ex.uid('fetch', latest_email_uid.decode('utf-8'), '(RFC822)')
            raw_email = data[0][1]
            email_message_receive = email.message_from_string(raw_email.decode('utf-8'))
            receiving_mail_ex.logout()
            return email_message_receive
        except Exception as ex:
            return f'Error receiving the message: {ex}'


if __name__ == '__main__':
    gmail = Email('login@gmail.com', 'qwerty')
    print(gmail.sending_message(
        'smtp.gmail.com',
        587,
        ['gmailuser@gmail.com', 'anotheruser@hmail.com'],
        'Initial message',
        'Text of the message'
    ))
    print(gmail.receiving_mail('imap.gmail.com', 'inbox'))