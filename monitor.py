import time
from bs4 import BeautifulSoup
import requests
import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Mail

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
EMAIL = os.environ['EMAIL']

def get_review_count():
	r  = requests.get("https://www.coursereport.com/schools/hackbright-academy")
	soup = BeautifulSoup(r.text, features="html.parser")
	span = soup.find(attrs={'itemprop': 'reviewCount'})
	return int(span.text)


def send_alert():
	from_email = Email(EMAIL)
	to_email = Email(EMAIL)
	subject = "new review"
	content = Content("text/plain", "https://www.coursereport.com/schools/hackbright-academy")
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	print(response.status_code)
	print(response.body)
	print(response.headers)

with open('count.txt') as f:
	count = int(f.read())

print('count', count)

while True:
	try:
		new_count = get_review_count()
	except Exception as e:
		print(e)

	if new_count != count:
		if new_count > count:
			send_alert()
		count = new_count
		with open('count.txt', 'w') as f:
			f.write(str(count))
		print('count updated:', count)
	else:
		print('no change')
	time.sleep(3600)
