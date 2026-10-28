
# Ansible Role:  `openvpn_exporter`

This ansible role installs and configure [openvpn_exporter](https://github.com/sergeymakinen/openvpn_exporter)


If `latest` is set for `openvpn_exporter_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/opt/openvpn_exporter/${openvpn_exporter_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The openvpn_exporter archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/openvpn_exporter`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `openvpn_exporter_direct_download` to `true`.


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
openvpn_exporter_version: '2.2.3'

openvpn_exporter_system_user:
  owner:  openvpn-exporter
  group: openvpn-exporter

openvpn_exporter_service:
  state: stopped
  enabled: false

openvpn_exporter_config_dir: /etc/openvpn_exporter

openvpn_exporter_release:
  download_url: https://github.com/sergeymakinen/openvpn_exporter/releases
  # file: openvpn_exporter-{{ openvpn_exporter_version }}_{{ ansible_facts.system | lower }}_{{ system_architecture }}.tar.gz
  # binary: openvpn_exporter

openvpn_exporter_service_config:
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
    unit: ""                                        # "openvpn@-.service"
    since: 0s
  openvpn:
    instance: ""                                    # openvpn
  config:
    file: ""

openvpn_exporter_direct_download: false
```

You can also look at the [molecule](molecule/configured/group_vars/all) test.

---

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
