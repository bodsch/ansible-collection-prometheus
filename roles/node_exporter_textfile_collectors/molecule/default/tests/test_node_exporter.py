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


@pytest.mark.parametrize(
    "files",
    [
        "/usr/bin/node_exporter",
    ],
)
def test_files(host, files):
    """ """
    d = host.file(files)
    assert d.is_file


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
