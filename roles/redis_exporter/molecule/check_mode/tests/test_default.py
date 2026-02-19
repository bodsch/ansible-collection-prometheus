from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize(
    "directories", ["/etc/redis_exporter", "/usr/local/opt/redis_exporter"]
)
def test_directories(host, directories):
    d = host.file(directories)
    assert not d.is_directory


@pytest.mark.parametrize(
    "files", ["/usr/bin/redis_exporter", "/lib/systemd/system/redis_exporter.service"]
)
def test_files(host, files):
    f = host.file(files)
    assert not f.exists


def test_service(host, get_vars):
    service = host.service("redis_exporter")
    assert not service.is_enabled
    assert not service.is_running


@pytest.mark.parametrize(
    "sockets",
    [
        "tcp://127.0.0.1:9121",
    ],
)
def test_socket(host, sockets):
    s = host.socket(sockets)
    assert not s.is_listening
