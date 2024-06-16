# filter-it
Simple rule based filter and updater for gmail
## Description
- Fetches new emails
- Parses and applies rules from rules.json
## Steps
1. Install dependencies `pip install -r requirements.txt`
2. Install postgresql@15 `brew install postgresql@15`
3. Start postgresql service `brew services start postgresql@15`
3. Create db and user and update the config file `utils/config`
4. Enable GmailAPI and download `credentials.json` from google cloud console into the project directory
4. Run using the command `python filterit.py`


