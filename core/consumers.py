from channels.generic.websocket import AsyncWebsocketConsumer
import json

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("users", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("users", self.channel_name)

    async def send_user_notification(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))




class UserNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "users"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Получение сообщений от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_user_notification',
                'message': message
            }
        )


    async def send_user_notification(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
