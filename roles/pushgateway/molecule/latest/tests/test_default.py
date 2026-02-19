from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


def test_version(host, get_vars):
    """ """
    version = local_facts(host=host, fact="pushgateway").get("version")

    version_dir = f"/usr/local/opt/pushgateway/{version}"
    current_link = "/usr/bin/pushgateway"

    print(version_dir)

    directory = host.file(version_dir)
    assert directory.is_directory

    link = host.file(current_link)
    assert link.is_symlink
    assert link.linked_to == f"{version_dir}/pushgateway"


@pytest.mark.parametrize("files", ["/usr/bin/pushgateway"])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("pushgateway_system_user", "pushgateway")
    group = get_vars.get("pushgateway_system_group", "pushgateway")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("pushgateway")
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    listen_default = "127.0.0.1:9091"

    pushgateway_service = get_vars.get("pushgateway_service", {})

    print(f"- pushgateway_service: {pushgateway_service}")

    if isinstance(pushgateway_service, dict):
        pushgateway_web = pushgateway_service.get("web", {})
        listen_address = pushgateway_web.get("listen_address", listen_default)
    else:
        listen_address = listen_default

    print(f"- listen_address: {listen_address}")

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
