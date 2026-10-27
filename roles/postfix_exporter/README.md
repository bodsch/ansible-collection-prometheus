
# Ansible Role:  `postfix_exporter`

This ansible role installs and configure [postfix_exporter](https://github.com/sergeymakinen/postfix_exporter)


If `latest` is set for `postfix_exporter_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/opt/postfix_exporter/${postfix_exporter_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The postfix_exporter archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/postfix_exporter`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `postfix_exporter_direct_download` to `true`.


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
postfix_exporter_version: '2.2.3'

postfix_exporter_system_user:
  owner:  postfix-exporter
  group: postfix-exporter

postfix_exporter_service:
  state: stopped
  enabled: false

postfix_exporter_config_dir: /etc/postfix_exporter

postfix_exporter_release:
  download_url: https://github.com/sergeymakinen/postfix_exporter/releases
  # file: postfix_exporter-{{ postfix_exporter_version }}_{{ ansible_facts.system | lower }}_{{ system_architecture }}.tar.gz
  # binary: postfix_exporter

postfix_exporter_service_config:
  log:
    level: info
    format: ""
  web:
    listen_address: "127.0.0.1:9907"
    telemetry_path: "/metrics"
    systemd_socket: ""                              # [true, false]
    config:
      file: ""                                      #
  collector: ""
  journald:
    path: ""
    unit: ""                                        # "postfix@-.service"
    since: 0s
  postfix:
    instance: ""                                    # postfix
  config:
    file: ""

postfix_exporter_direct_download: false
```

You can also look at the [molecule](molecule/configured/group_vars/all) test.

---

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
