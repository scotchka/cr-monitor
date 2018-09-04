import time
from bs4 import BeautifulSoup
import requests
import sendgrid
import os
from sendgrid.helpers.mail import Email, Content, Mail

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

def get_review_count():
	r  = requests.get("https://www.coursereport.com/schools/hackbright-academy")
	soup = BeautifulSoup(r.text, features="html.parser")
	span = soup.find(attrs={'itemprop': 'reviewCount'})
	return span.text


def send_alert():
	from_email = Email("tahafut@gmail.com")
	to_email = Email("tahafut@gmail.com")
	subject = "new review"
	content = Content("text/plain", "https://www.coursereport.com/schools/hackbright-academy")
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())
	print(response.status_code)
	print(response.body)
	print(response.headers)

with open('count.txt') as f:
	count = f.read()

print('count', count)

while True:
	new_count = get_review_count()
	if new_count != count:
		count = new_count
		send_alert()
		with open('count.txt', 'w') as f:
			f.write(count)
		print('count updated:', count)
	else:
		print('no change')
	time.sleep(3600)
