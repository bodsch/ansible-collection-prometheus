#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (c) 2022-2023, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import absolute_import, division, print_function

import os

from ansible.module_utils.basic import AnsibleModule


class AlertmanagerTemplates:
    """
    Main Class
    """

    module = None

    def __init__(self, module):
        """
        Initialize all needed Variables
        """
        self.module = module

        self.state = module.params.get("state")
        self.verbose = module.params.get("verbose")
        self.templates_directory = module.params.get("templates_directory")
        templates = module.params.get("templates")
        self.templates = []

        if isinstance(templates, str):
            templates = templates.split(",")

        if isinstance(templates, list):
            for x in templates:
                self.templates.append(os.path.basename(x))

    def run(self):
        """
        runner
        """
        result = dict(
            failed=False,
        )

        exists_template_files = [
            f
            for f in os.listdir(self.templates_directory)
            if os.path.isfile(os.path.join(self.templates_directory, f))
            and f.endswith(".tmpl")
        ]

        _exists = set(self.templates)

        templates_diff = [x for x in exists_template_files if x not in _exists]

        if len(templates_diff) > 0:
            self.remove_templates(templates_diff)

            result.update({"changed": True, "removed_templates": templates_diff})

        return result

    def remove_templates(self, templates):
        """ """
        os.chdir(self.templates_directory)

        for t in templates:
            if os.path.isfile(t):
                os.remove(t)


# ===========================================
# Module execution.
#


def main():

    argument_spec = dict(
        state=dict(default="check", choices=["check", "remove"]),
        verbose=dict(type=bool, default=True),
        templates_directory=dict(type=str, default="/etc/alertmanager/templates"),
        templates=dict(type=list, required=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    s = AlertmanagerTemplates(module)
    result = s.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == "__main__":
    main()
