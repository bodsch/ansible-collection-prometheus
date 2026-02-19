
from __future__ import annotations, unicode_literals

import os
import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize(
    "files",
    [
        "/usr/bin/json_exporter",
        "/etc/json_exporter/config.yml",
        "/lib/systemd/system/json_exporter.service",
    ],
)
def test_files(host, files):
    f = host.file(files)
    assert f.exists


def test_version(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="json_exporter").get("version")

    install_dir = get_vars.get("json_exporter_install_path")
    defaults_dir = get_vars.get("json_exporter_defaults_directory")
    config_dir = get_vars.get("json_exporter_config_dir")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/json_exporter")

    if install_dir:
        files.append(f"{install_dir}/json_exporter")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/json_exporter")
    if config_dir:
        files.append(f"{config_dir}/config.yml")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("json_exporter_system_user", "json_exporter")
    group = get_vars.get("json_exporter_system_group", "json_exporter")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("json_exporter")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    json_exporter_service = get_vars.get("json_exporter_service", {})

    print(json_exporter_service)

    if isinstance(json_exporter_service, dict):
        json_exporter_web = json_exporter_service.get("web", {})
        listen_address = json_exporter_web.get("listen_address")

    if not listen_address:
        listen_address = "0.0.0.0:7979"

    print(listen_address)

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
