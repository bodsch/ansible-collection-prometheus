from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize("directories", ["/usr/local/opt/mongodb_exporter"])
def test_directories(host, directories):
    d = host.file(directories)
    assert d.is_directory
    assert d.exists


def test_files(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="mongodb_exporter").get("version")

    install_dir = get_vars.get("mongodb_exporter_install_path")
    defaults_dir = get_vars.get("mongodb_exporter_defaults_directory")
    config_dir = get_vars.get("mongodb_exporter_config_dir")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/mongodb_exporter")

    if install_dir:
        files.append(f"{install_dir}/mongodb_exporter")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/mongodb_exporter")
    # if config_dir:
    #    files.append(f"{config_dir}/mongodb_exporter.cnf")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.exists
        assert f.is_file


def test_user(host, get_vars):
    username = get_vars.get("mongodb_exporter_system_user")
    groupname = get_vars.get("mongodb_exporter_system_group")

    assert host.group(groupname).exists
    assert host.user(username).exists
    assert groupname in host.user(username).groups
    assert host.user(username).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("mongodb_exporter")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    _service = get_vars.get("mongodb_exporter_service", {})

    print(_service)

    if isinstance(_service, dict):
        _web = _service.get("web", {})
        listen_address = _web.get("listen_address")

    if not listen_address:
        listen_address = "127.0.0.1:9216"

    print(listen_address)

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
