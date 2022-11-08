from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Local
from ..serializers.locais_busca_serializer import LocaisBuscaSerializer
from ..models import Objeto
from ..serializers.objeto_serializer import ObjetoSerializer
from django.db.models import Q


class LocaisBuscaView(APIView):

    def get(self, request, format=None):
        nome = request.query_params.get('nome')
        id = request.query_params.get('id')
        query_params = Q(pk=id) | Q(nome__icontains=nome) if nome else Q(pk=id)
        locais = Local.objects.filter(query_params)

        locais_serializer = LocaisBuscaSerializer(locais, many=True, context={'request': request})

        return Response(locais_serializer.data)


class ObjetosLocalBuscaView(APIView):

    def get(self, request, local_id, format=None):
        objetos = Objeto.objects.filter(local_id=local_id)
        serializer_objeto = ObjetoSerializer(objetos, many=True, context={'request': request})
        return Response(serializer_objeto.data, status.HTTP_200_OK)