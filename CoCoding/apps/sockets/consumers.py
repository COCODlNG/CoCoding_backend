import json
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.meetings.models import MeetingMemberRelation


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        self.relation = MeetingMemberRelation.objects.get(
            member=self.scope['user'],
            meeting_id=self.scope['url_route']['kwargs']['room_name'],
        )

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'add_user',
                'username': self.scope['user'].username,
            }
        )

    async def disconnect(self, close_code):
        self.relation.save()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'discard_user',
                'username': self.scope['user'].username,
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        text_data['username'] = self.scope['user'].username
        if text_data['action'] == 'edit_code':
            if text_data['username'] == text_data['current_user']:
                self.relation.code = text_data['code']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_message',
                'message': text_data,
            }
        )

    async def send_message(self, data):
        data = data['message']
        data['from'] = self.scope['user'].username
        await self.send(text_data=json.dumps(data))

    async def add_user(self, event):
        if not self.relation.code:
            self.relation.code = {
                'python': "print('hello python!')",
                'java': """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello java!");
    }
}
                """,
                'c': """#include<stdio.h>

void main(){
    printf("hello C!");
}
                """,
            }
        await self.send(text_data=json.dumps({
            'action': 'add_user',
            'username': event['username'],
            'code': self.relation.code,
            'is_admin': self.relation.is_admin_template(),
        }))

    async def discard_user(self, event):
        await self.send(text_data=json.dumps({
            'action': 'discard_user',
            'username': event['username'],
        }))
