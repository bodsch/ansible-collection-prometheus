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

    version = local_facts(host=host, fact="nginx_exporter").get("version")

    install_dir = get_vars.get("nginx_exporter_install_path")
    defaults_dir = get_vars.get("nginx_exporter_defaults_directory")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/nginx_exporter")
    files.append("/etc/systemd/system/multi-user.target.wants/nginx_exporter.service")

    if install_dir:
        files.append(f"{install_dir}/nginx_exporter")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/nginx_exporter")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("nginx_exporter_system_user", "nginx_exporter")
    group = get_vars.get("nginx_exporter_system_group", "nginx_exporter")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("nginx_exporter")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    nginx_exporter_service = get_vars.get("nginx_exporter_service", None)

    if not nginx_exporter_service:
        nginx_exporter_service = get_vars.get("nginx_exporter_defaults_service", None)

    print(nginx_exporter_service)

    if isinstance(nginx_exporter_service, dict):
        nginx_exporter_web = nginx_exporter_service.get("web", {})

        listen_address = nginx_exporter_web.get("listen_address")
    else:
        listen_address = "127.0.0.1:9213"

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
