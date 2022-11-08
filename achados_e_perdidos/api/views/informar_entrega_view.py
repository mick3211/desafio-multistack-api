from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..permissions.dono_permission import DonoPermission
from ..models import Objeto
from ..serializers.informar_entrega_serializer import InformarEntregaSerializer


class InformarEntregaView(APIView):

    permission_classes = [DonoPermission]

    def post(self, request, objetoId, format=None):
        try:
            objeto = Objeto.objects.get(id=objetoId)
        except:
            return Response({'message': 'Objeto não encontrado'}, status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, objeto)
        serializer_objeto = InformarEntregaSerializer(data=request.data, context={"request": request});
        if serializer_objeto.is_valid():
            objeto.dono_nome = serializer_objeto.data['dono_nome']
            objeto.dono_cpf = serializer_objeto.data['dono_cpf']
            objeto.entregue = True
            objeto.save()
            return Response('Dono do objeto definido com sucesso')
        return Response(serializer_objeto.errors, status.HTTP_400_BAD_REQUEST)