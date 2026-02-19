from __future__ import annotations, unicode_literals

import os
import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


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
