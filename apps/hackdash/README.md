# Hackdash for codebridge

1. ansible-playbook
2. mongo
3. git push to dokku repo
4. letsencrypt


## Manual steps


### mongo

```
MONGO_IMAGE_VERSION=4.1.8-xenial dokku mongo:create hackdash
dokku mongo:link  hackdash hackdash --alias DATABASE_URL
```

### letsencrypt

... dokku:letsencrypt ...
