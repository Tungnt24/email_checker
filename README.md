# Email Checker
Email Checker is a simple little API for verifying an email address. It's free and quite easy to use. Just enter the email address and hit the check button. It tells you whether the email id is real or fake

# How do we verify an email?

- First it checks for email address format.
- Then make sure that domain name is valid. We also check whether it’s a disposable email address or not.
- In the final step, It extracts the MX records from the domain records and connects to the email server (over SMTP and also simulates sending a message) to make sure the mailbox really exists for that user/address. Some mail servers do not cooperate in the process, in such cases, the result of this email verification tool may not be as accurate as expected.


# Run Worker

```sh
export PYTHONPATH=$PWD

python workers/celery_app.py 
```

# Run API
```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

# DEMO
```sh
http://103.56.158.197:8000/docs
```