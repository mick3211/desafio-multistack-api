from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import (
                    locais_view,
                    objetos_view,
                    imagem_objeto_view,
                    locais_busca_view,
                    informar_entrega_view,
                )

urlpatterns = [
    path('locais/', locais_view.LocaisView.as_view(), name='locais-list'),
    path('locais/busca', locais_busca_view.LocaisBuscaView.as_view(), name='locais-busca-list'),
    path('locais/<int:local_id>/objetos', locais_busca_view.ObjetosLocalBuscaView.as_view(), name='objetos-local-list'),
    path('locais/imagem/', locais_view.ImagemLocalView.as_view(), name='imagem-local'),
    path('objetos/', objetos_view.ObjetoView.as_view(), name='objetos-list'),
    path('objetos/<int:objetoId>/', objetos_view.ObjetoViewId.as_view(), name='objeto-detail'),
    path('objetos/<int:objetoId>/imagem/', imagem_objeto_view.ImagemObjetoView.as_view(), name='imagem-objeto'),
    path('objetos/<int:objetoId>/donos/', informar_entrega_view.InformarEntregaView.as_view(), name='dono-objeto-list'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
