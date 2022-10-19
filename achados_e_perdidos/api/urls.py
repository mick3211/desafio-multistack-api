from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import (
                    locais_view
                )

urlpatterns = [
    path('locais/', locais_view.LocaisView.as_view(), name='locais-list'),
    path('locais/imagem/', locais_view.ImagemLocalView.as_view(), name='imagem-local'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
