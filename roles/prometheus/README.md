
# Ansible Role:  `prometheus` 

Ansible role to install and configure [prometheus](https://github.com/prometheus/prometheus).


If `latest` is set for `prometheus_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/opt/prometheus/${prometheus_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The Prometheus archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/prometheus`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `prometheus_direct_download` to `true`.

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

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-prometheus/tags)!

## Configuration

```yaml
prometheus_version: 2.35.0

prometheus_release_download_url: https://github.com/prometheus/prometheus/releases

prometheus_system_user: prometheus
prometheus_system_group: prometheus
prometheus_config_dir: /etc/prometheus
prometheus_data_dir: /var/lib/prometheus

prometheus_direct_download: false

prometheus_service: {}

prometheus_global: {}

prometheus_alerting: {}

prometheus_rule_files: []

prometheus_alert_rules: {}

prometheus_scrape_configs: []

prometheus_remote_write: []

prometheus_remote_read: []

prometheus_storage: {}

prometheus_tracing: {}

prometheus_file_sd_targets: {}
```

### `prometheus_service`

Configures the command line parameters of Prometheus.  
These are stored in the file `/etc/conf.d/prometheus` or `/etc/defaults/prometheus` and used by the start script.  
All parameters can be called via `prometheus --help`.


```yaml
prometheus_service:
  log:
    level: info
    format: ""
  # See https://prometheus.io/docs/prometheus/latest/feature_flags/
  features: []
  storage:
    tsdb:
      path: /var/lib/prometheus
      retention:
        time: 15d
        size: ""
  web:
    # [EXPERIMENTAL]
    # Path to configuration file that can enable TLS or authentication.
    config:
      file: ""
    console:
      libraries: ""
      templates: ""
    cors:
      origin:
    enable_lifecycle: false
    enable_remote_write_receiver: false
    enable_admin_api: false
    external_url: ""
    listen_address: "0.0.0.0:9090"
    max_connection: ""
    page_title: ""
    read_timeout: ""
    route_prefix: ""
    user_assets: ""
  raw_flags: {}
```

### `prometheus_global`


```yaml
prometheus_global:
  scrape_interval: 1m
  scrape_timeout: 10s
  evaluation_interval: ""
  external_labels: {}
  query_log_file: ""
```

#### example

```yaml
prometheus_global:
  scrape_interval: 5m
  evaluation_interval: 2m
  external_labels:
    environment: MOLECULE
    production: not
```


### `prometheus_alerting`

