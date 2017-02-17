from django.core.management.base import BaseCommand, CommandError
from backbone.models import Accounts, Transfers
class Command(BaseCommand):
    help = 'Calculate the revenue, needs no arguments'

    def handle(self, *args, **options):
        revenue_account = Accounts.objects.get(pk=4)
        accounting = Transfers.objects.filter(account=revenue_account)

        summation = 0
        for transfer in accounting:
            summation += transfer.credit
            text_out = 'ID = %s ~~~ +%s ~~~ on %s ' % (transfer.id, transfer.credit, transfer.date)
            self.stdout.write(self.style.SUCCESS(text_out))
        text_out = 'The Summation of the credit of the revenue is %s' % summation
        self.stdout.write(self.style.SUCCESS(text_out))
