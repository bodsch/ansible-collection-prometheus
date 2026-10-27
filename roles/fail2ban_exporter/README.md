
# Ansible Role:  `fail2ban_exporter`

This ansible role installs and configure [fail2ban_exporter](https://github.com/NightSquawk/fail2ban-prometheus-exporter)


If `latest` is set for `fail2ban_exporter_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/opt/fail2ban_exporter/${fail2ban_exporter_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The fail2ban_exporter archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/fail2ban_exporter`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `fail2ban_exporter_direct_download` to `true`.


## Requirements & Dependencies

Ansible Collections

- [bodsch.core](https://github.com/bodsch/ansible-collection-core)

```bash
ansible-galaxy collection install bodsch.core
```
or
```bash
ansible-galaxy collection install --requirements-file collections.yml
```


### Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian  12 / 13
    - Ubuntu 22.04 / 24.04

## Usage

```
fail2ban_exporter_version: 1.0.0-beta

fail2ban_exporter_system_user:
  owner:  root
  group: root

fail2ban_exporter_service:
  state: stopped
  enabled: false

fail2ban_exporter_config_dir: /etc/fail2ban_exporter

fail2ban_exporter_release: {}
  # download_url: https://github.com/NightSquawk/fail2ban-prometheus-exporter/releases
  # file: fail2ban_exporter-{{ fail2ban_exporter_version }}_{{ ansible_facts.system | lower }}_{{ system_architecture }}.tar.gz
  # binary: fail2ban_exporter

fail2ban_exporter_service_config:
  web:
    listen_address: "127.0.0.1:9191"
    basic_auth:
      username: ""
      password: ""
  collector:
    f2b:
      socket: ""
      exit_on_socket_connection_error: ""
      textfile:
        directory: ""
  geo:
    enabled: false
    db_path: ""
    provider: "maxmind"

fail2ban_exporter_direct_download: false
```

You can also look at the [molecule](molecule/configured/group_vars/all) test.

---

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
