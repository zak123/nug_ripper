nug_ripper

![alt text](https://i.imgur.com/q4hdY5x.png "successful console log")

I am not responsible for any misuse of this script -- it does not break any rules and performs no sort of DRM decryption.

# pre reqs

- an account
- PyCharm Community Edition recommended, it sets up your virtual env for you and its free. If you dont use this, setup your virtual env yourself
	- https://packaging.python.org/guides/installing-using-pip-and-virtualenv/

# installation

- install python
- pip install selenium and wget if needed
- install chrome driver 
	- http://chromedriver.chromium.org/getting-started

# configuration
- inside of nugs_grabber.py
	- replace `email` with your login email
	- replace `password` with your password
	- replace the last line with the show ID/s you want to rip

# running

- in terminal/cmd, run `python nugs_grabber.py`
	- this implies that you have your path variable set for python3, if not, direct your command at python (replace python with the path to it)
