from django.urls import path
from .views import (
                    locais_view
                )

urlpatterns = [
    path('locais/', locais_view.LocaisView.as_view(), name='locais-list'),
    path('locais/imagem/', locais_view.ImagemLocalView.as_view(), name='imagem-local'),
]
