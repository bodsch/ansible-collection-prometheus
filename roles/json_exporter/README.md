
# Ansible Role:  `json_exporter`

This ansible role installs and configure [json_exporter](https://github.com/prometheus-community/json_exporter)


If `latest` is set for `json_exporter_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/opt/json_exporter/${json_exporter_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The json_exporter archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/json_exporter`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `json_exporter_direct_download` to `true`.


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
json_exporter_version: '0.6.0'

json_exporter_release: {}

json_exporter_system_group: json-exporter
json_exporter_system_user: json-exporter
json_exporter_config_dir: /etc/json_exporter

json_exporter_direct_download: false

json_exporter_service: {}

json_exporter_config: []

json_exporter_modules: {}
```

### `json_exporter_service`

#### defaults

```yaml
json_exporter_service:
  config:
    file: "{{ json_exporter_config_dir }}/config.yml"
  log:
    level: info
    format: ""
  web:
    listen_address: "0.0.0.0:7979"
```

### `json_exporter_config`

> **This variable is OBSOLETE and has been replaced by `json_exporter_modules`!**

The entries of `json_exporter_config` are currently being converted to the new format.

#### defaults

```yaml
json_exporter_config: []
```

#### example

```yaml
json_exporter_config:
  - name: example_global_value
    help: Example of a top-level global value scrape in the json
    path: "{ .counter }"
    labels:
      environment: beta                   # static label
      location: "planet-{.location}"      # dynamic label

  - name: mgob_backup
    help: MongoDB Backup
    type: object
    path: "{}"
    labels:
      environment: DEV                    # static label
      id: '{[].plan}'                     # dynamic label
    values:
      next_run: "{[].next_run}"
      last_run: "{[].last_run}"
      last_run_status: "{[].last_run_status}"
```

### `json_exporter_modules`

All possible parameters can be found in the [original documentation](https://github.com/prometheus-community/json_exporter/blob/master/examples/config.yml).

The [tests](molecule/configured/group_vras/all/vars.yml) run with an adapted version of this configuration.


#### defaults

```yaml
json_exporter_modules: {}
```

#### example

```yaml
json_exporter_modules:

  jellyfin:
    headers:
      Authorization: MediaBrowser Token=xxxxxxxxxxxxxxxxx
      Content-Type: application/json
      accept: application/json

    metrics:
      - name: jellyfin
        type: object
        help: User playback metrics from Jellyfin
        path: '{ [*] }'
        labels:
          user_name: '{ .UserName }'
          # User PromQL label_join and label_replace to concatenate
          # these values into a nice item description
          item_type: '{ .NowPlayingItem.Type }'
          item_name: '{ .NowPlayingItem.Name }'
          item_path: '{ .NowPlayingItem.Path }'
          series_name: '{ .NowPlayingItem.SeriesName }'
          episode_index: 'e{ .NowPlayingItem.IndexNumber }'
          season_index: 's{ .NowPlayingItem.ParentIndexNumber }'
          client_name: '{ .Client }'
          device_name: '{ .DeviceName }'
        values:
          is_paused: '{ .PlayState.IsPaused }'

  animals:
    metrics:
      - name: animal
        type: object
        help: Example of top-level lists in a separate module
        path: '{ [*] }'
        labels:
          name: '{ .noun }'
          predator: '{ .predator }'
        values:
          population: '{ .population }'
    http_client_config:
      tls_config:
        insecure_skip_verify: true
      basic_auth:
        username: myuser
        password: veryverysecret
        # password_file: /tmp/mysecret.txt
    valid_status_codes:
      - 200
      - 204
    body:
      content: !unsafe
        '{"time_diff": "{{ duration `95` }}","anotherVar": "{{ .myVal | first }}"}'
      templatize: true
```

You can also look at the [molecule](molecule/default/group_vars/all) test.


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-json-exporter/tags)!

---

## Author and License

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
