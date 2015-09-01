#!/usr/bin/env python
"""
    html_mail enables sending html content to
    a list of recipients

    implements a multipart mime message for text email and HTML content

    sets up a mime message frame

    requires:
        html message
        recipient list
        smtp configuration

    depends html2text
"""

__author__ = "mark.menkhus@gmail.com"
__version__ = "v0.1"

import smtplib
import html2text
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re


def html_mail(sender='me@mail.com', recipients=['them@mail.com'],
              html_content='<p>Hi</p>', subject='Hello!',
              mailserver='localhost'):
    """ html_mail takes input html, sender, recipents and
    emails it in a mime type that will show as text or html on
    the recipients mail reader.

    depends on email, html2text

    """
    # Create an email message container - uses multipart/alternative.
    # sets up basic email components
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = recipients
    # create a markdown text version of the supplied html content
    text = html2text.html2text(html_content)
    # setup the MIME types for both email content parts, text - plain & text - html.
    email_part1 = MIMEText(text, 'plain')
    email_part2 = MIMEText(html_content, 'html')
    """
    complete the message composition -
      attach the email parts into our message container.
      make the order such that the text email is seen by the recipient, in case
      they are not reading with a mime & html compatible reader.
    """
    message.attach(email_part1)
    message.attach(email_part2)
    # Send the message via our SMTP server.
    conn = smtplib.SMTP(mailserver)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    try:
        return_value = conn.sendmail(sender, recipients, message.as_string())
        conn.quit()
    except Exception as e:
        print "error sending email: html_mail.html_mail %s" % (e,)
        return (return_value)

    if return_value:
        return return_value
    else:
        return None


def highlight_cve(html_doc='<html>\n<p>\nthis is CVE-1999-1000\n</p>\n</html>\n'):
    """ highlight CVE numbers in html doc, change each CVE to a
        link
    """
    output_doc = ''
    nvd_url = 'https://web.nvd.nist.gov/view/vuln/detail?vulnId='
    for line in html_doc.split('\n'):
        m = re.findall(r'CVE-\d\d\d\d-\d\d\d\d\d|CVE-\d\d\d\d-\d\d\d\d', line)
        if m:
            for matched in m:
                ref = r'<a href="' + nvd_url + matched + r'" target="_blank">' + matched + r'</a>'
                line = re.sub(matched, ref, line)
            output_doc += line + '\n'
        else:
            output_doc += line + '\n'
    return output_doc

