# coding: utf-8
from __future__ import unicode_literals

from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar

import json
import pytest
import os

import testinfra.utils.ansible_runner

HOST = 'instance'

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts(HOST)


def pp_json(json_thing, sort=True, indents=2):
    if type(json_thing) is str:
        print(json.dumps(json.loads(json_thing), sort_keys=sort, indent=indents))
    else:
        print(json.dumps(json_thing, sort_keys=sort, indent=indents))
    return None


def base_directory():
    """
    """
    cwd = os.getcwd()

    if 'group_vars' in os.listdir(cwd):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = f"molecule/{os.environ.get('MOLECULE_SCENARIO_NAME')}"

    return directory, molecule_directory


def read_ansible_yaml(file_name, role_name):
    """
    """
    read_file = None

    for e in ["yml", "yaml"]:
        test_file = f"{file_name}.{e}"
        if os.path.isfile(test_file):
            read_file = test_file
            break

    return f"file={read_file} name={role_name}"


@pytest.fixture()
def get_vars(host):
    """
        parse ansible variables
        - defaults/main.yml
        - vars/main.yml
        - vars/${DISTRIBUTION}.yaml
        - molecule/${MOLECULE_SCENARIO_NAME}/group_vars/all/vars.yml
    """
    base_dir, molecule_dir = base_directory()
    distribution = host.system_info.distribution
    operation_system = None

    if distribution in ['debian', 'ubuntu']:
        operation_system = "debian"
    elif distribution in ['redhat', 'ol', 'centos', 'rocky', 'almalinux']:
        operation_system = "redhat"
    elif distribution in ['arch', 'artix']:
        operation_system = f"{distribution}linux"

    # print(" -> {} / {}".format(distribution, os))
    # print(" -> {}".format(base_dir))

    file_defaults = read_ansible_yaml(f"{base_dir}/defaults/main", "role_defaults")
    file_vars = read_ansible_yaml(f"{base_dir}/vars/main", "role_vars")
    file_distibution = read_ansible_yaml(f"{base_dir}/vars/{operation_system}", "role_distibution")
    file_molecule = read_ansible_yaml(f"{molecule_dir}/group_vars/all/vars", "test_vars")
    # file_host_molecule = read_ansible_yaml("{}/host_vars/{}/vars".format(base_dir, HOST), "host_vars")

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    distibution_vars = host.ansible("include_vars", file_distibution).get("ansible_facts").get("role_distibution")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")
    # host_vars          = host.ansible("include_vars", file_host_molecule).get("ansible_facts").get("host_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(distibution_vars)
    ansible_vars.update(molecule_vars)
    # ansible_vars.update(host_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


def local_facts(host):
    """
      return local facts
    """
    local_fact = host.ansible("setup").get("ansible_facts").get("ansible_local")

    print(f"local_fact     : {local_fact}")

    if local_fact:
        return local_fact.get("bind_exporter", {})
    else:
        return dict()


@pytest.mark.parametrize("files", [
    "/usr/bin/bind_exporter",
    "/lib/systemd/system/bind_exporter.service"
])
def test_files(host, files):
    f = host.file(files)
    assert not f.exists


def test_version(host, get_vars):
    """
    """
    distribution = host.system_info.distribution
    release = host.system_info.release

    print(f"distribution: {distribution}")
    print(f"release     : {release}")

    version = local_facts(host).get("version")

    install_dir = get_vars.get("bind_exporter_install_path")
    defaults_dir = get_vars.get("bind_exporter_defaults_directory")

    if 'latest' in install_dir:
        install_dir = install_dir.replace('latest', version)

    files = []
    files.append("/usr/bin/bind_exporter")

    if install_dir:
        files.append(f"{install_dir}/bind_exporter")
    if defaults_dir and not distribution == "artix":
        files.append(f"{defaults_dir}/bind_exporter")

    print(files)

    for _file in files:
        f = host.file(_file)
        assert not f.is_file


def test_service(host, get_vars):
    service = host.service("bind_exporter")
    assert not service.is_enabled
    assert not service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    bind_exporter_service = get_vars.get("bind_exporter_service", {})

    print(bind_exporter_service)

    if isinstance(bind_exporter_service, dict):
        bind_exporter_web = bind_exporter_service.get("web", {})
        listen_address = bind_exporter_web.get("listen_address")

    if not listen_address:
        listen_address = "0.0.0.0:9119"

    print(listen_address)

    service = host.socket(f"tcp://{listen_address}")
    assert not service.is_listening

@pytest.mark.parametrize("sockets", [
    "tcp://127.0.0.1:9119",
])
def test_socket(host, sockets):
    s = host.socket(sockets)
    assert not s.is_listening
