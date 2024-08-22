#!/usr/bin/python3
# -*- coding: utf-8 -*-

# (c) 2022-2023, Bodo Schulz <bodo@boone-schulz.de>

from __future__ import absolute_import, division, print_function

import json
import datetime

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.bodsch.prometheus.plugins.module_utils.alertmanager import Alertmanager


class AlertmanagerSilence():
    """
      Main Class
    """
    module = None

    def __init__(self, module):
        """
        """
        self.module = module

        self.state = module.params.get("state")
        self.verbose = module.params.get("verbose")
        self.url = module.params.get("url")
        self.silence_downtime = module.params.get("silence_downtime")
        self.silence_id = module.params.get("silence_id")
        # self.starts_at = module.params.get("starts_at")
        # self.ends_at = module.params.get("ends_at")
        self.comment = module.params.get("comment")
        self.matchers = module.params.get("matchers")

    def run(self):
        """
          runner
        """
        result = dict(
            failed=False,
        )

        alertmanager = Alertmanager(self.module)

        code, message = alertmanager.status()

        if code == 200:
            if isinstance(message, str):
                message = json.loads(message)

            # alertmanager_cluster = message.get("cluster")
            # self.module.log(msg=f"alertmanager cluster: {alertmanager_cluster}")

            if self.state == "check":
                code, message = alertmanager.silence()

                if isinstance(message, str):
                    message = json.loads(message)

                alerts_expired = [x.get("id") for x in message if x.get("status", {}).get("state") == "expired"]
                alerts_active = [x.get("id") for x in message if x.get("status", {}).get("state") == "active"]
                alerts_pending = [x.get("id") for x in message if x.get("status", {}).get("state") == "pending"]

                result.update({
                    "alerts": dict(
                        expired=alerts_expired,
                        active=alerts_active,
                        pending=alerts_pending
                    )
                })

            if self.state == "add":
                silence_downtime = self.current_datetime(self.silence_downtime)

                starts_at = silence_downtime.get("begin")
                ends_at = silence_downtime.get("end")

                payload = {
                    "matchers": self.matchers,
                    "startsAt": starts_at,
                    "endsAt": ends_at,
                    "createdBy": "automation",
                    "comment": self.comment,
                    "status": {
                        "state": "active"
                    }
                }

                # self.module.log(msg=f"= payload: {payload}")

                code, message = alertmanager.silence(payload=payload)

                if isinstance(message, str):
                    message = json.loads(message)

                silenceId = message.get("silenceID")

                result.update({
                    "changed": True,
                    "silence_id": silenceId,
                    "silence_start": starts_at,
                    "silence_end": ends_at
                })

            if self.state == "remove":
                if self.silence_id == "":
                    return dict(
                        failed=True,
                        msg="Missing silence_id to delete a active alertmanager silence."
                    )

                code, message = alertmanager.silence()

                msg = "silence succeccful removed."

                if code == 200:
                    if isinstance(message, str):
                        message = json.loads(message)

                    alerts_active = [x.get("id") for x in message if x.get("status", {}).get("state") == "active"]
                    alerts_expired = [x.get("id") for x in message if x.get("status", {}).get("state") == "expired"]

                    if self.silence_id in alerts_expired:
                        msg = "silence already expired"

                    else:
                        code, message = alertmanager.delete_silence(silence_id=self.silence_id)
                        self.module.log(msg=f"= code: {code}, status: {message}")

                result.update({
                    "msg": msg
                })

        else:
            result = dict(
                failed=True,
                msg=f"The alertmanager is not accessible under the URL {self.url}."
            )

        return result

    def current_datetime(self, add_time):
        """
        """
        add_minutes = add_time.get("minutes", 10)
        add_hours = add_time.get("hours", 0)

        current_date_time = datetime.datetime.now()  # .isoformat()

        if add_hours > 0:
            datetime_delta = datetime.timedelta(hours=add_hours)
        elif add_minutes > 0:
            datetime_delta = datetime.timedelta(minutes=add_minutes)

        end_date_time = (current_date_time + datetime_delta).isoformat()
        begin_date_time = current_date_time.isoformat()

        return dict(
            begin=begin_date_time,
            end=end_date_time
        )

# ===========================================
# Module execution.
#


def main():

    argument_spec = dict(
        state=dict(
            default="check",
            choices=["check", "add", "remove"]
        ),
        verbose=dict(
            type=bool,
            default=True
        ),
        url=dict(
            type=str,
            required=True
        ),
        silence_downtime=dict(
            type=dict,
            required=False,
            default=dict(minutes=10)
        ),
        silence_id=dict(
            type=str,
            required=False
        ),
        starts_at=dict(
            type=str,
            required=False
        ),
        ends_at=dict(
            type=str,
            required=False
        ),
        comment=dict(
            type=str,
            required=False
        ),
        matchers=dict(
            type=list,
            required=False
        ),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    s = AlertmanagerSilence(module)
    result = s.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
