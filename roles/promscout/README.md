# Ansible Role:  `bodsch.prometheus.promscout`

Ansible role to install and configure [promscout](https://github.com/bodsch/promscout).


If `latest` is set for `promscout_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/opt/promscout/${promscout_version}` and later linked to `/usr/sbin`. 
This should make it possible to downgrade relatively safely.

The Source archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/promscout`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `promscout_direct_download` to `true`.

## Configuration

```yaml
promscout_version: "1.0.1"

promscout_system_user: promscout
promscout_system_group: promscout
promscout_config_dir: /etc/promscout

promscout_direct_download: false

promscout_release: {}

# CIDR network that will be scanned for Prometheus exporters.
# Example: 192.168.0.0/24, 10.10.0.0/16
promscout_network_cidr: ""

# List of TCP ports that should be scanned.
# Extend this list for custom exporters.
promscout_ports:
  - 9100

# Ordered list of paths to check for Prometheus metrics.
# The first successful match will be used.
promscout_metrics_paths:
  - /metrics

# Interval between discovery cycles.
# Uses Go duration format.
promscout_interval: "5m"

# Timeout for TCP dial and HTTP validation.
promscout_timeout: 3s

# HTTP address where this service exposes the HTTP-SD endpoint.
promscout_listen: "127.0.0.1:9099"

# Maximum number of parallel scanning workers.
promscout_max_workers: 50

# Log level: debug | info | error
promscout_log_level: info
```

---

## Author and License

- Bodo Schulz
