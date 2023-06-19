
# Ansible Role:  `blackbox_exporter`

Ansible role to install and configure [Prometheus Blackbox Exporter](https://github.com/blackboxinc/blackbox-prometheus-exporter).

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-blackbox_exporter/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-blackbox_exporter)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-blackbox_exporter)][releases]
[![Ansible Quality Score](https://img.shields.io/ansible/quality/50067?label=role%20quality)][quality]

[ci]: https://github.com/bodsch/ansible-blackbox_exporter/actions
[issues]: https://github.com/bodsch/ansible-blackbox_exporter/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-blackbox_exporter/releases
[quality]: https://galaxy.ansible.com/bodsch/blackbox_exporter


If `latest` is set for `blackbox_exporter_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/bin/blackbox_exporter/${blackbox_exporter_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The blackbox_exporter archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/blackbox_exporter`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `blackbox_exporter_direct_download` to `true`.

## Requirements & Dependencies

Ansible Collections

- [bodsch.core](https://github.com/bodsch/ansible-collection-core)
- [bodsch.scm](https://github.com/bodsch/ansible-collection-scm)

```bash
ansible-galaxy collection install bodsch.core
ansible-galaxy collection install bodsch.scm
```
or
```bash
ansible-galaxy collection install --requirements-file collections.yml
```

## Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 10 / 11
    - Ubuntu 20.10


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-blackbox_exporter/tags)!

## Configuration

```yaml
blackbox_exporter_version: '0.24.0'
blackbox_exporter_blackbox_plus: false

blackbox_exporter_system_group: blackbox-exporter
blackbox_exporter_system_user: "{{ blackbox_exporter_system_group }}"
blackbox_exporter_config_dir: /etc/blackbox_exporter

blackbox_exporter_direct_download: false

blackbox_exporter_service: {}

blackbox_exporter_release: {}

blackbox_exporter_modules: {}
```


----

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
