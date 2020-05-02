CKAN for OpenUp's Data Portal
=============================


    docker network create --internal openup-ckan


Set up SOLR
-----------

    dokku apps:create openup-ckan-solr
    dokku proxy:disable openup-ckan-solr


Set up Redis
------------

    dokku redis:create openup-ckan


Set up CKAN
-----------

1. Ensure the app exists and is configured

    ansible-playbook --inventory inventory/prod.yml  --limit hetzner1.openup.org.za --start-at-task "Dokku app exists" apps/openup-ckan/ckan.yml


2. Add the git remote to your local clone of the [Dockerfile deployment repository](https://github.com/openupsa/openup-ckan) as per the remote shown by the playbook.

3. Link CKAN to SOLR and Redis

    dokku redis:link --alias=CKAN_REDIS_URL openup-ckan openup-ckan
    dokku docker-options:add openup-ckan run,deploy --link ckan-solr.web.1:solr

4. Push the Dockerfile deployment repository master branch to the dokku git remote.

5. Initialise the database

    dokku --rm run openup-ckan paster --plugin=ckan db init -c ckan.ini