# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, print_function

import os
from typing import Any

from ansible.utils.display import Display

display = Display()


class FilterModule(object):

    def filters(self):
        return {
            "node_exporter_custom_dirs": self.custom_dirs,
            "unique_dirs": self.unique_dirs,
            "cron_jobs": self.cron_jobs,
        }

    def custom_dirs(
        self, data: dict[str, Any], custom_directory: str = "textfile"
    ) -> list[str]:
        """
        Return directory paths for a specific collector from the ``enabled`` section.

        The function is intentionally defensive and tolerates mixed/invalid entries in
        the input structure (e.g. strings, incomplete dicts, missing keys).

        Expected input shape (simplified example):
            {
                "enabled": [
                    {"textfile": {"directory": "/var/lib/node_exporter"}},
                    {"filesystem": {"mount-points-exclude": "..."}},
                    "cpu",
                    "meminfo",
                ]
            }
        Args:
            data: Filter input dictionary that may contain an ``enabled`` list.
            custom_directory: Collector key to inspect (default: ``"textfile"``).

        Returns:
            A list of directory paths (strings). Invalid or missing values are ignored.
            Duplicates are removed while preserving order.
        """
        display.vv(
            f"bodsch.prometheus.custom_dirs(self, data: {data}, custom_directory: {custom_directory})"
        )
        directories: list[str] = []

        if not isinstance(data, dict):
            display.vvv("  - invalid input: 'data' is not a dict")
            return directories

        if not isinstance(custom_directory, str) or not custom_directory.strip():
            display.vvv(
                "  - invalid input: 'custom_directory' must be a non-empty string"
            )
            return directories

        enabled = data.get("enabled", [])
        if not isinstance(enabled, list):
            display.vvv("  - invalid input: 'enabled' is not a list")
            return directories

        dicts = {k: v for e in enabled if isinstance(e, dict) for k, v in e.items()}
        display.vv(f"  - dicts: {dicts}")

        directories.append(dicts.get(custom_directory).get("directory"))

        display.vv(f"= result: {directories}")
        return directories

    def unique_dirs(self, data):
        """ """
        display.vv(f"bodsch.prometheus.unique_dirs(self, data: {data})")

        directories = [os.path.dirname(x) for x in data]

        if len(directories) > 0:
            # unique enries
            directories = list(set(directories))

        return directories

    def cron_jobs(self, data, enabled=True):
        """ """
        display.vv(
            f"bodsch.prometheus.cron_jobs(self, data: {data}, enabled: {enabled})"
        )

        if isinstance(data, list):
            if enabled:
                result = [x for x in data if x.get("cron", {}).get("enabled", True)]
            else:
                result = [x for x in data if not x.get("cron", {}).get("enabled", True)]

        return result
