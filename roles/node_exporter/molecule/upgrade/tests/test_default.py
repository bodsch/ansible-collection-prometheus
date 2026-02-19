from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize(
    "dirs",
    [
        "/etc/node_exporter",
    ],
)
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory


def test_files(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="node_exporter").get("version")

    install_dir = get_vars.get("node_exporter_install_path")
    defaults_dir = get_vars.get("node_exporter_defaults_directory")
    # config_dir = get_vars.get("node_exporter_config_dir")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/node_exporter")

    if install_dir:
        files.append(f"{install_dir}/node_exporter")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/node_exporter")
    # if config_dir:
    #     files.append(f"{config_dir}/config.yml")

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("node_exporter_system_user", "node_exp")
    group = get_vars.get("node_exporter_system_group", "node_exp")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("node_exporter")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    node_exporter_service = get_vars.get("node_exporter_service", {})

    print(node_exporter_service)

    if isinstance(node_exporter_service, dict):
        node_exporter__web = node_exporter_service.get("web", {})
        listen_address = node_exporter__web.get("listen_address")

    if not listen_address:
        listen_address = "0.0.0.0:9100"

    print(listen_address)

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
