# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import smtplib
from email.MIMEText import MIMEText

from crabapple.notifier.notifier import Notifier
from crabapple.exception import ConfigurationException


class EmailNotifier(Notifier):

    name = 'email'

    def __init__(self):
        super(EmailNotifier, self).__init__()
        self.host = None
        self.port = None
        self.ssl = True
        self.user = None
        self.password = None
        self.address = None
        self.recipients = []

    def config(self, kwargs):
        sender = kwargs.get('sender', None)
        if sender is None:
            raise ConfigurationException('missed the sender')
        host = sender.get('host', None)
        if host is None:
            raise ConfigurationException('missed the host')

        ssl = sender.get('ssl', True)
        port = int(sender.get('port', 587))
        user = sender.get('user', None)
        password = sender.get('password', None)
        address = sender.get('address', None)
        if user is None \
            or password is None \
                or address is None:
            raise ConfigurationException('missed the user or password or email address')

        self.host = host
        self.port = port
        self.ssl = ssl
        self.user = user
        self.password = password
        self.address = address

        recipients = kwargs.get('recipients', None)
        if recipients is None:
            raise ConfigurationException('missed the recipients')
        if not isinstance(recipients, list):
            recipients = [recipients]
        self.recipients = recipients

    def send(self, msg, subject=''):
        content = msg + '''

----

Crabapple - An automatic deployment tool which integrated with Github.

An open source software released by starfruit.io
'''
        m = MIMEText(content, _charset="UTF-8")
        m['From'] = self.address
        m['To'] = ','.join(self.recipients)
        m['Subject'] = subject
        s = smtplib.SMTP()
        s.connect(self.host, self.port)
        if self.ssl:
            s.starttls()
        s.login(self.user, self.password)
        s.sendmail(self.address, self.recipients, m.as_string())
        s.quit()
