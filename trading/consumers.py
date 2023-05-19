from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .market_data import calculate_equity
from accounts.models import UserProfile




class EquityConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user_profile = self.scope["user"].userprofile
        self.room_group_name = f'equity_{self.user_profile.id}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def equity_message(self, event):
        equity = event['equity']
        await self.send_json(content={'equity': equity})



