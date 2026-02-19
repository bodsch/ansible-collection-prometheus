# python 3 headers, required if submitting to Ansible

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import datetime

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """ """

    def filters(self):
        return {
            "expired": self.expired,
            "current_datetime": self.current_datetime,
        }

    def current_datetime(self, data, add_time):
        """ """
        add_minutes = add_time.get("minutes", 10)
        add_hours = add_time.get("hours", 0)

        current_date_time = datetime.datetime.now()

        if add_hours > 0:
            datetime_delta = datetime.timedelta(hours=add_hours)
        elif add_minutes > 0:
            datetime_delta = datetime.timedelta(minutes=add_minutes)

        end_date_time = (current_date_time + datetime_delta).isoformat()
        begin_date_time = current_date_time.isoformat()

        return dict(begin=begin_date_time, end=end_date_time)

    def expired(self, data):
        """ """
        result = []

        if isinstance(data, list):
            for i in data:
                _id = i.get("id")
                _state = i.get("status", {}).get("state", None)

                if _state == "expired":
                    result.append(_id)

        return result
