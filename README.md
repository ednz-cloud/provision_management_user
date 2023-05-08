Provision ansible user
=========
> This repository is only a mirror. Development and testing is done on a private gitlab server.

This role configures the ansible service user on **debian-based** distributions.

Requirements
------------

None.

Role Variables
--------------
Available variables are listed below, along with default values. A sample file for the default values is available in `default/provision_ansible_user.yml.sample` in case you need it for any `group_vars` or `host_vars` configuration.

```yaml
provision_ansible_user_name: ansible # by default, set to ansible
```
This variable sets the name to configure for the service account.

```yaml
provision_ansible_user_group: ansible # by default, set to ansible
```
This variable sets the primary group to configure for the service account.

```yaml
provision_ansible_user_password: "*" # by default, set to *
```
This variable sets the password of the account, by default, it is set to "*", which means password authentication is disabled.

```yaml
provision_ansible_user_is_system: true # by default, set to true
```
This variable describe whether the account should be a system user or not. Default (and recommended) is `true`.

```yaml
provision_ansible_user_home: /opt/{{ provision_ansible_user_name }} # by default, set to /opt/{{ provision_ansible_user_name }}
```
This variable sets the home for the service account. By default the home of the account is set in /opt/.

```yaml
provision_ansible_user_shell: /bin/bash # by default, set to /bin/bash
```
This variable sets the shell to be used by the account. Defaults to bash.

```yaml
provision_ansible_user_sudoer: false # by default, set to false
```
This variable defines if the user should be root. For security reasons, this defaults to `false`, but should probably be `true` in a real world scenario.

```yaml
provision_ansible_user_add_ssh_key: false # by default, set to false
```
This variable defines if ssh_keys should be added to the authroized_keys file for the user. Defaults to `false` because there is no "default" ssh_key. This should be set to true and a key passed to the role.

```yaml
provision_ansible_user_ssh_key: # by default, not set
```
This variable contains the ssh public key to use by ansible to log in the service account. Defaults to `None`, but should be set by the operator, and preferably obfuscated (see examples).

```yaml
provision_ansible_user_ssh_key_options: "" # by default, set to ""
```
This variable sets the potential ssh options to add in the authorized_keys file. Default to no options.

```yaml
provision_ansible_user_ssh_key_exclusive: true # by default, set to true
```
This variable defines if the ssh public key passed above should be the only key to log into this account. For security reasons, it is recommended that this gets set to `true`.

Dependencies
------------

None.

Example Playbook
----------------

```yaml
# calling the role inside a playbook with either the default or group_vars/host_vars
- hosts: servers
  roles:
    - ednxzu.provision_ansible_user
```

```yaml
# calling the role inside a playbook with just-in-time provisioning of the ssh public key, and vault storage
- hosts: servers
  tasks:
    - name: "Dynamic ssh keys generation"
      delegate_to: localhost
      block:
        - name: "Generate a keypair for {{ ansible_hostname }}"
          community.crypto.openssh_keypair:
            path: "/tmp/id_ed25519_{{ ansible_hostname }}"
            type: ed25519
            owner: root
            group: root
          delegate_to: localhost
          register: _keypair

        - name: "Write the private and public key to vault"
          community.hashi_vault.vault_write:
            url: https://vault.domain.tld
            path: "ansible/hosts/{{ inventory_hostname }}"
            data:
              private_key: "{{ lookup('ansible.builtin.file', '/tmp/id_ed25519_' ~ ansible_hostname ) }}\n"
              public_key: "{{ _keypair.public_key }}"
          delegate_to: localhost

        - name: "Remove private_key files"
          ansible.builtin.file:
            path: "/tmp/id_ed25519_{{ ansible_hostname }}"
            state: absent
          delegate_to: localhost

    - name: "Provision ansible user"
      ansible.builtin.include_role:
        name: ednxzu.provision_ansible_user
      vars:
        provision_ansible_user_add_ssh_key: true
        provision_ansible_user_ssh_key: "{{ _keypair.public_key }}"
```

License
-------

MIT / BSD

Author Information
------------------

This role was created by Bertrand Lanson in 2023.