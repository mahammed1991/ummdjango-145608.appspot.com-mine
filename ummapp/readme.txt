1. Fork repo

2. Clone the repo(hg clone) to your local machine within a folder from forked repo, update hgrc file with parent and default path.

3. create virtual environmet and activate the environment then install 
	sudo apt-get install libjpeg-dev
	pip install Pillow
	pip install mysql-python

4. download Python Google app engine SDK from https://cloud.google.com/appengine/downloads

5. export app engin to folder where project exist(Within ummapp)
   example:  ummapp$ export PATH=$PATH:/home/temp/work/appollo_mine/umm_apollo_mine/google_appengine

6. and run the project using bellow command within ummapp folder.
	dev_appserver.py .
	


