from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers.local_serializer import LocalSerializer, EditarLocalSerializer
from ..serializers.imagem_local_serializer import ImagemLocalSerializer
from rest_framework.permissions import IsAuthenticated
from ..services.local_service import get_local_by_user_id
from ..permissions.post_local_view_permission import PostLocalViewPermission

class LocaisView(APIView):

    permission_classes = [PostLocalViewPermission]

    def post(self, request, format=None):
        serializer_local = LocalSerializer(data=request.data)
        if serializer_local.is_valid():
            serializer_local.save()
            return Response(serializer_local.data, status.HTTP_201_CREATED)
        return Response(serializer_local.errors, status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, format=None):
        local = get_local_by_user_id(request.user.id)
        serializer_local = EditarLocalSerializer(local, data=request.data, context={'request': request})
        if serializer_local.is_valid():
            serializer_local.save()
            return Response(serializer_local.data)
        return Response(serializer_local.errors, status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        local = get_local_by_user_id(request.user.id)
        serializer_local = LocalSerializer(instance=local, context={'request': request})
        return Response(serializer_local.data)

    def delete(self, request, format=None):
        local = get_local_by_user_id(request.user.id)
        local.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImagemLocalView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer_imagem = ImagemLocalSerializer(data=request.data, context={"user": request.user})
        if serializer_imagem.is_valid():
            serializer_imagem.save()
            return Response({"message": 'Imagem definida com sucesso!'})
        return Response(serializer_imagem.errors, status.HTTP_400_BAD_REQUEST)

            