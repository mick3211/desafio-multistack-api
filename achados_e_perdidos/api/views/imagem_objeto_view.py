from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.imagem_objeto_serializer import ImagemObjetoSerializer
from ..permissions.dono_permission import DonoPermission
from ..models import Objeto


class ImagemObjetoView(APIView):

    permission_classes = [DonoPermission]

    def post(self, request, objetoId, format=None):
        try:
            objeto = Objeto.objects.get(id=objetoId)
        except:
            return Response({'message': 'Objeto não encontrado'}, status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, objeto)
        serializer_objeto = ImagemObjetoSerializer(data=request.data,)
        if serializer_objeto.is_valid():
            objeto.imagem_objeto = serializer_objeto.validated_data['imagem_objeto']
            objeto.save()
            return Response({'mensagem': 'Imagem definida com sucesso!'}, status.HTTP_200_OK)
        return Response(serializer_objeto.errors, status.HTTP_400_BAD_REQUEST)