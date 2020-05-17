import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = set()

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.users.add(self.scope['user'])
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'add_user',
            }
        )

    async def disconnect(self, close_code):
        self.users.remove(self.scope['user'])
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message in ['Python', 'Java', 'C']:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        else:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

    async def chat_message(self, event):
        message = event['message']
        if message in {'Python', 'Java', 'C'}:
            await self.send(text_data=json.dumps({
                'lang': message
            }))
        else:
            await self.send(text_data=json.dumps({
                'message': message
            }))

    async def add_user(self, event):
        user = self.scope['user']
        await self.send(text_data=json.dumps({
            'action': 'add_user',
            'username': user.username,
        }))

    async def call_user(self, data):
        user = self.scope['user']
        to = data['to']
        await self.send(text_data=json.dumps({
            'action': 'call_user',
            'from': user.username,
            'to': data['to'],
            'offer': data['offer'],
        }))

    async def answer(self, data):
        user = self.scope['user']
        await self.send(text_data=json.dumps({
            'action': 'add_user',
            'username': user.username,
        }))
