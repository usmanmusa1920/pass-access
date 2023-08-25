# Deployment on linode platform

This readme will walk on how to deploy django app on linode platform! In here we will assume our ip-address is `197.33.12.17`.

First create account on linode `cloud.linode.com`, once you create and login, click on create (linode i.e select) & select image & scroll i.e pick region & plan (nanode for testing mostly) & write your app label e.g (umfo-server) & root password on the server & create, wait to boot.

Once finished, click on your new server & click on networking & copy ssh access & paste to your terminal & type yes & type root password. Next is to run the following command on your server terminal:

```sh
    apt-get update && apt-get upgrade -y
```

and hit enter, next change hostname by

```sh
    hostnamectl set-hostname umfo-server
```

if you type `hostname` after such you will see `umfo-server`. Next get into a file using nano text-editor so as to add your ip-address and your server hostname, like so:

```sh
    nano /etc/hosts NB: under
```

in the file add the following and save the file

```sh
127.0.0.1         localhost
197.33.12.17      umfo-server
```

The next thing is to add new user: `adduser usman` & put password & fullname & hit tab. Also add the new user to the sudo group by `adduser usman sudo`, now logout and then loging using the user you just created by:

```sh
    ssh usman@197.33.12.17
```

hit tab & put password, if you type pwd you will see you are in home directory, now make a directory tree using `mkdir -p ~/.ssh` & then `ls -la`

Next thing is to open new terminal for local machine & type `ssh-keygen -b 4096` & hit enter, which will generate a public and private key.

After such type `scp ~/.ssh/id_rsa.pub usman@197.33.12.17:~/.ssh/authorised_keys` & enter your password, this will copy your generated public key from your local machine to your server machin.

To verify if it copy it, go back to server terminal and type `ls .ssh` you will see `authorised_keys`, change the mode of the entire `.ssh` directory by `sudo chmod 700 ~/.ssh/` & enter your password, then `sudo chmod 600 ~/.ssh/*` which will chnage the mode of everything within the directory & exit.

13. ssh usman@197.33.12.17 & sudo nano /etc/ssh/sshd_config & put password edit PermitRootLogin from yes to no, and also edit PasswordAuthentication from yes to no & CTRL + X & y & hit tab
14. And now restart the server by typing: sudo systemctl restart sshd
15. sudo apt-get instal ufw & sudo ufw default allow outgoing &
sudo ufw default deny incoming & sudo ufw allow 8000 & sudo ufw enable & y
and hit tab & sudo ufw status
16. Go back to local machine terminal and make requirements.txt
for your project, NB if you are in your project folder, go back one by cd ..
& scp -r zazzone usman@197.33.12.17:~/
17. Go back to server machine and type ls to see your project you copy just now
18. ls & ls zazzone
20. sudo apt-get install python3-pip & sudo apt-get install python3-venv
python3 -m venv zazzone/venv & ls zazzone & cd zazzone
& source venv/bin/activate & pip install -r requirements.txt
& sudo nano zazzone/settings.py & edit allowed host (Allowed_Host=['197.33.12.17'])
and go to bottom and add:STATIC_ROOT=os.path.join(BASE_DIR, 'static')
21. python manage.py collectstatic & ls (you will see new folder i.e static)
22. python3 manage.py runserver 0.0.0.0:8000 (specify the linode server i.e 0.0.0.0:8000)
23. Open browser and type your ip address (197.33.12.17:8000), and then test
your app by l,ogging and do manything as you can do when using localhost & CTRL + C
NB python manage.py runserver is not suite for production, but it is for testing.
NB to run server that is reliable for production e.g (apache, ngnix) first install apache & WSGI
24. cd (to go root directory) & sudo apt-get install apache2 &
sudo apt-get install libapache2-mod-wsgi-py3 &
cd /etc/apache2/sites-available/ & ls (NB: you may see two files i.e
000-default.conf and default-ssl.conf)
sudo cp 000-default.conf zazzone.conf & sudo nano zazzone.conf NB: scroll down before the closing virtualHost and add new rules:
```sh
    Alias /static /home/usman/zazzone/static
    <Directory /home/usman/zazzone/static>
        Require all granted
    </Directory>

    Alias /media /home/usman/zazzone/media
    <Directory /home/usman/zazzone/media>
        Require all granted
    </Directory>

    <Directory /home/usman/zazzone/zazzone>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIScriptAlias / /home/usman/zazzone/zazzone/wsgi.py
    WSGIDaemonProcess django_app python-path=/home/usman/zazzone python-home=/home/usman/zazzone/venv
    WSGIProcessGroup django_app
```
25. Save everything by CTRL + X and y then hit tab & then go back to your home directory by cd
26. Enable that site through apache by: sudo a2ensite zazzone & disable the default by: sudo a2dissite 000-default.conf
27. sudo chown :www-data zazzone/db.sqlite3
sudo chmod 664 zazzone/db.sqlite3
sudo chmod :www-data zazzone/, and the ls -la to verify
sudo chmod -R :www-data zazzone/media/
sudo chmod -R 775 zazzone/media == & sudo chmod 775 zazzone/
NB: environment variable in apache can be a little tricky to work with, because you have to change the wsgi python file and things like that, so it will be easier to use config file instead of environment variable
28. sudo touch /etc/config.json
sudo nano zazzone/zazzone/settings.py & copy your secret key & erase it also (within)
sudo nano /etc/config.json
{
    "SECRET_KEY": "fghfdsyhjgdjsftgdhfsyjdhgjks",
    "EMAIL_USER": "user@mail.com",
    "EMAIL_PASS": "**********",
}
Then save it and do: sudo nano zazzone/zazzone/settings.py
import json (within settings.py)
with open('/etc/config.json') as config_file:
    config = json.load(config_file)
SECRET_KEY = config['SECRET_KEY']
DEBUG = False & and then scroll down to edit other sensitive information
EMAIL_HOST_USER = config.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('EMAIL_HOST_PASSWORD')
and then save and exit
29. Now disallow the port 8000 for testing by: sudo ufw delete allow 8000
sudo ufw allow http/tcp, and now restart apache server
sudo service apache2 restart
NB: open browser and visit 197.33.12.17 without the port 8000, but if you
specify the port it won't reach, and then test your site by making post or login.
NB: if you see any error while testing a live server (website) you should set a test server and test with debug=True
NB: if you see attempt to write a readonly database, go to server terminal
and do: ls -la zazzone/ (to see permission)
        ls -la (to see permission)
    sudo chmod 775 zazzone/
    sudo service apache2 restart
NB: then go to browser and test your site, along side witj passwordReset (email)
NB: Do django deployment checklist & read to ensure anything is good to go
    if any or e.g debug is True go back to server terminal and edit it
    wheather in .env, config_file.json or directly in settings.py
NB: To delete server (maybe stop charging you), goto your linode account &
    click on the server to delete, then settings & expand delete linode
    & click delete