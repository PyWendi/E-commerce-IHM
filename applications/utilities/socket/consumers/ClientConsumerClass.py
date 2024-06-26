from .commonImport import *


class ClientConsummer(AsyncWebsocketConsumer):
    """
    Asynchrone version of the client consummer
    """
    async def connect(self):
        self.clientId = self.scope["url_route"]["kwargs"]["clientId"]
        self.room_group_name = f"client_{self.clientId}_notification"

        # join group room
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        Leave room group
        """
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    """
    Recieve message from websocket
    """
    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "client_notification", "operation": text_data_json}
        )

    """
    Send back message from room group via websocket
    """
    async def client_notification(self, event):
        print(event)
        operation = event["operation"]

        # Sending message to websocket
        await self.send(text_data=json.dumps({"opeartion": operation}))

