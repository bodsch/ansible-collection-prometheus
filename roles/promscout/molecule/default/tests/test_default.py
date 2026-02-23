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
        "/etc/promscout",
    ],
)
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


def test_files(host, get_vars):
    """ """
    install_dir = get_vars.get("promscout_install_path")
    defaults_dir = get_vars.get("promscout_defaults_directory")
    config_dir = get_vars.get("promscout_config_dir")

    files = []
    files.append("/usr/bin/promscout")

    if install_dir:
        files.append(f"{install_dir}/promscout")
    if defaults_dir:
        files.append(f"{defaults_dir}/promscout")
    if config_dir:
        files.append(f"{config_dir}/config.yml")

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("promscout_system_user", "promscout")
    group = get_vars.get("promscout_system_group", "promscout")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("promscout")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    promscout_listen = get_vars.get("promscout_listen")

    if isinstance(promscout_listen, dict):
        address = promscout_listen.get("address")
        port = promscout_listen.get("port")
    elif isinstance(promscout_listen, str):
        address = promscout_listen.split(":")[0]
        port = promscout_listen.split(":")[1]

    service = host.socket(f"tcp://{address}:{port}")
    assert service.is_listening
