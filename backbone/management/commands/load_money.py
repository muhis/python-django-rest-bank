from django.core.management.base import BaseCommand, CommandError
from backbone.models import Accounts, Transactions, Transfer, AccountFromCard
class Command(BaseCommand):
    help = 'Adds money to certain card.'
    def add_arguments(self, parser):
        parser.add_argument('Card', nargs='+', type = str)
        parser.add_argument('Amount', nargs='+', type = int)
        parser.add_argument('Currency', nargs='+', type = str)
    def handle(self, *args, **options):
        Card = options['Card'][0]
        Amount = options['Amount'][0]
        Currency = options['Currency'][0]
        Source = Accounts.objects.get(pk=1)
        user_account = AccountFromCard(Card)
        if (user_account):
            this_transaction = Transactions(transaction_type = 'Cash', card_id = Card,  destination_name = user_account.name, destination_mcc = user_account.card,transaction_amount = Amount, settelment_amount = Amount, billing_amount = Amount, billing_currency = Currency)
            this_transaction.save()
            Transfer('XXXX', Card, Amount, this_transaction)
            self.stdout.write(self.style.SUCCESS('Sucessfully loaded money to %s' % Card))
        else:
            raise CommandError('FAILED: Can not find card %s' % Card)
