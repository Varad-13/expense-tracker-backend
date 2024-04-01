from django.urls import path
from . import views

urlpatterns = [
    # General Paths
    path('api/auth/', views.TestLogin.as_view(), name='test-login'),
    # Card Paths
    path('api/add-card/', views.addAccount.as_view(), name='add-account'),
    path('api/get-cards/', views.getCards.as_view(), name='get-account'),
    path('api/delete-card/', views.deleteCard.as_view(), name='delete-account'),
    path('api/update-limit/', views.setLimit.as_view(), name='update-limit'),
    # Transaction Paths
    path('api/add-transaction/', views.addTransaction.as_view(), name='add-transaction'),
    path('api/get-transactions/', views.getTransactions.as_view(), name='get-transaction'),
    path('api/delete-transaction/', views.deleteTransaction.as_view(), name='get-transaction'),
    path('api/update-transaction/', views.updateTransaction.as_view(), name='update-transaction')
]
