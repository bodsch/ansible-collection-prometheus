# python 3 headers, required if submitting to Ansible

# from __future__ import absolute_import, print_function

# import base64
# import json
# import os
# import re

from ansible.utils.display import Display

display = Display()


class FilterModule:
    """ """

    def filters(self):
        return {
            "verify_additional_groups": self.verify_additional_groups,
        }

    def verify_additional_groups(self, data, system_groups):
        """ """
        display.vv(
            f"bodsch.prometheus::verify_additional_groups(data: {data}, system_groups: {system_groups})"
        )

        result: list = []

        _system_groups = system_groups.get("ansible_facts", {}).get("getent_group", {})
        # display.v(f"    - name: {_system_groups}")

        _system_group_names = list(_system_groups.keys())
        result = list(set(_system_group_names) & set(data))

        display.vv(f"result = {result}")

        return result
