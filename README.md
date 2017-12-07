# Capstone

====================================================
    Active learning using crowds in the loop
====================================================

Install python 2.7 or anaconda python 2

Required python packages: pymongo, boto and boto3

==========================================
		Installation and setup
==========================================

To clone the application:

	git clone (git url)

Data and AWS key:

    Place the data files inside the 'data' directory.

    Add your AWS access key and secret token  in the credentials file with a new line in-between located in
    python_scripts/AWS_key/.

To install Meteor:

	curl https://install.meteor.com/ | sh

To start the meteor application and let it run continuously:

    Go to meteor_application directory and run the command:

	    nohup meteor --port 8080 &

To setup meteor :

    Go to meteor application directory and run the commands:

	    meteor npm install --save babel-runtime

	    meteor npm install --save core-js

	    meteor add session

	    meteor remove autopublish


Load data into meteor mongo:

    Go to python_scripts directory and run the commands:

	    python insert_data_into_mongodb.py

	    python insert_crowdflower_data.py

Create HITS:

    Go to python_scripts directory and run the commands:

	    python create_hit.py (To create HITS using data which is not labeled)

	    python create_hit.py 10 (To create HITS using crowdflower data containing 10 tweets per HIT)
