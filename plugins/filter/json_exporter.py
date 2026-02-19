# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, print_function

__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """ """

    def filters(self):
        return {
            "convert_to_modules": self.convert_to_modules,
        }

    def convert_to_modules(self, data, modules={}):
        """ """
        result = None
        # display.v(f"convert_to_modules({data}, {modules})")

        if isinstance(modules, dict):

            keys = modules.keys()

            if "default" in keys:
                """
                default already exists
                """
                # display.v("use 'defaut' entry")

                for metric_b in data:
                    found = False
                    for metric_a in modules["default"]["metrics"]:
                        if metric_a.get("name") == metric_b.get("name"):
                            metric_a.update(metric_b)
                            found = True
                            break

                    if not found:
                        modules["default"]["metrics"].append(metric_b)

            else:
                """
                create 'defaut' entry
                """
                # display.v("create 'defaut' entry")

                modules["default"] = dict()
                modules["default"]["metrics"] = []
                modules["default"]["metrics"] = data

        result = modules

        # display.v(f"= result: {result}")

        return result
