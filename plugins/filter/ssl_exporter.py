# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, print_function

__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):

    def filters(self):
        return {
            "ssl_exporter_modules": self.ssl_exporter_modules,
        }

    def ssl_exporter_modules(self, data, valid_probers):
        """ """
        return [k for k, v in data.items() if v.get("prober") in valid_probers]
