
from __future__ import annotations, unicode_literals

import os
import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


def test_files(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="trickster").get("version")

    install_dir = get_vars.get("trickster_install_path")
    defaults_dir = get_vars.get("trickster_defaults_directory")
    config_dir = get_vars.get("trickster_config_dir")
    systemd_unit_dir = get_vars.get("systemd_lib_directory")
    service_manager = (
        host.ansible("setup").get("ansible_facts").get("ansible_service_mgr")
    )

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/trickster")

    if install_dir:
        files.append(f"{install_dir}/trickster")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/trickster")
    if config_dir:
        files.append(f"{config_dir}/config.yml")
    if systemd_unit_dir and service_manager == "systemd":
        files.append(f"{systemd_unit_dir}/trickster.service")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_user(host):
    assert host.group("trickster").exists
    assert "trickster" in host.user("trickster").groups
    assert host.user("trickster").shell == "/usr/sbin/nologin"
    assert host.user("trickster").home == "/nonexistent"


def test_service(host):
    s = host.service("trickster")
    assert s.is_enabled
    assert s.is_running


@pytest.mark.parametrize(
    "ports",
    [
        "127.0.0.1:8480",
        "127.0.0.1:8481",
        "127.0.0.1:8484",
    ],
)
def test_open_port(host, ports):

    for i in host.socket.get_listening_sockets():
        print(i)

    service = host.socket(f"tcp://{ports}")
    assert service.is_listening
