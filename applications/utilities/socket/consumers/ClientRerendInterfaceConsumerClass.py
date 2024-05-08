from .commonImport import *

class ClientRerendInterfaceConsumer(AsyncWebsocketConsumer):
    """
    Consumme datd `for administrator from user` after purchase via channel in the room `admin_notification`
    """
    async def connect(self):
        # join group room
        self.room_group_name = "client_rerend"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        Leave room group
        """
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    """
    Recieve message from websocket
    """

    async def receive(self, text_data=None):
        data_loaded = json.loads(text_data)
        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, {
            "type": "client_rerend",
            "data": data_loaded
        })

    """
    Send back message from room group via websocket
    """
    async def client_rerend(self, event):
        operation = event["data"]

        # Sending message to websocket
        await self.send(text_data=json.dumps(operation))
