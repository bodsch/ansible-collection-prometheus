# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, print_function

import os

__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):

    def filters(self):
        return {
            "node_exporter_custom_dirs": self.custom_dirs,
            "unique_dirs": self.unique_dirs,
            "cron_jobs": self.cron_jobs,
        }

    def custom_dirs(self, data, custom_directory="textfile"):
        """ """
        # display.v(f"custom_dirs(self, {data})")
        directories = []
        _enabled = data.get("enabled", None)

        display.v(f"_enabled: {_enabled}")

        if isinstance(_enabled, list) and _enabled:
            directories = [
                v.get("directory")
                for e in _enabled
                if type(e).__name__ == "dict"
                for k, v in e.items()
                if k == custom_directory and v.get("directory", None)
            ]

        return directories

    def unique_dirs(self, data):
        """ """
        # display.v(f"unique_dirs(self, {data})")
        directories = [os.path.dirname(x) for x in data]

        if len(directories) > 0:
            # unique enries
            directories = list(set(directories))

        return directories

    def cron_jobs(self, data, enabled=True):
        """ """
        # display.v(f"cron_jobs(self, {data}, {enabled})")
        if isinstance(data, list):
            if enabled:
                result = [x for x in data if x.get("cron", {}).get("enabled", True)]
            else:
                result = [x for x in data if not x.get("cron", {}).get("enabled", True)]

        # display.v(f"  = {result}")
        return result
