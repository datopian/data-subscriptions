from itertools import groupby
from operator import itemgetter
import os
from urllib.parse import urljoin

from ckanapi import RemoteCKAN

FRONTEND_SITE_URL = os.getenv("FRONTEND_SITE_URL")

CKAN_URL = os.getenv("CKAN_URL")
CKAN_API_KEY = os.getenv("CKAN_API_KEY")


class EmailTemplateData:
    """
    Build metadata for email template in SendGrid.
    """

    def __init__(self, user, datasets, activities):
        self.user = user
        self.datasets = datasets
        self.activities = activities

    def template_data(self):
        data = {"packages": []}
        data.update({"user": self.user})
        for activities in self.activities_by_dataset():
            metadata = self.datasets[activities[0]["object_id"]]
            dataset_item = DatasetActivity(metadata, activities)()
            data["packages"].append(dataset_item)
        return data

    def activities_by_dataset(self):
        xs = []
        for _, grouper in groupby(self.activities, itemgetter("dataset_id")):
            xs.append([x["activity"] for x in grouper])
        return xs


class DatasetActivity:
    """
    Build metadata, of a single dataset, for email template in SendGrid.
    """

    def __init__(self, dataset, activities):
        self.dataset = dataset
        self.activities = activities
        self.ckan_api = RemoteCKAN(CKAN_URL, apikey=CKAN_API_KEY)

    def __call__(self):
        pkg_url = urljoin(FRONTEND_SITE_URL, self.dataset["organization"]["name"])
        items = {
            "title": self.dataset["title"],
            "url": "%s/%s" % (pkg_url, self.dataset["name"]),
            "activities": [],
        }

        for activity in self.activities:
            if self.get_activity_type(activity) not in items["activities"]:
                items["activities"].append(self.get_activity_type(activity))
        return items

    def get_activity_type(self, activity):
        messages_for_activity_type = {
            "new package": "A new dataset has been created.",
            "new resource": "A new file has been added.",
            "changed resource": "The metadata for a file has been updated.",
            "changed package": "The metadata for the dataset has been updated.",
            "changed file": "An existing file has been updated.",
            "deleted resource": "The dataset has been updated.",
            "deleted package": "The dataset has been updated.",
            "removed tag": "The tags have been changed.",
        }

        activity_type = activity["data"].get("body", {}).get("activity_type", False)

        if activity_type:
            return messages_for_activity_type[activity_type]

        details = self.ckan_api.action.activity_detail_list(id=activity["id"])

        if len(details) == 1:
            detail = details[0]
            object_type = detail["object_type"]
            new_activity_type = "%s %s" % (detail["activity_type"], object_type.lower())
            activity["activity_type"] = new_activity_type

        if "activity_type" in activity:
            return messages_for_activity_type[activity.get("activity_type")]
