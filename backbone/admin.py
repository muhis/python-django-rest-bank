from django.contrib import admin
from .models import Accounts, Transfers, Transactions
# Register your models here.
admin.site.register(Accounts)
admin.site.register(Transfers)
admin.site.register(Transactions)
