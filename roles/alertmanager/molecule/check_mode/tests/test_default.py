from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


@pytest.mark.parametrize("dirs", ["/etc/alertmanager", "/etc/amtool"])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert not d.is_directory


def test_alertmanager_files(host, get_vars):
    """ """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host=host, fact="alertmanager").get("version")

    install_dir = get_vars.get("alertmanager_install_path")
    defaults_dir = get_vars.get("alertmanager_defaults_directory")
    config_dir = get_vars.get("alertmanager_config_dir")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/alertmanager")

    if install_dir:
        files.append(f"{install_dir}/alertmanager")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/alertmanager")
    if config_dir:
        files.append(f"{config_dir}/alertmanager.yml")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert not f.is_file
