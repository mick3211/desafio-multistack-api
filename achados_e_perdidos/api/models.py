import os
from django.db import models
from django.core.validators import validate_image_file_extension
from django.contrib.auth.models import AbstractUser
import uuid


def get_image_name(filename, id=uuid.uuid4()):
    ext = filename.split('.')[-1]
    filename = f'{id}.{ext}'
    return filename

def get_local_image_name(instance, filename):
    return os.path.join('img', 'locais', get_image_name(filename, instance.user.id))

def get_objeto_image_name(instance, filename):
    return os.path.join('img', 'objetos', get_image_name(filename, instance.id))


# Create your models here.
class User(AbstractUser):
    username=None
    nome = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(blank=False, null=False, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome',]


class Local(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False)
    endereco = models.CharField(max_length=255, blank=False, null=False)
    contato = models.CharField(max_length=255, blank=False, null=False)
    descricao = models.CharField(max_length=255, blank=False, null=True)
    imagem_local = models.ImageField(null=True, upload_to=get_local_image_name, validators=[validate_image_file_extension,])
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, null=False, blank=False)


class Objeto(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False)
    descricao = models.CharField(max_length=255, blank=False, null=False)
    entregue = models.BooleanField(default=False, null=False, blank=False)
    imagem_objeto = models.ImageField(null=True, upload_to=get_objeto_image_name, validators=[validate_image_file_extension,])
    local = models.ForeignKey(to=Local, on_delete=models.CASCADE, null=False, blank=False)
    dono_nome = models.CharField(max_length=255, blank=False, null=True)
    dono_cpf = models.CharField(max_length=11, blank=False, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    