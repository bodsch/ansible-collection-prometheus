#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (c) 2020-2023, Bodo Schulz <bodo@boone-schulz.de>
# Apache-2.0 (see LICENSE or https://opensource.org/license/apache-2-0)
# SPDX-License-Identifier: Apache-2.0

from __future__ import (absolute_import, print_function)
__metaclass__ = type

import re
from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'parse_checksum': self.parse_checksum,
        }

    def parse_checksum(self, data, application, os, arch, file_extension="tar.gz"):
        """
        """
        # display.v(f"parse_checksum(self, data, {application}, {os}, {arch})")

        checksum = None
        os = os.lower()

        if isinstance(data, list):
            # 206cf787c01921574ca171220bb9b48b043c3ad6e744017030fed586eb48e04b  alertmanager-0.25.0.linux-amd64.tar.gz
            # 2b8b693ce006406db200c7bd9987453b7055e4e98511fd7b36d492fc68bfc0f4  nginx-prometheus-exporter_0.11.0_linux_amd64.tar.gz
            # (?P<checksum>[a-zA-Z0-9]+).*alertmanager[-_].*linux-amd64\.tar\.gz$
            checksum = [
                x for x in data
                if re.search(fr"(?P<checksum>[a-zA-Z0-9]+).*{application}[-_].*{os}[-_]{arch}\.{file_extension}", x)
            ][0]

            display.v(f"  found checksum: {checksum}")

        if isinstance(checksum, str):
            checksum = checksum.split(" ")[0]

        display.v(f"= checksum: {checksum}")

        return checksum
