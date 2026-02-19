
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

    version = local_facts(host=host, fact="node_exporter").get("version")

    install_dir = get_vars.get("node_exporter_install_path")

    if "latest" in install_dir:
        install_dir = install_dir.replace("latest", version)

    files = []
    files.append("/usr/bin/node_exporter")

    if install_dir:
        files.append(f"{install_dir}/collector-scripts/apt.sh")
        files.append(f"{install_dir}/collector-scripts/required-reboot.sh")

    for _file in files:
        f = host.file(_file)
        assert f.is_file
