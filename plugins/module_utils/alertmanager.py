#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (c) 2022-2023, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import absolute_import, division, print_function

import requests


class Alertmanager:
    """ """

    module = None

    def __init__(self, module):
        """ """
        self.module = module

        self.state = module.params.get("state")
        self.verbose = module.params.get("verbose")
        self.url = module.params.get("url")

    def status(self):
        """ """
        path = "api/v2/status"

        code, status = self.__call_url(method="GET", path=path)

        return code, status

    def silences(self):
        """ """
        path = "api/v2/silences"

        code, status = self.__call_url(
            method="GET",
            path=path,
        )

        return code, status

    def silence(self, payload=None):
        """ """
        path = "api/v2/silences"

        if not payload:
            method = "GET"
        else:
            method = "POST"

        code, status = self.__call_url(
            method=method,
            path=path,
            data=payload,
        )

        return code, status

    def delete_silence(self, silence_id):
        """ """
        path = f"api/v2/silence/{silence_id}"

        code, status = self.__call_url(method="DELETE", path=path)

        return code, status

    def __call_url(self, method="GET", path=None, data=None, headers=None):
        """ """
        if headers is None:
            headers = {"Accept": "application/json"}

        url = f"{self.url}/{path}"

        try:
            if method == "GET":
                response = requests.get(url, verify=False)
                response.raise_for_status()

            elif method == "POST":
                response = requests.post(url, json=data, verify=False)

                response.raise_for_status()

            elif method == "DELETE":
                response = requests.delete(url, verify=False)

                response.raise_for_status()

            else:
                self.module.log(msg=f"unsupported: {method}")

                return 500, f"Unsupported method '{method}'"

            return response.status_code, response.text  # json.loads(response.text)

        except requests.exceptions.HTTPError as e:
            self.module.log(msg=f"ERROR   : {e}")

            status_code = e.response.status_code
            status_message = e.response.text
            # self.module.log(msg=f" status_message : {status_message} / {type(status_message)}")
            # self.module.log(msg=f" status_message : {e.response.json()}")

            return status_code, status_message

        except ConnectionError as e:
            error_text = (
                f"{type(e).__name__} {(str(e) if len(e.args) == 0 else str(e.args[0]))}"
            )
            self.module.log(msg=f"ERROR   : {error_text}")
            self.module.log(
                msg="------------------------------------------------------------------"
            )
            return 500, error_text

        except Exception as e:
            self.module.log(msg=f"ERROR   : {e}")

            return response.status_code, response.text
