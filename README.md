UQx Mailouts
========

UQx Mailouts sends email newsletters using Amazon Simple Email Service (SES). UQx Mailouts imports and updates a subscription list from the email_opt_in-prod-analytics.csv file that is downloaded with the edX data dump. UQx Mailouts stores email newsletters and ensures that no duplicate emails are sent to a learner that is enrolled in multiple courses.

Local Installation using VirtualEnv
---------

**If you do not have VirtualEnv installed:**
```bash
$ pip install virtualenv
$ pip install virtualenvwrapper
```
Add the following line to your bash config: `~/.bashrc` on Ubuntu, `~/.bash_profile` on macOS:
```
. /usr/local/bin/virtualenvwrapper.sh
```
Then run: `$ source ~/.bashrc` OR `$ source ~/.bash_profile`  


**Create a virtual environment for UQx Mailouts:**

```bash
$ mkvirtualenv clatoolkit
$ workon clatoolkit
```

**Get code from GitHub:**

```bash
$ git clone https://github.com/UQ-UQx/mailouts.git
$ cd mailouts
```

**Install Python and Django Requirements**

A requirements.txt file is provided in the code repository.

```bash
$ pip install -r requirements.txt
```

**Install UQx Mailouts**

Edit mailouts/settings.py
Enter a secret key
Create a database (both MySQL and Postgres are supported). Enter database port and name in settings.py
Enter the filename and path to the OPT_IN_CSVFILE from edX.
Enter the url for the server that has the unsubscribe link in UNSUBSCRIBE_SERVER_URL.

If a new database was created, you will need to setup the database tables and create a superuser.
```bash
$ python manage.py migrate
$ python manage.py createsuperuser
```

Now you can run the django webserver:
```bash
$ python manage.py runserver
```

**Creating an Email Newsletter**
If a new database was created go to http://localhost:8000/admin and login with superuser account. The Django admin interface is used to add Newsletters.

- Add a newsletter. You will need an Amazon SES verified from email address (Sender email). Both HTML (Email body) and Plaintext (Email text) emails are supported. A comma separated list of courses (i.e., the edX course id) must be specified (Course Criteria). A student will only be included as an email recipient once even if they are enrolled in multiple courses. The "Demographic criteria" field is not yet implemented.
http://www.campaignmonitor.com has a ui that can be used to create html email templates that are responsive and display in multiple clients.
The email body and email text fields are django templates. Currently only {{name}} and {{unsubscribe_link}} are the two supported variables. 
- Click the Save button. Copy the Newsletter id.

**Generate newsletter recipients**
- Go to http://localhost:8000/mailouts/setuprecipients/?newsletter_id=1 where newsletter_id is the Newsletter id that was copied from the admin interface. All recipients that are enrolled in courses matching the course id's entered will be added as a recipients. At this stage no emails are send out.

**Sanity Check**
- A query to ensure that a student is only included as a recipient once for a Newsletter even though the student may be enrolled in multiple courses
```
SELECT subscription_id, COUNT(*)
FROM mailouts_newsletterrecipient
WHERE newsletter_id_id=5 and sent_flag=false
GROUP BY subscription_id
HAVING
    COUNT(*) > 1
```

**Send email newsletters**
- Go to http://localhost:8000/mailouts/sendnewsletters/?newsletter_id=1 where newsletter_id is the Newsletter id that was copied from the admin interface. Emails are sent out.
