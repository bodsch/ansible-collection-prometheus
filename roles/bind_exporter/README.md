
# Ansible Role:  `bind_exporter`

This ansible role installs and configure [bind_exporter](https://github.com/prometheus-community/bind_exporter)


If `latest` is set for `bind_exporter_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/opt/bind_exporter/${bind_exporter_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The bind_exporter archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/bind_exporter`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `bind_exporter_direct_download` to `true`.


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
    - Debian 10 / 11 / 12
    - Ubuntu 20.04 / 22.04

## Usage

```
bind_exporter_version: '0.8.0'

bind_exporter_release: {}

bind_exporter_system_group: bind-exporter
bind_exporter_system_user: bind-exporter

bind_exporter_direct_download: false

bind_exporter_service: {}
```

### `bind_exporter_service`

#### defaults

```yaml
bind_exporter_service:
  web:
    listen_address: "127.0.0.1:9119"                # Addresses on which to expose metrics and web interface. Repeatable for multiple addresses.
    telemetry_path: "/metrics"                      # Path under which to expose metrics
    systemd_socket: false                           # Use systemd socket activation listeners instead of port listeners (Linux only).
  bind:
    stats_url: ""                                   # http://localhost:8053/
    timeout: 10s                                    # Timeout for trying to get stats from BIND server
    pid_file: "/run/named/named.pid"                # Path to BIND's pid file to export process information
    stats_version: auto                             # BIND statistics version. Can be detected automatically.
    stats_groups:                                   # List of statistics to collect
      - server
      - view
      - tasks
```

You can also look at the [molecule](molecule/configured/group_vars/all) test.


## Contribution

Please read [Contribution](CONTRIBUTING.md)

---

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
