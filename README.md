EXPERIMENTAL - not the default yet


Ansible configuration management for OpenUp
===========================================


Setting up your controller (probably your work laptop)
------------------------------------------------------

```
ansible-galaxy install dokku_bot.ansible_dokku,v2020.1.6
```


Ensuring admins have access to a server
---------------------------------------

```
ansible-playbook --limit hetzner1.openup.org.za users.yml
```

If you're not an admin on the server yet, authenticate with the initial superuser
credentials, e.g. `--user root --ask-pass`

Or you might need to specify an SSH key file for the initial non-root admin user:

    ansible-playbook --limit dokku123-aws.openup.org.za --user=ubuntu --become --key-file ~/.ssh/Bob.pem users.yml


### Add new admins

1. Add their key to the `files` directory
2. Add them to the correct user list

### Adding an admin that should be on all hosts

Add them to `all_hosts_admins` in `users.yml`

### Adding an admin for only specific hosts

Add them to the list `host_extra_admins` for the relevant hosts in `hosts.yaml`


Install dokku
-------------

After creating the server,

1. Add the hostname to the `dokku` group
2. Run the server setup playbook against just the new server:

```
ansible-playbook --limit dokku9.code4sa.org dokku-server.yml
```

Configure cron to email output for error alerts
-----------------------------------------------

Emails sent by the root, ubuntu and dokku users will be configured to "come from" webapps@openup.org.za.

Add `MAILTO=webapps@openup.org.za` at the top of the `crontab -e` file as one of those users. Mails from other users usually end up in spam because it's not setting a `From` header properly.

```
ansible-playbook --limit hetzner1.openup.org.za ssmtp.yml -e "ssmtp_AuthUser=apikey ssmtp_AuthPass=...secret-api-key..."
```

Familiarising yourself with Ansible
-----------------------------------

### Ping all the machines

Not in the network `ping` command sense, just an ansible command that checks that you can connect to them all

In this repo, run

```
ansible all -m ping
```

The result should look something like the following for all hosts:

```
dokku5.code4sa.org | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
dokku6.code4sa.org | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
...
```


### Run an arbitrary command on just the dokkus

Run the following, note we're using `dokkus` referring to the group in `hosts.yml`, and not `all` this time.

```
ansible dokkus -a "echo hello"
```

The output should look something like

```
dokku5.code4sa.org | CHANGED | rc=0 >>
hello

dokku8.code4sa.org | CHANGED | rc=0 >>
hello

dokku7.code4sa.org | CHANGED | rc=0 >>
hello

dokku4.code4sa.org | CHANGED | rc=0 >>
hello

dokku6.code4sa.org | CHANGED | rc=0 >>
hello
```

### Checking what a playbook would do using `--check`

Run with `--check`

```
ansible-playbook --limit dokku9.code4sa.org --check dokku-server.yml
```

Note how it says skipped around each step

```
PLAY [dokkus] ******************************************************************

TASK [Gathering Facts] *********************************************************
The authenticity of host 'dokku9.code4sa.org (18.200.13.154)' can't be established.
ECDSA key fingerprint is SHA256:Dgs79LzpwVgd/q+vlXqsnlOfZTpEGHUBekNCyruTBh8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
ok: [dokku9.code4sa.org]

TASK [Set the timezone for the server to be UTC] *******************************
skipping: [dokku9.code4sa.org]

TASK [Set up a unique hostname] ************************************************
changed: [dokku9.code4sa.org]

PLAY RECAP *********************************************************************
dokku9.code4sa.org         : ok=2    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
```

Best Practises
==============

Prefer declarative style over imperative
----------------------------------------

Prefer approaches that only make a change if needed. The `state: present` style
works this way: tasks that support this will only create something if it doesn't
exist, and will check its existence beforehand.

Name tasks accordingly, e.g _"Redis instance exists"_ instead of _"Create redis instance"
because it won't be creating it if it already exists.