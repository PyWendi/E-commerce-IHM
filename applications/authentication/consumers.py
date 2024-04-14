import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ClientConsummer(WebsocketConsumer):
    """
    Asynchrone version of the client consummer
    """
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"admin_{self.room_name}"

        # join group room
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """
        Leave room group
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    """
    Recieve message from websocket
    """
    def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "client_message", "message": message}
        )

    """
    Send back message from room group via websocket
    """
    def client_message(self, event):
        message = event["message"]

        # Sending message to websocket
        self.send(text_data=json.dumps({"message": message}))


    """
    This is the synchrone version
    """
    # def connect(self):
    #     print("***********\nA user is connected\n--------")
    #     self.accept()
    #
    # def disconnect(self, close_code):
    #     print("-----------\nA user is disconnected\n************")
    #     pass
    #
    # def receive(self, text_data):
    #     print("Data recieved succesfully *********")
    #     text = json.loads(text_data)
    #     message = text["message"]
    #
    #     self.send(text_data=json.dumps({"message": message}))
