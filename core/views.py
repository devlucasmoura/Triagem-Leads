from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .classificacao import classificar
from .models import Lead
from .serializers import LeadEntradaSerializer, LeadSerializer


class ClassificarLead(APIView):
    """Recebe o lead do n8n, classifica, grava e devolve o resultado."""

    def post(self, request):
        entrada = LeadEntradaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        dados = entrada.validated_data

        resultado = classificar(dados["mensagem"], dados["origem"])

        lead = Lead.objects.create(
            nome=dados["nome"],
            email=dados["email"],
            mensagem=dados["mensagem"],
            origem=dados["origem"],
            categoria=resultado["categoria"],
            urgencia=resultado["urgencia"],
            score=resultado["score"],
        )

        return Response(
            LeadSerializer(lead).data, status=status.HTTP_201_CREATED
        )


class LeadList(generics.ListAPIView):
    """Listagem para conferencia, ordenada por score."""

    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
