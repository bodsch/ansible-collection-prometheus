# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, print_function

__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """ """

    def filters(self):
        return {
            "docker_group": self.docker_group,
        }

    def docker_group(self, data, group: str = "docker"):
        """ """
        display.v(f"bodsch.prometheus.docker_group(data: {data}, group: {group})")

        if isinstance(data, dict):
            _getent = data.get("ansible_facts", {}).get("getent_group", {})
            display.v(f"  - {_getent}")
            if _getent:
                _docker = _getent.get(group, None)
                display.v(f"  - {_docker}")
                if _docker:
                    return True

        return False
