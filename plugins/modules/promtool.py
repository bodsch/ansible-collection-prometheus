#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (c) 2022-2023, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule


class Promtool(object):
    """
    Main Class
    """

    module = None

    def __init__(self, module):
        """
        Initialize all needed Variables
        """
        self.module = module

        self.promtool_bin = module.get_bin_path("promtool", False)
        self.state = module.params.get("state")
        self.config = module.params.get("config")

    def run(self):
        """
        runner
        """
        if self.module.check_mode:
            self.module.debug("In check mode.")

            return dict(failed=False, changed=False, msg="In check mode.")

        result = dict(
            failed=True,
        )

        args = [self.promtool_bin]

        if self.state == "check":
            args.append("check")
            args.append("config")

        args.append(self.config)

        # self.module.log(msg=f" - args {args}")

        rc, out, err = self._exec(args)

        result.update({"msg": out})

        if rc == 0:
            result.update({"failed": False})
        else:
            result.update({"error": err})

        return result

    def _exec(self, args):
        """ """
        rc, out, err = self.module.run_command(args, check_rc=False)
        self.module.log(msg=f"  rc : '{rc}'")

        if rc != 0:
            self.module.log(msg=f"  out: '{out}'")
            self.module.log(msg=f"  err: '{err}'")
        return rc, out, err


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default="check", choices=["check"]),
            config=dict(type=str),
        ),
        supports_check_mode=True,
    )

    s = Promtool(module)
    result = s.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == "__main__":
    main()
