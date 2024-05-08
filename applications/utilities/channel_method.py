from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def trigger_channel(room, data):
    channel = get_channel_layer()
    async_to_sync(channel.group_send)(room, data)