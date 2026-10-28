from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize(
    "files", ["/usr/bin/openvpn_exporter", "/lib/systemd/system/openvpn_exporter.service"]
)
def test_files(host, files):
    f = host.file(files)
    assert f.exists


def test_version(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="openvpn_exporter").get("version")

    install_dir = get_vars.get("openvpn_exporter_install_path")
    defaults_dir = get_vars.get("openvpn_exporter_defaults_directory")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/openvpn_exporter")

    if install_dir:
        files.append(f"{install_dir}/openvpn_exporter")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/openvpn_exporter")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("openvpn_exporter_system_user", "openvpn_exporter")
    group = get_vars.get("openvpn_exporter_system_group", "openvpn_exporter")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("openvpn_exporter")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    openvpn_exporter_service = get_vars.get("openvpn_exporter_service", {})

    print(openvpn_exporter_service)

    if isinstance(openvpn_exporter_service, dict):
        openvpn_exporter_web = openvpn_exporter_service.get("web", {})
        listen_address = openvpn_exporter_web.get("listen_address")

    if not listen_address:
        listen_address = "0.0.0.0:9119"

    print(listen_address)

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
