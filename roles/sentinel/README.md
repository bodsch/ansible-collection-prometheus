
# Ansible Role:  `sentinel`

This ansible role installs and configure [sentinel](https://github.com/bodsch/sentinel)


If `latest` is set for `sentinel_version`, the role tries to install the latest release version.  
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/opt/sentinel/${sentinel_version}` and later linked to `/usr/bin`. 
This should make it possible to downgrade relatively safely.

The sentinel archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`. 
By default it is `${HOME}/.cache/ansible/sentinel`.
If this type of installation is not desired, the download can take place directly on the target system. 
However, this must be explicitly activated by setting `sentinel_direct_download` to `true`.

## Usage

```
sentinel_version: '0.9.0'

sentinel_release: {}

sentinel_system_group: sentinel
sentinel_system_user: sentinel
sentinel_config_dir: /etc/sentinel

sentinel_direct_download: false

sentinel_service:
  listen: "127.0.0.1:8080"
  log:
    format: "json"
    level: "info"

sentinel_defaults: {}
sentinel_targets: []
```

### `sentinel_service`

#### defaults

```yaml
sentinel_service:
  listen: "127.0.0.1:8080"
  log:
    format: "json"
    level: "info"
```

### `sentinel_defaults`

#### defaults

```yaml
sentinel_defaults:
  interval: 30s                                       # how often each target is probed
  timeout: 10s                                        # total per-run timeout (covers all redirect hops)
  http:
    method: GET                                       # GET, HEAD, POST, PUT, PATCH or DELETE
    follow_redirects: true
    max_redirects: 10
    max_body_bytes: 1048576                           # 1 MiB cap on the body read (DoS safeguard)
```

#### example

```yaml
sentinel_defaults:
  interval: 30s                                       # how often each target is probed
  timeout: 10s                                        # total per-run timeout (covers all redirect hops)
  http:
    method: GET                                       # GET, HEAD, POST, PUT, PATCH or DELETE
    follow_redirects: true
    max_redirects: 10
    max_body_bytes: 1048576                           # 1 MiB cap on the body read (DoS safeguard)
```

### `sentinel_targets`


#### defaults

```yaml
sentinel_targets: []
```

#### example

```yaml
sentinel_targets:
  - name: homepage
    description: "Minimal target: inherits every default, expects HTTP 200."
    http:
      url: https://example.org

  - name: docs-availability
    description: "Cheap availability + TLS check using HEAD (no body downloaded)."
    interval: 5m
    tags:
      service: documentation
      environment: production
    http:
      url: https://docs.example.org/
      method: HEAD

  - name: dns-a-record
    description: "DNS target: resolve an A record via a specific resolver and check it."
    interval: 30s
    tags:
      service: dns
      environment: production
    dns:
      server: 1.1.1.1
      query: example.org
      type: A
      expected:
        - 93.184.216.34

  # Compatibility check: does the endpoint still serve TLS 1.2 clients? Pair it
  # with an uncapped target on the same endpoint to see the whole picture.
  - name: tls12-compatibility
    interval: 5m
    tags:
      service: web
      environment: production
    tls:
      host: www.example.org
      port: 443
      max_version: "1.2"
```

You can also look at the [molecule](molecule/default/group_vars/all) test.

---

## Author and License

- Bodo Schulz
