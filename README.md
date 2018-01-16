# How to install

## Follow analysts
```
cat analysts.txt
```

## and configure logstash.

```
$ sudo pip install -r requirements.txt
$ python generate.py CONSUMER_KEY CONSUMER_SECRET OAUTH_TOKEN OAUTH_TOKEN_SECRET OWNER_SCREEN_NAME LIST_NAME | sudo tee /etc/logstash/conf.d/logstash-twitter.conf
```
