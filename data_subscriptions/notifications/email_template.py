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
        data = {"user": self.user, "packages": [], "new_package": []}
        for activities in self.activities_by_dataset():
            metadata = self.datasets[activities[0]["object_id"]]
            if activities[0].get("activity_type", False) == "new package":
                new_dataset_item = DatasetActivity(metadata, activities)()
                data["new_package"].append(new_dataset_item)
            else:
                dataset_item = DatasetActivity(metadata, activities)()
                if dataset_item is not None:
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
        self.ckan_api = RemoteCKAN(
            CKAN_URL,
            apikey=CKAN_API_KEY,
            user_agent="data-subscription/latest (API call for CKAN activity details)",
        )

    def __call__(self):
        pkg_url = urljoin(FRONTEND_SITE_URL,
                          self.dataset["organization"]["name"])
        items = {
            "title": self.dataset["title"],
            "name": self.dataset["name"],
            "url": "%s/%s" % (pkg_url, self.dataset["name"]),
            "activities": [],
        }
        for activity in self.activities:
            activity_msg = self.get_activity_type(activity)
            if activity_msg and (activity_msg not in items["activities"]):
                items["activities"].append(activity_msg)
        if items["activities"]:
            return items
        else:
            return None

    def get_activity_type(self, activity):
        # Check custom activity type eg. 'changed file'
        custom_activity_type = (
            activity["data"].get("body", {}).get("activity_type", False)
        )
        if custom_activity_type:
            return self.get_message_for_activity(custom_activity_type)

        activity_type_from_detail = self.get_activity_detail(activity["id"])

        if (activity["activity_type"] != "new package") and activity_type_from_detail:
            return self.get_message_for_activity(activity_type_from_detail)
        else:
            return self.get_message_for_activity(activity["activity_type"])

    def get_activity_detail(self, activity_id):
        details = self.ckan_api.action.activity_detail_list(id=activity_id)
        RemoteCKAN.close(self.ckan_api)

        if details:
            try:
                # Filter recent activity sorted by 'last_modified'
                detail = sorted(
                    details, key=lambda i: i["data"].get("resource", i["data"].get("package"))[
                        "last_modified"
                    ] or "", reverse=True,
                )[0]
            except:
                detail = details[0]

            object_type = detail["object_type"]
            activity_type = "%s %s" % (
                detail["activity_type"], object_type.lower())
            return activity_type
        else:
            return False

    def get_message_for_activity(self, activity_type):
        messages_for_activity_type = {
            "new package": "A new dataset has been created.",
            "new resource": "A new file has been added.",
            "changed resource": "A file and/or the metadata for a file has been updated.",
            "changed package": "The metadata for the dataset has been updated.",
            "changed file": "An existing file has been updated.",
            "deleted resource": "The dataset has been updated.",
            "deleted package": "The dataset has been updated.",
            "removed tag": "The tags have been changed.",
        }

        if activity_type in messages_for_activity_type.keys():
            return messages_for_activity_type[activity_type]
        else:
            return False
