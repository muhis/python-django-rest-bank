from .models import Accounts, Transactions, Transfers, AccountFromCard
from datetime import datetime
from .serializers import TransactionSerializer, TransfersSerializer
def CardHolderTransactions(card, from_date, to_date):
    '''
    Returns the setteled and cash account transaction within a time period as an array.
    Dates format are expected to be 'YYYY-MM-DD' where Y is year, M is month and y is day.
    It will return if the account is not found.
    '''
    account = AccountFromCard(card)
    if account:
        start_date = datetime.strptime(from_date, "%Y-%m-%d")
        end_date = datetime.strptime(to_date, "%Y-%m-%d")
        card_holder_transactions = Transactions.objects.filter(card_id = card , date__range =(start_date, end_date)).exclude(transaction_type = 'authoroisation')
        transactions = TransfersSerializer(card_holder_transactions, many = True).data
        return transactions
    else:
        return 'Account can not be found'

def LedgerBalance(card):
    '''
    Return an array contains the transfers of a certain card excluding authorised transfers.
    >>>LedgerBalance('card_id')
    >>>[OrderedDict([('id', id integer), ('debit', String or None), ('credit', String or None), ('date', String), ('account', internal account Id), ('transaction', related transaction id as integer)])]
    '''
    account = AccountFromCard(card)
    #Pull hte account object that holds the card.
    if account:
        #The card belongs to an account.
        account_balance = Transfers.objects.filter(account=account).exclude(transaction__transaction_type = 'authoroisation')
        #Search for Transactions made by this account and which type is not 'authoroisation'
        balance = TransfersSerializer(account_balance, many=True).data
        #Serialize the data to convert it to simple python array object.
        return balance
    else:
        return 'Card %s can not be found' % card

def AvailableBalance(card):
    '''
    Return all the transfers of a card including the authorised payments.
    >>>AvailableBalance('Card_id')
    >>>[OrderedDict([('id', id integer), ('debit', String or None), ('credit', String or None), ('date', String), ('account', internal account Id), ('transaction', related transaction id as integer)])]
    '''
    account = AccountFromCard(card)
    #Pull hte account object that holds the card.
    if account:
        #The card belongs to an account.
        account_balance = Transfers.objects.filter(account=account)
        #Search for Transactions made by this account
        balance = TransfersSerializer(account_balance, many=True).data
        #Serialize the data to convert it to simple python array object.
        return balance
    else:
        return 'Card %s can not be found' % card
