# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, print_function

__metaclass__ = type

import base64
import json
import os
import re

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
    Ansible file jinja2 tests
    """

    def filters(self):
        return {
            "validate_file_sd": self.validate_file_sd,
            "validate_alertmanager_endpoints": self.validate_alertmanager_endpoints,
            "remove_empty_elements": self.remove_empty_elements,
            # 'raw_encode': self.raw_encode,
            "jinja_encode": self.jinja_encode,
        }

    def validate_file_sd(self, data, targets):
        """ """
        result = []
        sublist = []
        config_files = []

        for scrape in data:
            """ """
            file_sd = scrape.get("file_sd_configs", None)

            if isinstance(file_sd, list):
                file_sd = file_sd[0]
                files = file_sd.get("files", [])

                if len(files) > 0:
                    sublist.append(files)

        config_files = sum(sublist, [])

        display.v("  - files: {}".format(config_files))

        for f in config_files:
            name, extension = os.path.basename(f).split(".")

            display.v("    - name: {} / extenstion {}".format(name, extension))

            if name not in targets or extension not in ["yml", "yaml"]:
                result.append(os.path.basename(f))

        display.v("{}".format(result))

        return result

    def validate_alertmanager_endpoints(self, data):
        """ """
        # display.v(f"validate_alertmanager_endpoints({data})")

        supported = ["static_configs"]

        known_sd_configs = [
            "azure_sd_configs",
            "consul_sd_configs",
            "dns_sd_configs",
            "ec2_sd_configs",
            "eureka_sd_configs",
            "file_sd_configs",
            "digitalocean_sd_configs",
            "docker_sd_configs",
            "dockerswarm_sd_configs",
            "gce_sd_configs",
            "hetzner_sd_configs",
            "http_sd_configs",
            "kubernetes_sd_configs",
            "lightsail_sd_configs",
            "linode_sd_configs",
            "marathon_sd_configs",
            "nerve_sd_configs",
            "nerve_sd_configs",
            "openstack_sd_configs",
            "puppetdb_sd_configs",
            "scaleway_sd_configs",
            "serverset_sd_configs",
            "triton_sd_configs",
            "uyuni_sd_configs",
            "static_configs",
        ]

        sd_configs = []

        if isinstance(data, list):
            sd_configs = [
                x for x in data[0] if re.search(r".*sd_configs|static_configs$", x)
            ]

            # display.v(f"  - sd_configs: {sd_configs}")

            sd_are_known = len(set(sd_configs).intersection(known_sd_configs))

            if sd_are_known > 0:
                """
                well, we found a services discovery in the know array
                """
                # display.v(f"    known     {sd_configs}")
                if len(set(sd_configs).intersection(supported)) > 0:
                    """
                    and, the are supported!
                    """
                    # display.v(f"    supported {sd_configs}")

                    if len(sd_configs) == len(supported):
                        return [True, sd_configs, supported]
                    else:
                        return [False, sd_configs, supported]

        return [False, sd_configs, supported]

    def remove_empty_elements(self, data):
        """ """
        data_copy = data.copy()

        if isinstance(data_copy, dict):
            """ """
            result = {k: v for k, v in data_copy.items() if v}

            display.v("= result: {}".format(result))

            return result

    def jinja_encode(self, data):
        """ """
        # display.v(f"jinja_encode({data})")
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True).encode("utf-8")
        elif isinstance(data, list):
            data = json.dumps(data, sort_keys=True).encode("utf-8")
        else:
            data = data.encode("utf-8")

        result = base64.b64encode(data).decode("utf-8")
        # display.v(f"= result: {result}")

        return result
