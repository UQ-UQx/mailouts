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

Edit clatoolkit_project/settings.py
Enter secret key
Enter database port and name in settings.py

If a new database was created, you will need to setup the database tables and create a superuser.
```bash
$ python manage.py migrate
$ python manage.py createsuperuser
```

Now you can run the django webserver:
```bash
$ python manage.py runserver
```

**Sending an Email Newsletter**
If a new database was created go to http://localhost:8000/admin and login with superuser account
Add a newsletter. You will need an Amazon SES verified from email address. Both HTML and Plaintext emails are supported. The list of
