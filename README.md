To use automated login

Requirement:

-gmail account ASSOCIATED with Robinhodd

Steps:
1. go to https://developers.google.com/gmail/api/quickstart/python
2. click "Enable the Gmail API"
3. put credentials.json (downloaded upon clicking "Enable Gmail API") in "run" directory
4. run  "pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"
5. create login.ini in "run" directory
6. add [ROBINHOOD] section to login.ini
7. in [ROBINHOOD] section add your username and password as keys (ie: username = your_username)
8. add [GMAIL] section to login.ini
9. in [GMAIL] section add your gmail (ie: gmail = gmail@gmail.com)
10. log out and forget all other gmail accounts besides your robinhood account in chrome
11. run AND approve login for first run

After approving the first time, will not need to approve again