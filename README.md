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

	    python insert_data_into_mongodb.py (To add 1 year twitter data in mongoDB)

	    python insert_crowdflower_data.py (To add crowdflower data in mongoDB)

Create HITS:

    Go to python_scripts directory and run the commands:

    To run in the sandbox environment:

	    python create_hit.py sandbox unlabeled (To create HITS using data which is not labeled)

	    python create_hit.py sandbox crowdflower 10 (To create HITS using crowdflower data containing 10 tweets per HIT)

    To run in the production environment:

	    python create_hit.py production unlabeled (To create HITS using data which is not labeled)

	    python create_hit.py production crowdflower 10 (To create HITS using crowdflower data containing 10 tweets per HIT)



===============================================
		Compensation HIT and Worker Payment
===============================================


    Go to python_scripts directory and run the commands:

    To get the report on the compensation:

        python get_report_based_on_labels.py

    The report is generated in a csv file (/data/hit_report2.csv)



    To create a qualification type, compensation HIT and assigning workers with the qualification in the sandbox environment:

	    python contact_users_compensation_hit.py sandbox

	To create a qualification type, compensation HIT and assigning workers with the qualification in the production environment:

	    python contact_users_compensation_hit.py production



	To monitor the submission of the compensation HIT and to store the HIT information into mongoDB in the sandbox environment:

	    python collect_compensation_hit_results.py sandbox

        nohup python collect_compensation_hit_results.py sandbox & (To execute the script as a background process in the server)

	To monitor the submission of the compensation HIT and to store the HIT information into mongoDB in the production environment:

	    python collect_compensation_hit_results.py production

        nohup python collect_compensation_hit_results.py production & (To execute the script as a background process in the server)



    To pay a worker with worker ID and the compensation amount in sandbox environment:

        python worker_compensation.py sandbox 'WORKERID' 'AMOUNT'

        example: worker_compensation.py sandbox A3VOSKJ5LS9WB 0.10

    To pay a worker with worker ID and the compensation amount in production environment:

        python worker_compensation.py production 'WORKERID' 'AMOUNT'

        example: worker_compensation.py production A3VOSKJ5LS9WB 0.10
