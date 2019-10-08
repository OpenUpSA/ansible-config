Ansible role to setup ssmtp mail transfer agent for Ubuntu Bionic (18.04 LTS) and configure crond to notify operator via email after a job is run.

Requirements  

1. Privileged (root) access to the host system.
2. Host system with Ubuntu Bionic installed.

Role Variables

```

ssmtp_root: Default user that receives all outgoing email, default - "root@localhost"
ssmtp_hostname: Full hostname of the machine , default - "{{ ansible_hostname }}"
ssmtp_rewrite_domain: Domain where the mail appears to come from, default "localhost"
ssmtp_mailhub: Default "smtp.sendgrid.net:587"
ssmtp_FromLineOverride: Email 'From header's can override the default domain? default - "NO"
ssmtp_AuthUser: Username for smtp server, default - ""
ssmtp_AuthPass: Password for smtp server, default - ""
ssmtp_AuthMethod: Authentication method, default - "LOGIN"
ssmtp_UseTLS: Whether to use TLS, default - "YES"
ssmtp_UseSTARTTLS: Whether to use Start TLS, required for SendGrid - default "YES"
ssmtp_aliases: List of UNIX user aliases, default - "[]"
crond_MAILTO: Email address to notify after job exit, default -  "root@localhost"

```

Example Playbook

```
- hosts: "{{ hosts | default('localhost') }}"
  remote_user: "{{ ruser | default('linas') }}"
  become: yes
  become_method: sudo
  roles:
  - role: ssmtp
```

Example Usage

`ansible-playbook ssmtp.yml -e "hosts=localhost smtp_AuthUser=myverysecretuser smtp_AuthPass=myverysecretpassword"`
