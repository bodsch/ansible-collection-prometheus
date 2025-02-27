# Ansible Collection - bodsch.prometheus

A collection of Ansible roles for the Prometheus universe. 


[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/main.yml?branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-collection-prometheus)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-collection-prometheus)][releases]

[ci]: https://github.com/bodsch/ansible-collection-prometheus/actions
[issues]: https://github.com/bodsch/ansible-collection-prometheus/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-collection-prometheus/releases


## supported operating systems

* Arch Linux
* Debian based
    - Debian 11 / 12
    - Ubuntu 22.04


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-collection-prometheus/tags)!

---

## Roles

| Role                                                                       | Build State | Description |
|:---------------------------------------------------------------------------| :---- | :---- |
| [bodsch.prometheus.alertmanager](./roles/alertmanager/README.md)           |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/alertmanager.yml?branch=main)][workflow-alertmanager] | Ansible role to install and configure [alertmanager](https://github.com/prometheus/alertmanager). |
| [bodsch.prometheus.am_silence](./roles/am_silence/README.md)               |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/am_silence.yml?branch=main)][workflow-am_silence]| Ansible role to create an alertmanager silence |
| [bodsch.prometheus.docker_sd](./roles/docker_sd/README.md)                 |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/docker_sd.yml?branch=main)][workflow-docker_sd]| Ansible role to install and configure [docker-sd](https://github.com/bodsch/docker-sd). |
| [bodsch.prometheus.promcheck](./roles/promcheck/README.md)                 |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/promcheck.yml?branch=main)][workflow-promcheck]| Ansible role to install and configure [promcheck](https://github.com/cbrgm/promcheck). |
| [bodsch.prometheus.prometheus](./roles/prometheus/README.md)               |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/prometheus.yml?branch=main)][workflow-prometheus]| Ansible role to install and configure [prometheus](https://github.com/prometheus/prometheus). |
| [bodsch.prometheus.pushgateway](./roles/pushgateway/README.md)             |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/pushgateway.yml?branch=main)][workflow-pushgateway]| Ansible role to setup [pushgateway](https://github.com/prometheus/pushgateway). |
| [bodsch.prometheus.trickster](./roles/trickster/README.md)                 |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/trickster.yml?branch=main)][workflow-trickster]| Ansible role to install and configure [Trickster](https://github.com/tricksterproxy/trickster).  |

### Exporters

| Role                                                                       | Build State | Description |
|:---------------------------------------------------------------------------| :---- | :---- |
| [bodsch.prometheus.blackbox_exporter](./roles/blackbox_exporter/README.md) |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/blackbox_exporter.yml?branch=main)][workflow-blackbox_exporter]| Ansible role to install and configure [Prometheus Blackbox Exporter](https://github.com/blackboxinc/blackbox-prometheus-exporter). |
| [bodsch.prometheus.json_exporter](./roles/json_exporter/README.md)         |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/json_exporter.yml?branch=main)][workflow-json_exporter]| Ansible role to install and configure [json_exporter](https://github.com/prometheus-community/json_exporter) |
| [bodsch.prometheus.mysql_exporter](./roles/mysql_exporter/README.md)       |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/mysql_exporter.yml?branch=main)][workflow-mysql_exporter]| Ansible role to install and configure [mysqld_exporter](https://github.com/prometheus/mysqld_exporter). |
| [bodsch.prometheus.nginx_exporter](./roles/nginx_exporter/README.md)       |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/nginx_exporter.yml?branch=main)][workflow-nginx_exporter]| Ansible role to install and configure [Nginx Prometheus Exporter](https://github.com/nginxinc/nginx-prometheus-exporter) |
| [bodsch.prometheus.node_exporter](./roles/node_exporter/README.md)         |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/node_exporter.yml?branch=main)][workflow-node_exporter]| Ansible role to install and configure [node-exporter](https://github.com/prometheus/node_exporter). |
| [bodsch.prometheus.node_exporter_textfile_collectors](./roles/node_exporter_textfile_collectors/README.md) |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/node_exporter_collectors.yml?branch=main)][workflow-node_exporter_collectors]| Ansible role to install and configure external collector scripts for `node_exporter`. |
| [bodsch.prometheus.mongodb_exporter](./roles/mongodb_exporter/README.md)   |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/mongodb_exporter.yml?branch=main)][workflow-mongodb_exporter]| Ansible role to install and configure [mongodb_exporter](https://github.com/prometheus/mongodb_exporter). |
| [bodsch.prometheus.redis_exporter](./roles/redis_exporter/README.md)       |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/redis_exporter.yml?branch=main)][workflow-redis_exporter]| Ansible role to install and configure [redis_exporter](https://github.com/oliver006/redis_exporter) |
| [bodsch.prometheus.ssl_exporter](./roles/ssl_exporter/README.md)           |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/ssl_exporter.yml?branch=main)][workflow-ssl_exporter]| Ansible role to install and configure [SSL Exporter](https://github.com/ribbybibby/ssl_exporter). |
| [bodsch.prometheus.bind_exporter](./roles/bind_exporter/README.md)         |[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-collection-prometheus/bind_exporter.yml?branch=main)][workflow-bind_exporter]| Ansible role to install and configure [Bind Exporter](https://github.com/prometheus/bind_exporter). |

[workflow-alertmanager]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/alertmanager.yml
[workflow-am_silence]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/am_silence.yml
[workflow-blackbox_exporter]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/blackbox_exporter.yml
[workflow-docker_sd]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/docker_sd.yml
[workflow-json_exporter]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/json_exporter.yml
[workflow-mysql_exporter]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/mysql_exporter.yml
[workflow-nginx_exporter]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/nginx_exporter.yml
[workflow-node_exporter]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/node_exporter.yml
[workflow-node_exporter_collectors]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/node_exporter_collectors.yml
[workflow-mongodb_exporter]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/mongodb_exporter.yml
[workflow-promcheck]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/promcheck.yml
[workflow-prometheus]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/prometheus.yml
[workflow-pushgateway]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/pushgateway.yml
[workflow-trickster]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/trickster.yml
[workflow-redis_exporter]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/redis_exporter.yml
[workflow-ssl_exporter]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/ssl_exporter.yml
[workflow-bind_exporter]: https://github.com/bodsch/ansible-collection-prometheus/actions/workflows/bind_exporter.yml

## Modules

### `amtool`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.amtool` | |


### `promtool`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.promtool` | |

### `alertmanager_silence`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.alertmanager_silence` | |


### `alertmanager_templates`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.alertmanager_templates` | |


### `prometheus_alert_rule`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.prometheus_alert_rule` | |


### `prometheus_alert_rules`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.prometheus_alert_rules` | |

## Filters

### `mysql_exporter`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.valid_credentials` | |
| `bodsch.prometheus.has_credentials` | |

### `nginx_exporter`


| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.nginx_exporter_prometheus_labels` | |

### `parse_checksum`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.parse_checksum` | |

### `prometheus`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.validate_file_sd` | |
| `bodsch.prometheus.validate_alertmanager_endpoints` | |
| `bodsch.prometheus.remove_empty_elements` | |
| `bodsch.prometheus.jinja_encode` | |

### `silencer`

| Name  | Description |
| :---- | :---- |
| `bodsch.prometheus.expired` | |
| `bodsch.prometheus.current_datetime` | |
