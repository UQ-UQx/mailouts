def sendsesemail(newsletter_id):
	name = 'Aneesha'
	subject = 'Hello from SES Test'
	body = 'Hello {{name}} <br/> {{unsubscribe_link}}'
	recipient = 'test@test.edu.au'

	unsubscribe_link = make_unsubscribe_link(recipient)

	# create the message and send the email
	# the from address must be a verified sender in SES
	msg = SESMessage('test@test.edu.au', recipient, subject, body, body, {'name':name, 'unsubscribe_link':unsubscribe_link})
	#msg.text = body
	#msg.html = body + ' html'
	msg.send()
