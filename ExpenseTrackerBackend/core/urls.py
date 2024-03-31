from django.urls import path
from . import views

urlpatterns = [
    path('api/devices/', views.DeviceListCreateAPIView.as_view(), name='device-list-create'),
    path('api/accounts/', views.AccountListCreateAPIView.as_view(), name='account-list-create'),
    path('api/transactions/', views.TransactionListCreateAPIView.as_view(), name='transaction-list-create'),
    # other URL patterns
    path('api/auth/', views.MyAuthenticatedAPIView.as_view(), name='my-auth-view'),
    path('api/add-card/', views.addAccount.as_view(), name='add-account'),
    path('api/get-cards/', views.getCards.as_view(), name='get-account'),
]
