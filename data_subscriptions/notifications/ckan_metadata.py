import logging
import os

from ckanapi import RemoteCKAN, errors

CKAN_URL = os.getenv("CKAN_URL")
CKAN_API_KEY = os.getenv("CKAN_API_KEY")


class CKANMetadata:
    def __init__(self, action, entity_ids):
        self.action = action
        self.entity_ids = entity_ids
        self.api = RemoteCKAN(CKAN_URL, apikey=CKAN_API_KEY)

    def __call__(self):
        endpoint = getattr(self.api.action, self.action)
        metadata = {}
        for item_id in set(self.entity_ids):
            try:
                metadata[item_id] = endpoint(id=item_id)
            except errors.NotFound:
                url = f"action = {self.action} id={item_id}"
                logging.error(f"CKAN API NotFound error: {url}")

        return metadata
