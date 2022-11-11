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
    imagem = serializers.ImageField(read_only=True, source='imagem_local')
    links = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Local
        exclude = ('imagem_local', 'user')


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


class EditarUsuarioSerializer(UserSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=False)
    password_confirmation = serializers.CharField(write_only=True, required=False)

    def validate_email(self, email):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=email).exists():
            raise serializers.ValidationError("usuário com este email já existe.")
        return email

    def validate(self, data):
        password = data.get('password', None)
        password_confirmation = data.get('password_confirmation', None)

        if password is not None and password_confirmation != password:
            raise serializers.ValidationError('As senhas devem ser iguais')
        return data


class EditarLocalSerializer(LocalSerializer):

    usuario = EditarUsuarioSerializer(source='user')

    
    def update(self, instance, validated_data):
        user = User.objects.get(pk=instance.user.pk)
        user_data = validated_data.pop('user')
        password = user_data.get('password')
        
        if password is not None:
            user.set_password(password)
        
        user.email = user_data['email']
        user.nome = user_data['nome']
        user.save()

        instance.nome = validated_data['nome']
        instance.endereco = validated_data['endereco']
        instance.contato = validated_data['contato']
        instance.descricao = validated_data.get('descricao')
        instance.save()

        return instance