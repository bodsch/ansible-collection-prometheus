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
        "/usr/bin/sentinel",
        "/etc/sentinel/config.yml",
        "/lib/systemd/system/sentinel.service",
    ],
)
def test_files(host, files):
    f = host.file(files)
    assert f.exists


def test_user(host, get_vars):
    """ """
    system_user = get_vars.get("sentinel_system_user", {})

    owner = system_user.get("owner", "sentinel")
    group = system_user.get("group", "sentinel")

    assert host.group(group).exists
    assert host.user(owner).exists
    assert group in host.user(owner).groups
    assert host.user(owner).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("sentinel")
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize(
    "sockets",
    [
        "tcp://127.0.0.1:8080",
    ],
)
def test_socket(host, sockets):
    s = host.socket(sockets)
    assert s.is_listening
