import datetime as dt
import os

from ckanapi import RemoteCKAN


class LatestCKANActivity:
    def __init__(self, url=None, start_time=None, proposed_limit=1_000):
        self.url = url or os.getenv("CKAN_URL")
        self.start_time = start_time
        self.server_limit = proposed_limit
        self.current_offset = 0

    def __call__(self):
        api = RemoteCKAN(self.url)
        self.activity_list = []
        while True:
            response = api.action.recently_changed_packages_activity_list(
                limit=self.server_limit, offset=self.current_offset
            )
            self.activity_list += self.filter_response_for_time_range(response)
            if self.current_offset == 0:
                self.server_limit = len(response)
            self.current_offset += self.server_limit
            if self.has_reached_the_end(response):
                break
        return self.activity_list

    def filter_response_for_time_range(self, response):
        def is_in_time_range(item):
            timestamp = dt.datetime.fromisoformat(item["timestamp"])
            return (self.start_time is None) or (timestamp > self.start_time)

        return filter(is_in_time_range, response)

    def has_reached_the_end(self, last_response):
        items_returned = len(last_response)
        if items_returned == 0:
            return True

        return (self.current_offset > 0) and (
            (items_returned < self.server_limit) or (len(self.activity_list) == 0)
        )
