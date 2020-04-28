from flask_restful import Resource, request
from flask import Response

from data_subscriptions.models import Subscription as Model
from data_subscriptions.notifications.ckan_metadata import CKANMetadata

def create_csv(dataset, columns):
    header = ','.join(columns)
    content = header + '\n'

    for data in dataset:
        row = ','.join(data.values())
        content += row + '\n'
    return content

def get_user(user_id):
    result = CKANMetadata("user_show", [user_id])()
    if user_id in result:
        return result[user_id]
    return {"display_name": ""}

def get_dataset(dataset_id):
    result = CKANMetadata("package_show", [dataset_id])()
    if dataset_id in result:
        return result[dataset_id]
    return {"name": ""}
    
def prepare_stat(data):
    dataset_name = get_dataset(data.dataset_id)["name"]
    user_name = get_user(data.user_id)["display_name"]
    
    return {
        "subscribed_at": str(data.created_at),
        "user_id": data.user_id,
        "user_name": user_name,
        "dataset_id": data.dataset_id,
        "dataset_name": dataset_name,
    }
        
class Stat(Resource):
    def get(self):
        dataset = Model.query.all()
        result = map(prepare_stat, dataset)
        download = request.args.get('download')
        if download == "yes":
            columns = ["Subscribed At", "User ID","Username", "Dataset ID", "Dataset Name"]
            csv = create_csv(result, columns)
            return Response(
                csv,
                mimetype="text/csv",
                headers={"Content-disposition":
                        "attachment; filename=myplot.csv"})
        return { "result": list(result) }
    

   
        
        