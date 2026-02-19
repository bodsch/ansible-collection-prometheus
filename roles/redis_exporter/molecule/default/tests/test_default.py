from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize(
    "files", ["/usr/bin/redis_exporter", "/lib/systemd/system/redis_exporter.service"]
)
def test_files(host, files):
    f = host.file(files)
    assert f.exists


@pytest.mark.parametrize(
    "sockets",
    [
        "tcp://127.0.0.1:9121",
    ],
)
def test_socket(host, sockets):
    s = host.socket(sockets)
    assert s.is_listening
