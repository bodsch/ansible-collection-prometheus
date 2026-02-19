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
        "/usr/bin/redis_exporter",
        "/etc/default/redis_exporter",
        "/lib/systemd/system/redis_exporter.service",
    ],
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

    version = local_facts(host=host, fact="redis_exporter").get("version")

    install_dir = get_vars.get("redis_exporter_install_path")
    defaults_dir = get_vars.get("redis_exporter_defaults_directory")
    config_dir = get_vars.get("redis_exporter_config_dir")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/redis_exporter")

    if install_dir:
        files.append(f"{install_dir}/redis_exporter")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/redis_exporter")
    # if config_dir:
    #    files.append(f"{config_dir}/config.yml")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("redis_exporter_system_user", "redis_exporter")
    group = get_vars.get("redis_exporter_system_group", "redis_exporter")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("redis_exporter")
    assert service.is_enabled
    assert service.is_running


@pytest.mark.parametrize(
    "sockets",
    [
        "tcp://127.0.0.1:9121",
    ],
)
def test_socket(host, sockets):
    s = host.socket(sockets)
    assert s.is_listening
