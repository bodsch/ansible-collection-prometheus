from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize(
    "files", [
        "/usr/bin/openvpn_exporter",
        "/lib/systemd/system/openvpn_exporter.service"
    ]
)
def test_files(host, files):
    f = host.file(files)
    assert f.exists

def test_user(host, get_vars):
    """ """
    system_user = get_vars.get("openvpn_exporter_system_user", {})

    owner = system_user.get("owner", "openvpn-exporter")
    group = system_user.get("group", "openvpn-exporter")

    assert host.group(group).exists
    assert host.user(owner).exists
    assert group in host.user(owner).groups
    assert host.user(owner).home == "/nonexistent"
