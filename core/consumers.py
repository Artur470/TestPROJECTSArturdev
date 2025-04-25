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
        # Создаём группу пользователей, которая будет принимать уведомления
        self.group_name = "users"

        # Подключаемся к группе
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединяемся от группы при закрытии соединения
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Получение сообщений от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Отправляем сообщение всем пользователям в группе
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_user_notification',
                'message': message
            }
        )

    # Обработка сообщения и отправка его на WebSocket
    async def send_user_notification(self, event):
        message = event['message']

        # Отправляем уведомление на WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
