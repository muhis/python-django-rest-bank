from rest_framework import serializers
from .models import Transactions, Transfers

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ('__all__')

class TransfersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfers
        fields = ('__all__')
