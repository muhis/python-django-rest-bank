from django.conf.urls import url
from backbone import models
from backbone import views
urlpatterns = [
url(r'^', views.TransactionsView.as_view())
]
