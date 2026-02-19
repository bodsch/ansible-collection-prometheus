from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize(
    "dirs",
    [
        "/etc/prometheus",
    ],
)
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.exists


def test_files(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="prometheus").get("version")

    install_dir = get_vars.get("prometheus_install_path")
    defaults_dir = get_vars.get("prometheus_defaults_directory")
    config_dir = get_vars.get("prometheus_config_dir")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/prometheus")

    if install_dir:
        files.append(f"{install_dir}/prometheus")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/prometheus")
    if config_dir:
        files.append(f"{config_dir}/prometheus.yml")
        files.append(f"{config_dir}/rules/ops.rules")
        files.append(f"{config_dir}/rules/prometheus.rules")

        files.append(f"{config_dir}/file_sd/kresd.yml")
        files.append(f"{config_dir}/file_sd/node.yml")
        files.append(f"{config_dir}/file_sd/sensors.yml")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert f.exists
        assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("prometheus_system_user", "prometheus")
    group = get_vars.get("prometheus_system_group", "prometheus")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("prometheus")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    prometheus_service = get_vars.get("prometheus_service", {})

    print(prometheus_service)

    if isinstance(prometheus_service, dict):
        prometheus_web = prometheus_service.get("web", {})

        listen_address = prometheus_web.get("listen_address")
    else:
        listen_address = "0.0.0.0:9090"

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
