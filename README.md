EXPERIMENTAL - not the default yet

Ansible configuration management for OpenUp
===========================================

Setting up your controller (probably your work laptop)
------------------------------------------------------

```
ansible-galaxy install dokku_bot.ansible_dokku
```

Set up a new dokku server
-------------------------

After creating the server,

1. Add the hostname to the `hosts`
2. Run the server setup playbook against just the new server:

```
ansible-playbook --limit dokku9.code4sa.org --inventory hosts -u ubuntu dokku-server.yml
```


Familiarising yourself with Ansible
-----------------------------------

### Ping all the machines

Not in the network `ping` command sense, just an ansible command that checks that you can connect to them all

In this repo, run

```
ansible all -i hosts -m ping -u ubuntu
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

Run the following, note we're using `dokkus` referring to the group in `hosts`, and not `all` this time.

```
ansible dokkus -i hosts -u ubuntu -a "echo hello"
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
ansible-playbook --limit dokku9.code4sa.org --inventory hosts -u ubuntu --check dokku-server.yml
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