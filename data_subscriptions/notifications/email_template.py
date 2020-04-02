from itertools import groupby

HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Datasets you subscribed were recently changed</title>
  </head>
  <body>
    <p>Hi {user_name},</p>

    <p>The following datasets changed since the last time you checked:</p>

    <p>
      {activities}
    </p>
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
            html = ResourceActivitiesPresenter(metadata, activities)()
            html_list += html
        return HTML.format(user_name=self.user["name"], activities=html_list)

    def activities_by_resource(self):
        activities = []
        for _, xs in groupby(self.activities, lambda x: x["object_id"]):
            activities.append(list(xs))
        return activities


class ResourceActivitiesPresenter:
    def __init__(self, dataset, activities):
        self.dataset = dataset
        self.activities = activities

    def __call__(self):
        name = self.dataset["organization"]["title"] + " / " + self.dataset["title"]
        html = f"<strong>{name}</strong>"
        html += f"<br><ul>"
        items = []
        for activity in self.activities:
            item = ActivityPresenter(self.dataset, activity)()
            items.append(item)

        return html + "".join(set(items)) + "</ul>"


class ActivityPresenter:
    def __init__(self, dataset, activity):
        self.dataset = dataset
        self.activity = activity

    def __call__(self):
        self._assign_attributes()
        if self._changed_data:
            # resource_id = self.activity["body"]["resource_id"]
            message = f"The data inside a resource have changed."
        elif self._changed_metadata:
            message = f"The properties have changed."
        return f"<li>{message}</li>"

    def _assign_attributes(self):
        action = self.activity["data"].get("action")
        self._changed_data = action and action.startswith("datastore_")
        self._changed_metadata = self.activity["activity_type"] == "changed package"
