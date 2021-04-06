# secret_santa_program

This program is the backend for the Secret Santa App. 
It has been updated to have only one endpoint that is responsible for 
sending emails to selected giftees. The database and selection algorithm
has been moved to the Secret Santa App. 

Required Environment Variables:
* SECRET_SANTA_SENDER_EMAIL
* SECRET_SANTA_SENDER_PASSWORD

Setup:

Install python virtual environment and source in. 

Then install the required packages using pip3. 

pip3 -r install requirements.txt

To run the program use the following command:

python3 app.py

Additional Notes:

The program currently works as is and can be run on your local machine.

Before placing this program on a production server the following updates still
need to be made:

1. JSON validation on the email participants endpoint
2. Secure endpoints and email sending with HTTPS
3. Write unit tests for existing code