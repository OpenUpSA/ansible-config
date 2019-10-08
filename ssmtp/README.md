Role Name
=========

Ansible role to setup ssmtp mail transfer agent for Ubuntu Bionic (18.04 LTS) and configure crond to notify operator via email after a job is run.

Requirements
------------

1. Privileged (root) access to the host system.
2. Host system with Ubuntu Bionic installed.

Role Variables
--------------

```
ssmtp:
  root: Default user that receives all outgoing email, default - "root@localhost"
  hostname: Full hostname of the machine , default - "{{ ansible_hostname }}"
  rewrite_domain: Domain where the mail appears to come from, default "localhost"
  mailhub: Default "smtp.sendgrid.net:587"
  FromLineOverride: Email 'From header's can override the default domain? default - "NO"
  AuthUser: Username for smtp server, default - ""
  AuthPass: Password for smtp server, default - ""
  AuthMethod: Authentication method, default - "LOGIN"
  UseTLS: Whether to use TLS, default - "YES"
  UseSTARTTLS: Whether to use Start TLS, required for sendgrid - default "YES"
  aliases: List of UNIX user aliases, default - "[]"
crond:
  MAILTO: Email address to notify after job exit, default -  "root@localhost"
```
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

```
- hosts: "{{ hosts | default('localhost') }}"
  remote_user: "{{ ruser | default('linas') }}"
  become: yes
  become_method: sudo
  roles:
  - role: ssmtp
```