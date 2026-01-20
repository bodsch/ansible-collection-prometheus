# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, print_function

__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """ """

    def filters(self):
        return {
            "nginx_exporter_prometheus_labels": self.prometheus_labels,
        }

    def prometheus_labels(self, data):
        """
        -prometheus.const-labels value
              A comma separated list of constant labels that will be used in every metric.
              Format is label1=value1,label2=value2...
              The default value can be overwritten by CONST_LABELS environment variable.
        """
        display.v(f"prometheus_labels({data})")

        result = []

        for k, v in data.items():
            result.append(f"{k}={v}")

        result = ",".join(result)
        display.v(f"= result: {result}")

        return result
