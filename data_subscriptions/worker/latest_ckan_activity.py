import datetime as dt
import os
import logging

from ckanapi import RemoteCKAN


class LatestCKANActivity:
    """
    Fetch all the CKAN activity list, since a given start time.
    """

    def __init__(self, url=None, start_time=None, proposed_limit=100):
        self.url = url or os.getenv("CKAN_URL")
        self.start_time = start_time
        self.server_limit = proposed_limit
        self.current_offset = 0

    def __call__(self):
        with RemoteCKAN(
            self.url,
            user_agent="data-subscription/latest (API call for CKAN recent activity pull)",
        ) as api:

          self.activity_list = []
          while True:
              logging.info(f"LatestCKANActivity: fetching activities {self.server_limit} - {self.current_offset}")
              response = api.action.recently_changed_packages_activity_list(
                  limit=self.server_limit, offset=self.current_offset
              )
              self.activity_list += self.filter_response_for_time_range(response)
              if self.current_offset == 0:
                  self.server_limit = len(response)
              self.current_offset += self.server_limit
              if self.has_reached_the_end(response):
                  logging.info("LatestCKANActivity: has reached the end - stop")
                  break
          logging.info("LatestCKANActivity: return list of activities")
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

        items_after_filter = self.filter_response_for_time_range(last_response)
        if len(list(items_after_filter)) < items_returned:
            return True

        return (self.current_offset > 0) and (
            (items_returned < self.server_limit) or (len(self.activity_list) == 0)
        )
