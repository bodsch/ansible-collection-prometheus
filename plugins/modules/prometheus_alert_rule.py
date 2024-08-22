#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (c) 2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import os
import hashlib
import json
import base64
import binascii

from pathlib import Path

from ansible.module_utils.basic import AnsibleModule


class PrometheusAlertRule(object):
    """
    """

    def __init__(self, module):
        """
        """
        self.module = module

        self.state = module.params.get("state")

        self.rules_directory = module.params.get("rules_directory")
        self.name = module.params.get("name")
        self.alert = module.params.get("alert")
        self.for_clause = module.params.get("for_clause")
        self.expression = module.params.get("expression")
        self.labels = module.params.get("labels")
        annotations = module.params.get("annotations")

        self.checksum_directory = f"{Path.home()}/.ansible/cache/prometheus_alert_rules"

        annotations_title = annotations.get('title', None)
        annotations_description = annotations.get('description', None)
        annotations_summary = annotations.get('summary', None)

        self.annotations = dict()

        if annotations_title and len(annotations_title) != 0:
            self.annotations['title'] = self.is_base64(annotations_title)

        if annotations_description and len(annotations_description) != 0:
            self.annotations['description'] = self.is_base64(annotations_description)

        if annotations_summary and len(annotations_summary) != 0:
            self.annotations['summary'] = self.is_base64(annotations_summary)

    def run(self):
        """
        """
        result = dict(
            changed=False,
            failed=True,
            msg="initial"
        )

        properties = dict(
            alert=self.alert,
            for_clause=self.for_clause,
            expression=self.expression,
            labels=self.labels,
            annotations=self.annotations
        )

        if not os.path.exists(self.rules_directory):
            return dict(
                failed=True,
                msg=f"rules directory {self.rules_directory} does not exist."
            )

        result_state = []

        self.__create_directory(self.checksum_directory)

        if self.state == "present":
            changed = self._write_rule(self.name, properties)

            if changed:
                res = {}
                state = f"rule {self.name} successful written."

                res[self.name] = dict(
                    # changed=True,
                    state=state
                )

                result_state.append(res)

        if self.state == "absent":
            changed = self._delete_rule(self.name)

            if changed:
                res = {}
                state = f"rule {self.name} successful removed."

                res[self.name] = dict(
                    # changed=True,
                    state=state
                )

                result_state.append(res)

        # define changed for the running tasks
        # migrate a list of dict into dict
        combined_d = {key: value for d in result_state for key, value in d.items()}
        # find all changed and define our variable
        # changed = (len({k: v for k, v in combined_d.items() if v.get('changed') and v.get('changed') == True}) > 0) == True
        changed = (len({k: v for k, v in combined_d.items() if v.get('state')}) > 0)

        result = dict(
            changed=changed,
            failed=False,
            state=result_state
        )

        return result

    def _write_rule(self, name, properties={}):
        """
        """
        if len(properties) == 0:
            return False

        data_file = os.path.join(self.rules_directory, f"{name}.rules")
        checksum_file = os.path.join(self.checksum_directory, f"{name}.rules.checksum")

        return self.__write_file(properties, data_file, checksum_file)

    def _delete_rule(self, name):
        """
        """
        data_file = os.path.join(self.rules_directory, name, f"{name}.rules")
        checksum_file = os.path.join(self.checksum_directory, name, f"{name}.rules.checksum")

        if os.path.exists(data_file):
            os.remove(data_file)
            if os.path.exists(checksum_file):
                os.remove(checksum_file)

            return True

        return False

    def __write_file(self, data, data_file, checksum_file):
        """
        """
        _old_checksum = ""

        if os.path.exists(checksum_file):
            with open(checksum_file, "r") as f:
                _old_checksum = f.readlines()[0]

        data = self.__template(data)
        checksum = self.__checksum(data)

        data_up2date = (_old_checksum == checksum)

        # self.module.log(msg=f" - new  checksum '{checksum}'")
        # self.module.log(msg=f" - curr checksum '{_old_checksum}'")
        # self.module.log(msg=f" - up2date       '{data_up2date}'")

        if data_up2date:
            return False

        with open(data_file, "w") as f:
            f.write(data)

            with open(checksum_file, "w") as f:
                f.write(checksum)

        return True

    def __checksum(self, plaintext):
        """
        """
        if isinstance(plaintext, dict):
            password_bytes = json.dumps(plaintext, sort_keys=True).encode('utf-8')
        else:
            password_bytes = plaintext.encode('utf-8')

        password_hash = hashlib.sha256(password_bytes)
        return password_hash.hexdigest()

    def __template(self, data):
        """
          generate data from dictionary
        """
        tpl = """---
# generated by ansible

groups:
- name: ansible alert rule
  rules:
    - alert: {{ item.alert }}
{%- if item.for_clause is defined and item.for_clause | string | length > 0 %}
      for: {{ item.for_clause }}
{%- endif %}
{%- if item.expression is defined and item.expression | string | length > 0 %}
      expr: {{ item.expression }}
{%- endif %}
{%- if item.labels is defined and item.labels | count > 0 %}
      labels:
{%- for k, v in item.labels.items() %}
        {{ k }}: {{ v }}
{%- endfor %}
{%- endif %}
{%- if item.annotations is defined and item.annotations | count > 0 %}
      annotations:
{%- if item.annotations.title is defined %}
        title: |
          {{ item.annotations.title | indent(10) }}
{%- endif %}
{%- if item.annotations.description is defined %}
        description: |
          {{ item.annotations.description | indent(10) }}
{%- endif %}
{%- if item.annotations.summary is defined %}
        summary: |
          {{ item.annotations.summary | indent(10) | indent(10) }}
{%- endif %}
{%- endif %}

"""

        from jinja2 import Template

        tm = Template(tpl)
        d = tm.render(item=data)

        return d

    def __create_directory(self, dir):
        """
        """
        try:
            os.makedirs(dir, exist_ok=True)
        except FileExistsError:
            pass

        if os.path.isdir(dir):
            return True
        else:
            return False

    def is_base64(self, sb):
        """
        """
        try:
            data = base64.b64decode(sb, validate=True).decode('utf-8')
        except binascii.Error:
            data = sb

        return data


# ===========================================
# Module execution.


def main():
    """
    """
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(
                default="present", choices=["absent", "present"]
            ),
            name=dict(
                required=True,
                type='str'
            ),
            # rules=dict(
            #     required=False,
            #     type='list'
            # ),
            alert=dict(
                required=True,
                type="str"
            ),
            for_clause=dict(
                required=True,
                type="str"
            ),
            expression=dict(
                required=True,
                type="str"
            ),
            labels=dict(
                required=False,
                type="dict"
            ),
            annotations=dict(
                required=False,
                type="dict"
            ),
            rules_directory=dict(
                required=False,
                type='path',
                default="/etc/prometheus/rules"
            ),
        ),
        supports_check_mode=True,
    )

    p = PrometheusAlertRule(module)
    result = p.run()

    module.log(msg=f"= result: {result}")
    module.exit_json(**result)


if __name__ == '__main__':
    main()
