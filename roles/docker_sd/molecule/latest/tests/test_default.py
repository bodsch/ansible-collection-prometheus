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
        "/etc/docker-sd",
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

    version = local_facts(host=host, fact="docker_sd").get("version")

    install_dir = get_vars.get("docker_sd_install_path")
    defaults_dir = get_vars.get("docker_sd_defaults_directory")
    config_dir = get_vars.get("docker_sd_config_dir")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/docker-sd")

    if install_dir:
        files.append(f"{install_dir}/docker-sd")
    if defaults_dir:
        files.append(f"{defaults_dir}/docker-sd")
    if config_dir:
        files.append(f"{config_dir}/docker-sd.yml")

    for _file in files:
        f = host.file(_file)
        assert f.exists
        assert f.is_file


def test_user(host, get_vars):
    """ """
    user = get_vars.get("docker_sd_system_user", "node_exp")
    group = get_vars.get("docker_sd_system_group", "node_exp")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups
    assert host.user(user).home == "/nonexistent"


def test_service(host, get_vars):
    service = host.service("docker-sd")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    docker_sd_rest_api = get_vars.get("docker_sd_rest_api")

    address = docker_sd_rest_api.get("address")
    port = docker_sd_rest_api.get("port")

    service = host.socket(f"tcp://{address}:{port}")
    assert service.is_listening
