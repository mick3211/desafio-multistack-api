from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Local
from ..serializers.locais_busca_serializer import LocaisBuscaSerializer
from ..models import Objeto
from ..serializers.objeto_serializer import ObjetoSerializer


class LocaisBuscaView(APIView):

    def get(self, request, format=None):
        nome = request.query_params.get('nome')
        locais = Local.objects.filter(nome=nome)

        locais_serializer = LocaisBuscaSerializer(locais, many=True)

        return Response(locais_serializer.data)


class ObjetosLocalBuscaView(APIView):

    def get(self, request, local_id, format=None):
        objetos = Objeto.objects.filter(local_id=local_id)
        serializer_objeto = ObjetoSerializer(objetos, many=True, context={'request': request})
        return Response(serializer_objeto.data, status.HTTP_200_OK)