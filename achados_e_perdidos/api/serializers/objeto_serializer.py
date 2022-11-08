from rest_framework import serializers
from ..models import Objeto
from ..hateoas import Hateoas
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser


class ObjetoSerializer(serializers.ModelSerializer):

    data_cadastro = serializers.DateField(source="created_at", read_only=True)
    imagem = serializers.ImageField(source="imagem_objeto", read_only=True)
    entregue = serializers.BooleanField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Objeto
        fields = ('nome', 'descricao', 'entregue', 'id', 'imagem', 'data_cadastro', 'links')


    def get_links(self, obj):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return None

        links = Hateoas()
        links.add_get('self', reverse('objeto-detail', kwargs={'objetoId': obj.id}))
        links.add_put('atualizar_objeto', reverse('objeto-detail', kwargs={'objetoId': obj.id}))
        links.add_delete('apagar_objeto', reverse('objeto-detail', kwargs={'objetoId': obj.id}))
        links.add_post('definir_imagem_objeto', reverse('imagem-objeto', kwargs={'objetoId': obj.id}))

        if not obj.entregue:
            links.add_post('definir_dono_objeto',  reverse('dono-objeto-list', kwargs={'objetoId': obj.id}))

        return links.to_array()