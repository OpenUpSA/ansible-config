Ansible configuration management for OpenUp
===========================================

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