- [relabel_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#relabel_config)
- [alertmanager_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#alertmanager_config)


```yaml
# Alerting specifies settings related to the Alertmanager.
alerting:
  alert_relabel_configs:
    [ - <relabel_config> ... ]
  alertmanagers:
    [ - <alertmanager_config> ... ]
```

#### example

Currently only `static_config` is supported!  
If another service discopvery should be supported, please write an issue or submit a pull request!

```yaml
prometheus_alerting:
  alertmanagers:
    - scheme: http
      timeout: 10s
      api_version: ""
      path_prefix: "/"
      static_configs:
        - targets:
            - localhost
          labels:
            can_ignored: true
```

##### `prometheus_alert_rules`

All rules that can trigger an alarm are defined under `prometheus_alert_rules`.  

Each entry kept under `name` is saved as a separate file.  
This makes it possible to set up a structured configuration for different environments.


> Go templates offer a similar syntax to Jinja2.  
> Therefore, it is difficult to transfer them cleanly via Ansible to the target system.  
> You can transfer the templates as base64 coded strings, but then you have to take
> care of decoding them yourself.  
> This always requires more effort in the form of a separate module.
>
> Alternatively, you can mark the corresponding string with [`!unsafe`](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_advanced_syntax.html#unsafe-or-raw-strings).
>
> Ansible can handle this. But then the molecule tests fail!
>
> Yes, you could also use `{% raw %}{% endraw %}`, but then filters like `combine()`
> are no longer usable.

Here is an example of how to use unsafe:

```yaml
prometheus_alert_rules:
  - name: ops
    rules:
      watchdog:
        alert: Watchdog
        expr: vector(1)
        for: 10m
        labels:
          severity: information
        annotations:
          description: |
            This is an alert meant to ensure that the entire alerting pipeline is functional.
            This alert is always firing, therefore it should always be firing in Alertmanager
            and always fire against a receiver.
            There are integrations with various notification mechanisms that send a notification when this alert is not firing.
            For example the

            "DeadMansSnitch" integration in PagerDuty.

          summary: 'Ensure entire alerting pipeline is functional'
      #
      instance_down:
        # state: absent
        alert: InstanceDown
        # Condition for alerting
        expr: up == 0
        for: 1m
        # Annotation - additional informational labels to store more information
        annotations: !unsafe
          notes: "prometheus.matrix.lan"
          title: 'Instance {{ $labels.instance }} down'
          description: '{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 1 minute.'
        # Labels - additional labels to be attached to the alert
        labels:
          severity: 'critical'

  - name: prometheus
    rules:
      prometheus_job_missing:
        # state: absent
        alert: PrometheusJobMissing
        expr: !unsafe 'absent(up{job="prometheus"})'
        for: 0m
        labels:
          severity: warning
        annotations: !unsafe
          summary: 'Prometheus job missing (instance {{ $labels.instance }})'
          description: 'A Prometheus job has disappeared\n  VALUE = {{ $value }}\n  LABELS = {{ $labels }}'
```

For more examples, check out the [molecule test](molecule/configured/group_vars/all/alert_rules.yml).


### `prometheus_rule_files`

```yaml
# Rule files specifies a list of globs. Rules and alerts are read from
# all matching files.
rule_files:
  [ - <filepath_glob> ... ]
```

#### example

```yaml
prometheus_rule_files:
  - foo.yml
  - bar.json
```

### `prometheus_scrape_configs`

The original documentation is detailed enough.  
Please read!  
A fully resolved version of a scrape_config is available in the template [scrape_configs.j2](templates/prometheus/prometheus.d/scrape_configs.j2) can be seen.

- [scrape_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#scrape_config)
- [file_sd_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#file_sd_config)

```yaml
# A list of scrape configurations.
prometheus_scrape_configs:
  [ - <scrape_config> ... ]
```

#### example:


```yaml
prometheus_scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets:
          - "{{ ansible_fqdn | default(ansible_host) | default('localhost') }}:9090"
  #
  - job_name: grafana
    static_configs:
      - targets:
        - grafana.matrix.lan:3000
  #
  - job_name: node
    file_sd_configs:
      - files:
          - "{{ prometheus_config_dir }}/file_sd/node.yml"
        refresh_interval: 2m
```


### `prometheus_remote_write`

- [remote_write](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write)

```yaml
prometheus_remote_write:
  - url: http://10.18.0.2:9190/api/v1/write
    basic_auth:
      username: 'your-username'
      password: 'your-password'
    queue_config:
      capacity: 5000
      max_shards: 10
      max_samples_per_send: 1000
      batch_send_deadline: 5s
      min_backoff: 30ms
      max_backoff: 100ms
```

### `prometheus_remote_read`

- [remote_read](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read)

```yaml
prometheus_remote_read:
  - url: 'https://10.18.0.2:9190/api/v1/read'
    basic_auth:
      username: 'your-username'
      password: 'your-password'
```

### `prometheus_storage`

- [exemplars](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#exemplars)

```yaml
# Storage related settings that are runtime reloadable.
storage:
  [ - <exemplars> ... ]
```

### `prometheus_tracing`

- [tracing_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#tracing_config)

```yaml
# Configures exporting traces.
tracing:
  [ <tracing_config> ]
```

### `prometheus_file_sd_targets`

Creates static files for the `file_sd_config`.  
These files are created below `/etc/prometheus/file_sd`.  
These files are then referenced in `prometheus_scrape_configs` (under `file_sd_configs`. see above).  
If it is not possible to resolve a reference, an error is issued when the role runs and the run is aborted.

```yaml
prometheus_file_sd_targets:
  node:
    - targets:
        - localhost:9100
      labels:
        env: test
  grafana:
    - targets:
       - grafana:3000
      label:
        env: ops
        application: grafana
```
---


## Federation

As you already guess in this way your Prometheus will collect only time series whose metric names 
have `dht_` , `node_` or `container_` prefix.

And all jobs with `sensors` tag.


Config for federate service:

```yaml
prometheus_scrape_configs:
  - job_name: federate
    scrape_interval: 15s

    honor_labels: true
    metrics_path: '/federate'

    params:
      'match[]':
        - 'up'
        - '{ __name__ =~ "dht_.* | node_.* | container_.*" }'
        - '{ job = "sensors" }'

    static_configs:
      - targets:
        - 'instance:9090'
```


## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
