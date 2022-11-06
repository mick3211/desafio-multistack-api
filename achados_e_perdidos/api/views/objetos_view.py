from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.objeto_serializer import ObjetoSerializer
from ..services.local_service import get_local_by_user_id
from ..permissions.dono_permission import DonoPermission
from ..models import Objeto


class ObjetoView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        local_id = get_local_by_user_id(request.user.id).id
        objetos = Objeto.objects.filter(local_id=local_id)
        serializer_objeto = ObjetoSerializer(objetos, many=True, context={'request': request})
        return Response(serializer_objeto.data, status.HTTP_200_OK)


    def post(self, request, format=None):
        local_id = get_local_by_user_id(request.user.id).id
        serializer_objeto = ObjetoSerializer(data=request.data, context={'request': request})

        if serializer_objeto.is_valid():
            serializer_objeto.save(local_id=local_id)
            return Response(serializer_objeto.data, status.HTTP_201_CREATED)
        return Response(serializer_objeto.errors, status.HTTP_400_BAD_REQUEST)


class ObjetoViewId(APIView):

    permission_classes = [DonoPermission]

    def get(self, request, objetoId, format=None):
        try:
            objeto = Objeto.objects.get(id=objetoId)
        except:
            return Response({'message': 'Objeto não encontrado'}, status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, objeto)
        serializer_objeto = ObjetoSerializer(objeto, context={'request': request})
        return Response(serializer_objeto.data, status.HTTP_200_OK)

    def put(self, request, objetoId, format=None):
        try:
            objeto = Objeto.objects.get(id=objetoId)
        except:
            return Response({'message': 'Objeto não encontrado'}, status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, objeto)
        serializer_objeto = ObjetoSerializer(objeto, request.data, context={'request': request})
        if serializer_objeto.is_valid():
            serializer_objeto.save()
            return Response(serializer_objeto.data, status.HTTP_200_OK)
        return Response(serializer_objeto.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, objetoId, format=None):
        try:
            objeto = Objeto.objects.get(id=objetoId)
        except:
            return Response({'message': 'Objeto não encontrado'}, status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, objeto)
        objeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

