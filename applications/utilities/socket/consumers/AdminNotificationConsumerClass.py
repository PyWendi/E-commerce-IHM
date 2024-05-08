from .commonImport import *

class AdminNotificationConsummer(AsyncWebsocketConsumer):
    """
    Consumme datd `for administrator from user` after purchase via channel in the room `admin_notification`
    """
    async def connect(self):
        # join group room
        self.room_group_name = "admin_notification"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print(self.channel_name)

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
            "type": "admin_notification",
            "operation": data_loaded
        })

    """
    Send back message from room group via websocket
    """
    async def admin_notification(self, event):
        operation = event["operation"] #Data from event

        # Sending message to websocket
        await self.send(text_data=json.dumps({"operation": operation}))
