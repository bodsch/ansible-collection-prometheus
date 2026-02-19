from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize("dirs", ["/etc/alertmanager", "/etc/amtool"])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory


def test_alertmanager_files(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="alertmanager").get("version")

    install_dir = get_vars.get("alertmanager_install_path")
    defaults_dir = get_vars.get("alertmanager_defaults_directory")
    config_dir = get_vars.get("alertmanager_config_dir")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/alertmanager")

    if install_dir:
        files.append(f"{install_dir}/alertmanager")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/alertmanager")
    if config_dir:
        files.append(f"{config_dir}/alertmanager.yml")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_amtool_files(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="alertmanager").get("version")
    install_dir = get_vars.get("alertmanager_install_path")
    config_dir = get_vars.get("alertmanager_amtool", {}).get("config_dir", None)

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/amtool")

    if install_dir:
        files.append(f"{install_dir}/amtool")
    if config_dir:
        files.append(f"{config_dir}/config.yml")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("alertmanager_system_user", "alertmanager")
    group = get_vars.get("alertmanager_system_group", "alertmanager")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("alertmanager")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    alertmanager_service = get_vars.get("alertmanager_service", {})

    print(alertmanager_service)

    if isinstance(alertmanager_service, dict):
        alertmanager_web = alertmanager_service.get("web", {})

        listen_address = alertmanager_web.get("listen_address")
    else:
        listen_address = "0.0.0.0:9093"

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
