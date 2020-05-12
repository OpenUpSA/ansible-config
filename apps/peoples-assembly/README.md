People's Assembly
=================

1. elasticsearch
2. rabbitmq
3. pombola
  a. postgres
  b. app
4. writeinpublic
  a. rabbitmq
  b. postgres
  c. app


elasticsearch
-------------

We follow the [Dokku image deployment using tags](http://dokku.viewdocs.io/dokku/deployment/methods/images/#deploying-from-a-docker-registry) approach.

Create and configure the app using ansible

    ansible-playbook --start-at-task "Dokku app exists" --inventory inventory/prod.yml apps/peoples-assembly/elasticsearch.yml

Pull the image on the server

    docker pull elasticsearch:1

Tag the image with the app name

    docker tag elasticsearch:1 dokku/elasticsearch-1:latest

Create a docker network and configure dokku to attach elasticsearch instances to it on deploy

    dokku network:create elasticsearch-1
    dokku network:set elasticsearch-1 attach-post-deploy elasticsearch-1

Now you can depoy the app

    dokku tags:deploy elasticsearch-1 latest

In a single-node cluster, replicas will never be assigned, so status will always be yellow.

To disable replicas and get status green, wait until your apps have created their indexes, then set number of replicas to zero:

Get a shell that can connect to elasticsearch with curl, e.g.

    docker exec -ti elasticsearch-1.web.1 bash

Configure zero replicas via that shell

    curl -XPUT localhost:9200/_settings -d '{ "index": { "number_of_replicas" : 0 } }'


writeinpublic
-------------

    ansible-playbook --inventory inventory/prod.yml apps/peoples-assembly/writeinpublic.yml

Configure worker and beat instances to run: On the server:

    dokku ps:scale writeinpublic  web=1 worker=1 beat=1

### Configure rabbitmq

    dokku rabbitmq:link writeinpublic writeinpublic --alias CELERY_BROKER_URL


### Configure elasticsearch

Attach writeinpublic instances to the elasticsearch-1 network on creation

    dokku network:set writeinpublic attach-post-create elasticsearch-1

Rebuild the elasticsearch index

    dokku --rm run writeinpublic python manage.py rebuild_index