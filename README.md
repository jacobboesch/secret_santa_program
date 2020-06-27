# secret_santa_program

This program is designed to select people for gift giving this christmas. 

The rules for selection are as follows:
1. Family members in the same household can't get each other as secret santa
2. You can't get yourself as a secret santa. 
3. All family members are emailed the name of the person they are shopping for. 
4. You can't get the same person you had the previous year

I've made this program a REST API, just incase I wanted to make 
a front end for it in the future. 

Required Environment Variables:
* SECRET_SANTA_DB_CONNECTION_STRING
* SECRET_SANTA_SENDER_EMAIL
* SECRET_SANTA_SENDER_PASSWORD

Setup:

Install python virtual enviornment and source in. 

Then install the required packages using pip3. 

pip3 -r install requirements.txt

To run the program use the following command:

python3 app.py

Additional Notes:

This is a working prototype of the product.
The program works, and can be hosted on your local machine. 
This program is NOT ready to be placed on a production server.
To address this problem the following additions will be made in a 
future update:

1. Redesign the database schema to allow for user accounts
2. Modify the algorithm to only select names from family members associated
with a persons account. 
3. Create account authorization using OAuth 2.0
4. Design and create a front end for the product using TypeScript and Semantic UI
5. Register a domain name, and obtain and SSL certificate using letsencrypt
6. Document endpoints using swagger
7. Create database migration scripts using alembic
8. Create integration tests using behave

Other possible future additions:
- Add support for custom exclusions
- Add the ability to add whish lists to the email
