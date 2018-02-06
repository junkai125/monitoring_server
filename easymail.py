#!/usr/bin/python
"""  
MIT LICENSE
Copyright (c) 2016 Tan Kuan Pern

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import smtplib
import mimetypes
import subprocess
import tempfile
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEAudio import MIMEAudio
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64

def sendMail(emailUser, recipient, emailPassword, subject, text, *attachmentFilePaths):

	def getAttachment(attachmentFilePath):
		contentType, encoding = mimetypes.guess_type(attachmentFilePath)

		if contentType is None or encoding is not None:
			contentType = 'application/octet-stream'

		mainType, subType = contentType.split('/', 1)
		file = open(attachmentFilePath, 'rb')

		if mainType == 'text':
			attachment = MIMEText(file.read())
		elif mainType == 'message':
			attachment = email.message_from_file(file)
		elif mainType == 'image':
			attachment = MIMEImage(file.read(),_subType=subType)
		elif mainType == 'audio':
			attachment = MIMEAudio(file.read(),_subType=subType)
		else:
			attachment = MIMEBase(mainType, subType)
		attachment.set_payload(file.read())
		encode_base64(attachment)

		file.close()

		attachment.add_header('Content-Disposition', 'attachment',	 filename=os.path.basename(attachmentFilePath))
		return attachment
	# end def
	msg = MIMEMultipart()
	msg['From'] = emailUser
	msg['To'] = recipient
	msg['Subject'] = subject
	msg.attach(MIMEText(text))

	for attachmentFilePath in attachmentFilePaths:
		msg.attach(getAttachment(attachmentFilePath))

	mailServer = smtplib.SMTP('smtp.gmail.com', 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(emailUser, emailPassword)
	mailServer.sendmail(emailUser, recipient, msg.as_string())
	mailServer.close()

# end def

def utils_sendMail(emailUser, recipient, subject, text, attachFile = None):

	fp = tempfile.NamedTemporaryFile()
	fp.write(text)
	fp.seek(0)

	cmd_template = '''mail -aFrom:{emailUser} -s "{subject}" --attach "{attachFile}" {recipient} < {textFile}'''
	cmd = cmd_template.format(
		emailUser = emailUser,
		recipient = recipient,
		subject   = subject,
		textFile  = fp.name,
		attachFile = attachFile
	)

	if attachFile == None:
		cmd = cmd.replace('--attach "None"', '')
	# end if

	process = subprocess.Popen(cmd, shell = True)
	process.wait()
# end def

_ = """
def sendMail(emailUser, recipient, emailPassword, subject, text, attachFile = None):
	utils_sendMail(emailUser, recipient, subject, text, attachFile = attachFile)
# end def
"""
