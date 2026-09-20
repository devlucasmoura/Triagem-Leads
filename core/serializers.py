from rest_framework import serializers

from .models import Lead


class LeadEntradaSerializer(serializers.Serializer):
    """O que o n8n envia."""

    nome = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    mensagem = serializers.CharField()
    origem = serializers.CharField(max_length=40, default="site")


class LeadSerializer(serializers.ModelSerializer):
    """O que a API devolve e lista."""

    class Meta:
        model = Lead
        fields = [
            "id",
            "nome",
            "email",
            "mensagem",
            "origem",
            "categoria",
            "urgencia",
            "score",
            "recebido_em",
        ]
