from rest_framework import serializers
from ..models import Local, User
from django.contrib.auth.hashers import make_password
from ..hateoas import Hateoas
from django.urls import reverse


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)
    nome = serializers.CharField(max_length=255, min_length=3, required=True)

    class Meta:
        model = User
        fields = ('email', 'nome', 'password', 'password_confirmation')

    
    def validate(self, data):
        password_confirmation = data['password_confirmation']
        password = data['password']
        if password_confirmation != password:
            raise serializers.ValidationError('As senhas devem ser iguais')
        return data


class LocalSerializer(serializers.ModelSerializer):

    usuario = UserSerializer(source='user')
    nome = serializers.CharField(max_length=255, min_length=3, required=True)
    endereco = serializers.CharField(max_length=255, min_length=3, required=True)
    contato = serializers.CharField(max_length=255, min_length=3, required=True)
    imagem = serializers.SerializerMethodField(read_only=True)
    links = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Local
        exclude = ('imagem_local', 'user')


    def get_imagem(self, data):
        return str(data.imagem_local) or None

    def get_links(self, data):
        links = Hateoas()
        links.add_get('self', reverse('locais-list'))
        links.add_put('atualizar_local', reverse('locais-list'))
        links.add_delete('apagar_local', reverse('locais-list'))
        links.add_post('definir_imagem_local', reverse('imagem-local'))
        links.add_get('listar_objetos_local', reverse('objetos-list'))
        links.add_post('adicionar_objeto_local', reverse('objetos-list'))
        return links.to_array()

    def create(self, validated_data):
        user = validated_data.pop('user')
        user['password'] = make_password(user['password'])
        user.pop('password_confirmation')
        user = User.objects.create(**user)
        local = Local.objects.create(user=user, **validated_data)
        return local