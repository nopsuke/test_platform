from django.core.management.base import BaseCommand
from .models import Trade, Asset
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Applies swap charges to all open positions'

    def handle(self, *args, **options):
        # Get all trades that are open
        open_trades = Trade.objects.filter(is_open=True)

        for trade in open_trades:
            # Calculate swap charge
            swap_charge = trade.asset.swap_charge * trade.trade_size

            # Subtract swap charge from user's balance
            user_profile = UserProfile.objects.get(user=trade.user)
            user_profile.balance -= swap_charge
            user_profile.save()

        self.stdout.write(self.style.SUCCESS('Successfully applied swap charges'))
