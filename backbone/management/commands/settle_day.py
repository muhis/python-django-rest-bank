from django.core.management.base import BaseCommand, CommandError
from backbone.models import Accounts, Transactions, Transfers
from datetime import datetime
class Command(BaseCommand):
    help = 'Calculate the scheme debit on a certain day, input a date as YYYY-MM-DD or leave empty to use today.'

    def add_arguments(self, parser):
        parser.add_argument('Date', default = datetime.now(), nargs='?', type = str)

    def handle(self, *args, **options):
        Date = options.get('Date',None)
        scheme_account = Accounts.objects.get(pk=5)
        accounting = Transfers.objects.filter(account=scheme_account, date = Date)
        summation = 0
        for transfer in accounting:
            summation += transfer.credit
            text_out = 'ID = %s ~~~ +%s ~~~ on %s ' % (transfer.id, transfer.credit, transfer.date)
            self.stdout.write(self.style.SUCCESS(text_out))
        text_out = 'The Summation of the debit on %s to the scheme is %s' % (Date, summation)
        self.stdout.write(self.style.SUCCESS(text_out))
