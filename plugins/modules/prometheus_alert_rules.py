#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (c) 2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function

import base64
import binascii

# import sys
import hashlib
import json
import os
from json.decoder import JSONDecodeError
from pathlib import Path

from ansible.module_utils.basic import AnsibleModule


class PrometheusAlertRules(object):
    """ """

    def __init__(self, module):
        """ """
        self.module = module

        self.state = module.params.get("state")

        # self.module.log(msg=f" - '{sys.version_info}")

        self.rules_directory = module.params.get("rules_directory")
        rules = module.params.get("rules")
        self.rules = self.is_base64(rules)

        self.checksum_directory = f"{Path.home()}/.ansible/cache/prometheus_alert_rules"

    def run(self):
        """ """
        result = dict(changed=False, failed=True, msg="initial")

        self.module.log(msg=f" - {self.rules}")

        try:
            self.rules = json.loads(self.rules)
        except ValueError as e:  # includes simplejson.decoder.JSONDecodeError
            self.module.log(msg=f"ValueError - '{e}'")

            return dict(changed=False, failed=True, msg=f"can't decode json: '{e}'")

        except JSONDecodeError as e:
            self.module.log(msg=f"JSONDecodeError - '{e}'")

            return dict(changed=False, failed=True, msg=f"can't decode json: '{e}'")
        except TypeError as e:
            self.module.log(msg=f"TypeError - '{e}'")

            return dict(changed=False, failed=True, msg=f"can't decode json: '{e}'")

        if not os.path.exists(self.rules_directory):
            return dict(
                failed=True,
                msg=f"rules directory {self.rules_directory} does not exist.",
            )

        self.__create_directory(self.checksum_directory)

        result_state = []

        if isinstance(self.rules, list):
            """ """
            result_state = self._rules_as_list()

        if isinstance(self.rules, dict):
            """ """
            result_state = self._rules_as_dict()

        # define changed for the running tasks
        # migrate a list of dict into dict
        combined_d = {key: value for d in result_state for key, value in d.items()}

        # find all changed and define our variable
        changed = len({k: v for k, v in combined_d.items() if v.get("changed")}) > 0
        # find all failed and define our variable
        # failed = (len({k: v for k, v in combined_d.items() if v.get('failed')}) > 0)

        result_msg = {k: v.get("state") for k, v in combined_d.items()}

        result = dict(changed=changed, failed=False, state=result_msg)

        return result

    def _rules_as_list(self):
        """ """
        self.module.log(msg="_rules_as_list()")

        result_state = []

        for rule in self.rules:
            """ """
            properties = []
            rules = rule.get("rules", {})
            file_name = rule.get("name", None)

            # self.module.log(msg=f" - {file_name}")
            # self.module.log(msg=f" - {len(rules)}")

            if len(rules) == 0:
                res = {}
                changed = self._delete_rule(file_name)

                if changed:
                    res[file_name] = dict(
                        changed=True, state="rule successful removed."
                    )

                result_state.append(res)

                return result_state

            for rule_name, values in rules.items():
                """ """
                # self.module.log(msg=f" - rule: {rule_name}")
                # state = values.get("state", "present")

                properties.append(self.decode_values(values))

            if properties:
                """ """
                # self.module.log(msg=f" - write rule {file_name}")

                res = {}

                changed = self._write_rule(file_name, properties)

                if changed:
                    res[file_name] = dict(
                        changed=True, state="rule successful written."
                    )
                else:
                    res[file_name] = dict(
                        changed=False, state="rule has not been changed."
                    )

                # if state == "absent":
                #     # changed = self._delete_rule(name)
                #
                #     if changed:
                #         res[rule_name] = dict(
                #             changed=True,
                #             state="rule successful removed."
                #         )

                result_state.append(res)

        return result_state

    def _rules_as_dict(self):
        """ """
        self.module.log(msg="_rules_as_dict()")

        result_state = []

        properties = []

        for name, values in self.rules.items():
            """ """
            state = values.get("state", "present")

            properties.append(self.decode_values(values))

            if properties:
                """ """
                res = {}

                if state == "present":
                    changed = self._write_rule(name, properties)

                    if changed:
                        res[name] = dict(changed=True, state="rule successful written.")
                    else:
                        res[name] = dict(
                            changed=False, state="rule has not been changed."
                        )

                if state == "absent":
                    changed = self._delete_rule(name)

                    if changed:
                        res[name] = dict(changed=True, state="rule successful removed.")

                result_state.append(res)

        return result_state

    def decode_values(self, values):
        """ """
        self.module.log(msg="decode_values(values)")

        if isinstance(values, dict):
            alert = values.get("alert")
            for_clause = values.get("for")
            expression = values.get("expr")
            labels = values.get("labels")
            annotations = values.get("annotations")

            self.module.log(msg=f"  annotations: {annotations}")

            if expression:
                expression = self.is_base64(expression)

            # annotations_title = annotations.get('title', None)
            # annotations_description = annotations.get('description', None)
            # annotations_summary = annotations.get('summary', None)
            #
            # annotations = dict()
            #
            # if annotations_title and len(annotations_title) != 0:
            #     annotations['title'] = self.is_base64(annotations_title)
            #
            # if annotations_description and len(annotations_description) != 0:
            #     annotations['description'] = self.is_base64(annotations_description)
            #
            # if annotations_summary and len(annotations_summary) != 0:
            #     annotations['summary'] = self.is_base64(annotations_summary)

            properties = dict(
                alert=alert,
                for_clause=for_clause,
                expression=expression,
                annotations=annotations,
            )

            if labels:
                properties["labels"] = labels
        else:
            properties = dict()

        return properties

    def _write_rule(self, name, properties={}):
        """ """
        if len(properties) == 0:
            return False

        data_file = os.path.join(self.rules_directory, f"{name}.rules")
        checksum_file = os.path.join(self.checksum_directory, f"{name}.rules.checksum")

        return self.__write_file(name, properties, data_file, checksum_file)

    def _delete_rule(self, name):
        """ """
        data_file = os.path.join(self.rules_directory, f"{name}.rules")
        checksum_file = os.path.join(self.checksum_directory, f"{name}.rules.checksum")

        if os.path.exists(data_file):
            os.remove(data_file)
            if os.path.exists(checksum_file):
                os.remove(checksum_file)

            return True

        return False

    def __write_file(self, name, data, data_file, checksum_file):
        """ """
        _old_checksum = ""

        if not os.path.exists(data_file) and os.path.exists(checksum_file):
            """ """
            os.remove(checksum_file)

        if os.path.exists(checksum_file):
            with open(checksum_file, "r") as f:
                _old_checksum = f.readlines()[0]

        data = self.__template(name, data)
        checksum = self.__checksum(data)

        data_up2date = _old_checksum == checksum

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
        """ """
        if isinstance(plaintext, dict):
            password_bytes = json.dumps(plaintext, sort_keys=True).encode("utf-8")
        else:
            password_bytes = plaintext.encode("utf-8")

        password_hash = hashlib.sha256(password_bytes)
        return password_hash.hexdigest()

    def __template(self, name, data):
        """
        generate data from dictionary
        """
        tpl = """---
# generated by ansible

groups:
{%- if item is defined and item | count > 0 %}
  - name: "Alert rules for {{ name }}"
    rules:
{%- for i in item %}
    - alert: {{ i.alert }}
{%- if i.for_clause is defined and i.for_clause | string | length > 0 %}
      for: {{ i.for_clause }}
{%- endif %}
{%- if i.expression is defined and i.expression | string | length > 0 %}
      expr: |
        {{ i.expression | indent(8) }}
{%- endif %}
{%- if i.labels is defined and i.labels | count > 0 %}
      labels:
{%- for k, v in i.labels.items() %}
        {{ k }}: {{ v }}
{%- endfor %}
{%- endif %}
{%- if i.annotations is defined and i.annotations | count > 0 %}
      annotations:
{%- for k, v in i.annotations.items() %}
        {{ k }}: |
          {{ v | indent(10) }}
{%- endfor %}
{% endif -%}
{% endfor %}
{% endif %}
"""

        from jinja2 import Template

        tm = Template(tpl)
        d = tm.render(name=name, item=data)

        return d

    def __create_directory(self, dir):
        """ """
        try:
            os.makedirs(dir, exist_ok=True)
        except FileExistsError:
            pass

        if os.path.isdir(dir):
            return True
        else:
            return False

    def is_base64(self, sb):
        """ """
        try:
            data = base64.b64decode(sb, validate=True).decode("utf-8")
        except binascii.Error:
            data = sb

        return data


# ===========================================
# Module execution.


def main():
    """ """
    module = AnsibleModule(
        argument_spec=dict(
            rules=dict(required=True),
            rules_directory=dict(
                required=False, type="path", default="/etc/prometheus/rules"
            ),
            group=dict(required=False, type="str"),
            mode=dict(required=False, type="str"),
        ),
        supports_check_mode=True,
    )

    p = PrometheusAlertRules(module)
    result = p.run()

    module.log(msg=f"= result: {result}")
    module.exit_json(**result)


if __name__ == "__main__":
    main()
