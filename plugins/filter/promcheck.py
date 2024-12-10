# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, print_function)
import re
import operator as op
from packaging.version import Version

__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):

    def filters(self):
        return {
            'promcheck_fix_release': self.fix_release,
        }

    def fix_release(self, data, promcheck_version, version=None):
        """
        """
        display.v(f"fix_release(self, {data}, {promcheck_version}, {version})")

        if version:
            if self.version_compare(promcheck_version, ">", version):
                archiv_name = data.get("file")
                extracted_name = data.get("extracted")
                display.v(f"  - file: {archiv_name} - {extracted_name}")
                # 1.1.8: promcheck_linux_amd64.tar.gz - promcheck_linux_amd64
                # 1.2.0: promcheck_linux-amd64 - promcheck_linux-amd64
                data["file"] = re.sub(r'_linux_amd64.tar.gz', '_linux-amd64', archiv_name)
                data["extracted"] = re.sub(r'_linux_amd64', '_linux-amd64', extracted_name)

        return data

    def version_compare(self, ver1, specifier, ver2):
        """
        """
        lookup = {'<': op.lt, '<=': op.le, '==': op.eq, '>=': op.ge, '>': op.gt}

        try:
            return lookup[specifier](Version(ver1), Version(ver2))
        except KeyError:
            # unknown specifier
            return False
