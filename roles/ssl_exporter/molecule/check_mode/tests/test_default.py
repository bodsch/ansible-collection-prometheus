
from __future__ import annotations, unicode_literals

import os
import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


def test_exporter_files(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="ssl_exporter").get("version")

    install_dir = get_vars.get("ssl_exporter_install_path")
    defaults_dir = get_vars.get("ssl_exporter_defaults_directory")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/ssl_exporter")
    files.append("/etc/systemd/system/multi-user.target.wants/ssl_exporter.service")

    if install_dir:
        files.append(f"{install_dir}/ssl_exporter")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/ssl_exporter")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert not f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("ssl_exporter_system_user", "ssl_exporter")
    group = get_vars.get("ssl_exporter_system_group", "ssl_exporter")

    assert not host.group(group).exists
    assert not host.user(user).exists
    # assert group in host.user(user).groups
    # assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("ssl_exporter")
    assert not service.is_enabled
    assert not service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    ssl_exporter_service = get_vars.get("ssl_exporter_service", None)

    if not ssl_exporter_service:
        ssl_exporter_service = get_vars.get("ssl_exporter_defaults_service", None)

    print(ssl_exporter_service)

    if isinstance(ssl_exporter_service, dict):
        ssl_exporter_web = ssl_exporter_service.get("web", {})

        listen_address = ssl_exporter_web.get("listen_address")
    else:
        listen_address = "127.0.0.1:9219"

    service = host.socket(f"tcp://{listen_address}")
    assert not service.is_listening
