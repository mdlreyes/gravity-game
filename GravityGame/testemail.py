# Import smtplib for the actual sending function
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
#from camera import to_email

#print to_email
def SendEmail(to_email):
	gmail_user = 'starwarps.openafternoon@gmail.com'
	gmail_pwd = 'gravitygame'
	to_user = to_email #'mithidelosreyes@gmail.com'
	FROM = 'Star Warps: Gravitational Lensing Game'
	TO = [to_email] #['mithidelosreyes@gmail.com']
	'''
	SUBJECT = 'Your lensed picture!'
	TEXT = 
	'''

	body = """
	Hi!\n
	Attached is the image of yourself that you \"lensed\" using a dark matter halo! 
	Thanks for attending the Open Afternoon at the University of Cambridge's Institute of Astronomy. We hope you had a good time, and that you stay curious about science!\n
	From,
	Your friends at the IoA
	\n\n"""

	msg = MIMEMultipart()

	msg['From'] = gmail_user
	msg['To']	= to_user
	msg['Subject'] = 'Your lensed picture!'

	msg.attach(MIMEText(body, 'plain'))

	filename = "YourLensedSelfie.jpg"
	attachment = open("images/test_image_lensed.jpg", "rb")
	 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	 
	msg.attach(part)
	'''
	message = """From: %s\nTo: %s\nSubject: %s\n\n%s
		""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
	'''

	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)

		text = msg.as_string()
		server.sendmail(FROM, TO, text)

		server.close()
		print 'successfully sent the mail'

	except:
		print "failed to send mail"