from itertools import groupby
from ckanapi import RemoteCKAN
import os

FRONTEND_SITE_URL = os.getenv("FRONTEND_SITE_URL")

CKAN_URL = os.getenv("CKAN_URL")
CKAN_API_KEY = os.getenv("CKAN_API_KEY")

HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Datasets you subscribed were recently changed</title>
    <style>
        body {{padding : 0 5px}}
        p {{margin: 0px;}}
        a {{margin:0;}}
        ul {{margin: 8px 1px 10px 1px;}}
    </style>
  </head>
  <body>
    <p>Dear {user_name},</p><br>

    <p>The following dataset(s) to which you are subscribed have recently been updated on the ESO data portal:</p></br>

    <div>
    {activities}
    <div>

    <br>
    <p><a href='{frontend_url}/dashboard'>View recent updates to your subscribed datasets.</a></p>
    <p><a href='{frontend_url}/settings'>Manage your subscriptions.</a><p>
    <br>

    <p>Regards,</p>
    <p>ESO Data Portal Team</p>
    <p>nationalgridESO</p>
    <p><a href='mailto:box.OpenData.ESO@nationalgrideso.com'>box.OpenData.ESO@nationalgrideso.com</a></p>
  </body>
</html>
"""


class EmailTemplate:
    def __init__(self, user, datasets, activities):
        self.user = user
        self.datasets = datasets
        self.activities = activities

    def html_content(self):
        html_list = ""
        for activities in self.activities_by_resource():
            metadata = self.datasets[activities[0]["object_id"]]
            html = ActivityPresenter(metadata, activities)()
            html_list += html
        return HTML.format(
            user_name=self.user["name"],
            activities=html_list,
            frontend_url=FRONTEND_SITE_URL,
        )

    def activities_by_resource(self):
        activities = []
        for _, xs in groupby(self.activities, lambda x: x["object_id"]):
            activities.append(list(xs))
        return activities


class ActivityPresenter:
    def __init__(self, dataset, activities):
        self.dataset = dataset
        self.activities = activities
        self.ckan_api = RemoteCKAN(CKAN_URL, apikey=CKAN_API_KEY)

    def __call__(self):
        name = self.dataset["title"]
        pkg_url = self.dataset["organization"]["name"] + "/" + self.dataset["name"]
        html = "<a href='%s/%s'>%s</a>:" % (FRONTEND_SITE_URL, pkg_url, name)
        html += f"<ul>"
        items = []
        for activity in self.activities:
            item = "<li>%s</li>" % (self.activity_msg_stream(activity))
            items.append(item)

        return html + "".join(set(items)) + "</ul>"

    def activity_msg_stream(self, activity):

        activity_stream_string_functions = {
            "new resource": f"A new file has been added.",
            "changed resource": f"A metadata for the resource has been udpated.",
            "changed package": f"A metadata for the dataset has been udpated.",
            "changed file": f"An existing file has been updated.",
            "deleted resource": f"The dataset has been udpated.",
            "deleted package": f"The dataset has been udpated.",
        }

        activity_type = activity["data"].get("body", {}).get("activity_type", False)
        # Check API activity
        if activity_type:
            return activity_stream_string_functions[activity_type]

        details = self.ckan_api.action.activity_detail_list(id=activity["id"])

        # Check activity detail
        if len(details) == 1:
            detail = details[0]
            object_type = detail["object_type"]
            new_activity_type = "%s %s" % (detail["activity_type"], object_type.lower())

            if new_activity_type in activity_stream_string_functions:
                activity["activity_type"] = new_activity_type

        if "activity_type" in activity:
            return activity_stream_string_functions[activity["activity_type"]]
