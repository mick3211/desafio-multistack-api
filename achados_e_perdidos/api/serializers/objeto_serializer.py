from rest_framework import serializers
from ..models import Objeto
from django.contrib.auth.hashers import make_password
from ..hateoas import Hateoas
from django.urls import reverse


class ObjetoSerializer(serializers.ModelSerializer):

    data_cadastro = serializers.DateField(source="created_at", read_only=True)
    imagem = serializers.ImageField(source="imagem_objeto", read_only=True)
    entregue = serializers.BooleanField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Objeto
        fields = ('nome', 'descricao', 'entregue', 'id', 'imagem', 'data_cadastro', 'links')


    def get_links(self, obj):
        links = Hateoas()

        links.add_get('self', reverse('objeto-detail', kwargs={'objetoId': obj.id}))
        links.add_put('atualizar_objeto', reverse('objeto-detail', kwargs={'objetoId': obj.id}))
        links.add_delete('apagar_objeto', reverse('objeto-detail', kwargs={'objetoId': obj.id}))
        links.add_post('definir_imagem_objeto', reverse('imagem-objeto', kwargs={'objetoId': obj.id}))
        # links.add_patch('definir_dono_objeto', reverse())

        return links.to_array()