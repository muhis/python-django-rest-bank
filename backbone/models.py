from django.db import models
from django.utils  import timezone
from django.core.exceptions import ValidationError
from decimal import Decimal
# Create your models here.
class Accounts(models.Model):
    name = models.TextField()
    card = models.TextField()
    def Funds(self):
        '''Returns the Funds avaialable in that card,
        the return is the result of comparing the credit sum against the debit sum of any account.
        Will raise "Database corrupted" if a row has both debit and credit empty'''
        debit_sum = 0
        credit_sum = 0
        for transfer in Transfers.objects.filter(account = self):
            if transfer.debit != None:
                debit_sum += transfer.debit
            elif transfer.credit != None:
                credit_sum += transfer.credit
            else:
                raise Exception ('Database corrupted')
        return credit_sum - debit_sum

    def FundsAvailable(self, Amount):
        '''Takes Amount as integer and compare it against the avaialable balance.
        Return True if the card has the amount and returns false if there is insificint funds avaialable.
        '''
        #convert Amount into decimal in case it is pulled from a string.
        Amount = Decimal(Amount)
        funds = self.Funds()
        if funds >= Amount:
            return True

def AccountFromCard(Card):
    '''Takes a card_id and return an account object if it is valid. If the account is invalid it will return a false.'''
    if(Accounts.objects.filter(card = Card).exists()):
        return Accounts.objects.get(card = Card)
    else:
        return False

class Transactions(models.Model):
    #The fields that are Null(until settelment_amount field) are for development purposes, remove the null = True on deployment.
    #It is just to make the API calls in tests shorter, you don't have to fill the request everytime(countries and cities etc...)
    transaction_type = models.TextField()
    card_id = models.TextField()
    ref_transaction_id = models.TextField()
    destination_name = models.TextField()
    destination_city = models.TextField(null=True)
    destination_country = models.TextField(null=True)
    destination_mcc = models.TextField()
    billing_amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    billing_currency = models.TextField(null=True)
    transaction_amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    transaction_currency = models.TextField(null=True)
    settelment_amount = models.DecimalField(max_digits = 10, decimal_places = 2, null=True)
    settelment_currency = models.TextField(null=True)
    date = models.DateField(default=timezone.now)
    def is_possible(self):
        '''
        Checks if the object is a valid transaction.
        '''
        user_account = AccountFromCard(self.card_id)
        #Pull the Account connected to the card provided.
        if user_account:
            #There is such card in the system.
            reserved_account = Accounts.objects.get(pk=3)
            #In my implementation, I made three acounts for the internal use, this is one of them.
            #Reserved Account is where the credit is transfered if authoroisation is accepted.
            #With this implementation, it will be easy to track the money and give it back to the account if no settelement is received in 30 days.
            if self.transaction_type == 'authoroisation':
                if user_account.FundsAvailable(self.billing_amount):
                    #There is enough fund to authorise the payment.
                    self.save()
                    #Establish the transaction.
                    Transfer(user_account.card, reserved_account.card, self.billing_amount, self)
                    #Transfer the money to the reserved_account. The credit is now marked as reserved.
                    return True
                else:
                    return False
            elif self.transaction_type == 'settelement':
                if Transactions.objects.filter(ref_transaction_id = self.ref_transaction_id).exists():
                    #The transaction is related to a previously established transaction.
                    #In real application, Check also if the transsaction is authoroised for security reasons
                    #or dublicate settelement request.
                    reserved_account = Accounts.objects.get(pk=3)
                    revenue_account = Accounts.objects.get(pk=4)
                    #Bank internal revenue account.
                    scheme_account = Accounts.objects.get(pk=5)
                    #Bank internal debit account to the scheme.
                    authorised_transaction = Transactions.objects.get(ref_transaction_id = self.ref_transaction_id)
                    #Pull the old authorised transaction.
                    authorised_amount = authorised_transaction.billing_amount
                    #The billing amount from the old authorised Transaction.
                    billing_amount_dec = Decimal(self.billing_amount)
                    #The new requested billing amount(in the settelement transaction), convert it into decimal (it is received as string).
                    return_to_account = authorised_amount - billing_amount_dec
                    #return to the account the remainder of the authorised reserved payment.
                    if return_to_account > 0:
                        #There is a return, the authoroised billing amount is bigger than the settelment billing amount.
                        Transfer(reserved_account.card, user_account.card, return_to_account, authorised_transaction)
                        #Transfer the return from the reserved account into the user account.
                    elif return_to_account < 0:
                        #Pass the Authoroisation error here, the settelement asked is bigger than the authorised amount.
                        #According to Visa, the settelement billing amount can't be bigger than the authoroised billing amount.
                        return False
                    revenue = billing_amount_dec - Decimal(self.settelment_amount)
                    #Calculate the bank revenue from the (new settelement billing amount - settelement amount).
                    Transfer(reserved_account.card, revenue_account.card, revenue, authorised_transaction)
                    #Transfer the revenue from the reserved account into the revenue account.
                    Transfer(reserved_account.card, scheme_account.card, self.settelment_amount, authorised_transaction)
                    #Transfer the settelement amount to the scheme account so it can be paid accordingly.
                    authorised_transaction.billing_amount = self.billing_amount
                    authorised_transaction.billing_currency = self.billing_currency
                    authorised_transaction.settelment_amount = self.settelment_amount
                    authorised_transaction.settelment_currency = self.settelment_currency
                    authorised_transaction.transaction_type = 'settelement'
                    authorised_transaction.save()
                    #Update the transaction and save the new version.
                    return True
                else:
                    return False
            else:
                return False

        else:
            return False

class Transfers(models.Model):
    debit = models.DecimalField(max_digits = 10, decimal_places = 2, null=True)
    credit = models.DecimalField(max_digits = 10, decimal_places = 2, null=True)
    account = models.ForeignKey(Accounts)
    date = models.DateField(default=timezone.now)
    transaction = models.ForeignKey(Transactions)



def Transfer(source_card_id, destination_card_id, amount, related_transaction):
    '''Transfer(source_card_id as integer, destination_card_id as integer, amount as a decimal, related_transaction as Transaction object)
    Returns boolean True if the operation is successful. Used for internal accounts only, both card have to be registered'''
    source_account = AccountFromCard(source_card_id)
    destination_account = AccountFromCard(destination_card_id)
    debit_transfer_operation = Transfers(debit = amount, account = source_account, transaction = related_transaction)
    debit_transfer_operation.save()
    credit_transfer_operation = Transfers(credit = amount, account = destination_account, transaction = related_transaction)
    credit_transfer_operation.save()
    return True
