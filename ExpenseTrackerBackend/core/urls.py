from django.urls import path
from . import views

urlpatterns = [
    # Login Test
    path('api/auth/', views.MyAuthenticatedAPIView.as_view(), name='my-auth-view'),
    # Card Paths
    path('api/add-card/', views.addAccount.as_view(), name='add-account'),
    path('api/get-cards/', views.getCards.as_view(), name='get-account'),
    path('api/delete-card/', views.deleteCard.as_view(), name='delete-account'),
    path('api/update-limit/', views.setLimit.as_view(), name='update-limit'),
]
