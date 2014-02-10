pylib
=====

python library for useful tools

mail.py
========
Email sender using HTML/TEXT templates

Step 1:
--------------------------
Create a TEXT/HTML file with the Keys as below

  Hi [username],
  
  Thank you for your registration.
  
  Best regards,
  [from]
  [url]


Step 2:
----------------------------
Create a template passing the values to replace with the keys in template

  values = {}
  values['username'] = 'Ludmal de silva!'
  values['from'] = 'The Team'
  values['url'] = 'http://www.ludmal.com'
  
  temp = EmailTemplate(template_name='welcome.txt', values=values)

Step 3:
-----------------------------
Create a Mail Server 
  server = MailServer(server_name='smtp.gmail.com', username='<username>', password='<password>', port=0, require_starttls=True)

Step 4:
-----------------------------
Create a mail message and send the email

  msg = MailMessage(from_email='ludmal@gmail.com', to_emails=['ludmal@gmail.com'], subject='Welcome')
  send(mail_msg=msg, mail_server=server, template=temp)


