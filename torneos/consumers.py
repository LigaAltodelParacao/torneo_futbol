from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PartidoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.partido_id = self.scope['url_route']['kwargs']['partido_id']
        self.group_name = f'partido_{self.partido_id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # Reenvía a todos los conectados al partido
        await self.channel_layer.group_send(self.group_name, {
            'type': 'broadcast',
            'message': text_data
        })

    async def broadcast(self, event):
        await self.send(text_data=event['message'])
