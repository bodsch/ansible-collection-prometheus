# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, print_function

__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """ """

    def filters(self):
        return {
            "valid_credentials": self.valid_credentials,
            "has_credentials": self.has_credentials,
        }

    def valid_credentials(self, data):
        """
        input: dict ''
        output: dict or None
        """
        result = None
        display.v(f"valid_credentials({data})")

        if isinstance(data, dict):
            _hostname = data.get("hostname", None)
            _port = data.get("port", None)
            _socket = data.get("socket", None)
            # _username = data.get("username", None)
            # _password = data.get("password", None)

            if _hostname and not _port:
                data["port"] = 3306

            if _hostname and _port and _socket:
                _ = data.pop("socket")

            if not _hostname and not _socket:
                data = None

        result = data

        display.v(f"= result: {result}")

        return result

    def has_credentials(self, data):
        """ """
        result = {}

        if isinstance(data, dict):
            display.v(f"valid_credentials({data})")

            for k, v in data.items():
                is_valid = self.valid_credentials(v)

                if is_valid:
                    result[k] = {}
                    result[k] = is_valid

        display.v(f"= result: {result}")

        return result
