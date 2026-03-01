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
        "/usr/bin/logstream-exporter",
        "/etc/logstream_exporter/config.yml",
        "/lib/systemd/system/logstream_exporter.service",
    ],
)
def test_files(host, files):
    f = host.file(files)
    assert f.exists

def test_user(host, get_vars):
    """ """
    user = get_vars.get("logstream_exporter_system_user", "logstream_exporter")
    group = get_vars.get("logstream_exporter_system_group", "logstream_exporter")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("logstream_exporter")
    assert service.is_enabled
    assert service.is_running

@pytest.mark.parametrize(
    "sockets",
    [
        "udp://127.0.0.1:2212",
        "tcp://127.0.0.1:9212",
    ],
)
def test_socket(host, sockets):
    s = host.socket(sockets)
    assert s.is_listening
