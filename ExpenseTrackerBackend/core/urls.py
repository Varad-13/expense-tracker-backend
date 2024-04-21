from django.urls import path
from . import views

urlpatterns = [
    # General Paths
    path('api/auth/', views.TestLogin.as_view(), name='test-login'),
    path('api/delete_data/', views.deleteUserData.as_view(), name='delete-data'),
    # Card Paths
    path('api/add-card/', views.addAccount.as_view(), name='add-account'),
    path('api/get-cards/', views.getCards.as_view(), name='get-account'),
    path('api/delete-card/', views.deleteCard.as_view(), name='delete-account'),
    path('api/update-limit/', views.setLimit.as_view(), name='update-limit'),
    # Transaction Paths
    path('api/add-transaction/', views.addTransaction.as_view(), name='add-transaction'),
    path('api/get-transactions/', views.getTransactions.as_view(), name='get-transaction'),
    path('api/get-transaction-debit/', views.getDebitTransactions.as_view(), name='get-transaction-debit'),
    path('api/get-transaction-credit/', views.getCreditTransactions.as_view(), name='get-transaction-credit'),
    path('api/get-transaction-category/', views.getCategoryTransactions.as_view(), name='get-transaction-category'),
    path('api/get-transaction-card/', views.getCardTransactions.as_view(), name='get-transaction-card'),
    path('api/get-transaction-card-category/', views.getCardCategoryTransactions.as_view(), name='get-transaction-card-category'),
    path('api/delete-transaction/', views.deleteTransaction.as_view(), name='get-transaction'),
    path('api/delete-all-transaction/', views.deleteAllTransactions.as_view(), name='get-transaction'),
    path('api/update-transaction/', views.updateTransaction.as_view(), name='update-transaction'),
    # Limits
    path('api/get-limit/', views.getLimits.as_view(), name='get-limit'),
    path('api/get-total-limit/', views.getTotalLimits.as_view(), name='get-total-limit'),
    path('api/get-limit-card/', views.getLimitsCard.as_view(), name='get-limit-card'),
    path('api/reset-limit/', views.resetLimit.as_view(), name='reset-limit'),
    path('api/get-income-expense/', views.getCreditDebit.as_view(), name='get-income-expense'),
    path('analytics/<str:device_id>/', views.device_analytics, name='device_analytics'),
]
