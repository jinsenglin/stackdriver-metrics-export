# Import python built-in library
import base64
import json

# Import google cloud library
from google.cloud import resource_manager

# Import custom library
import config

# Initialize global variable
client = resource_manager.Client()

# Define function
def get_projects():
    try:
        # Lists all current projects
        projects = client.list_projects()
        print("Got past list_projects() call")
        
        # Set a uniform endTime for all the resulting messages
        #
        # TODO
        #
        # sample 2019-11-12T17:58:26.068483Z
        
        for project in projects:
            # Only publish messages for active projects
            #
            # TODO
            #
            pass

    except:
        raise

# Define entrypoint
def list_projects(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
         event. The `data` field contains the PubsubMessage message. The
         `attributes` field will contain custom attributes if there are any.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata. The `event_id` field contains the Pub/Sub message ID. The
         `timestamp` field contains the publish time.
    """

    print("""This Function was triggered by messageId {} published at {}
    """.format(context.event_id, context.timestamp))

    if 'data' in event:
        data = base64.b64decode(event['data']).decode('utf-8')
        
        jsonMessage = None
        try:
            jsonMessage = json.loads(data)
        except TypeError:
            raise TypeError('Error parsing input message')
        
        if jsonMessage and 'token' in jsonMessage:
            token = jsonMessage['token']
            if token == config.TOKEN:
                return get_projects()
            else:
                raise RuntimeError('The token property in the pubsub message does not match, not processing')
        else:
            raise ValueError("No token property in the pubsub message, not processing")
    else:
        raise RuntimeError('Not found data in event')
