from backbone.models import Transactions
from backbone.serializers import TransactionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class TransactionsView(APIView):
    #Uncomment in development if you want to recieve the objects as answer to GET requests.
    #def get(self, request, format=None):
        #
        #transaction = Transactions.objects.all()
        #serializer = TransactionSerializer(transaction, many=True)
        #return Response(serializer.data)
    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        #Create a serializer object with the data received.
        if serializer.is_valid():
            #use serializer builtin validater to check that the object is complete.
            serialized_data = serializer.data
            this_transaction = Transactions(**serializer.data)
            #Use the validated information as a dictionary to construct new Transactions object.\
            if this_transaction.is_possible():
                #Provoke the method is_possible on the new object to check if that Transaction is valid.
                return Response(status=status.HTTP_200_OK)
                #If valid, returns an http 200 Response.
        return Response(status=status.HTTP_403_FORBIDDEN)
        #check failed and there is something wrong, respond with a http response 403.
