from rest_framework import serializers
from ..models import Objeto


class InformarEntregaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Objeto
        fields = ('dono_nome', 'dono_cpf')