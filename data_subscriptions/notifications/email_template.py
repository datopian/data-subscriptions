class EmailTemplate:
    def __init__(self, user_id, activities):
        self.user_id = user_id
        self.activities = activities

    def html_content(self):
        return (
            f"User {self.user_id}, these are the latest changes: <br>{self.activities}"
        )
