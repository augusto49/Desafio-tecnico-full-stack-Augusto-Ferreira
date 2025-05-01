import io
from django.http import HttpResponse
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from .models import EtapaProcesso, Falha, Material, User
from .serializers import EtapaProcessoSerializer, FalhaSerializer, MaterialSerializer, UserSerializer, UserRoleUpdateSerializer
from .permissions import IsAdminRole, IsEnfermagemRole, IsTecnicoRole
from rest_framework.views import APIView
import pandas as pd
from reportlab.pdfgen import canvas

from users import models

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

# ✅ Listar todos os usuários (somente administrativo)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]

# ✅ Atualizar role do usuário (somente administrativo)
class UserRoleUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRoleUpdateSerializer  
    permission_classes = [permissions.IsAuthenticated, IsAdminRole]
    lookup_field = 'pk'

class MaterialCreateView(generics.CreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, IsTecnicoRole]

class MaterialListView(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]


class EtapaProcessoCreateView(generics.CreateAPIView):
    serializer_class = EtapaProcessoSerializer
    permission_classes = [IsAuthenticated, IsTecnicoRole]

    def perform_create(self, serializer):
        # A criação já se encarrega de definir o status corretamente
        serializer.save()

class EtapasPorMaterialView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, serial):
        try:
            material = Material.objects.get(serial=serial)
        except Material.DoesNotExist:
            return Response({'error': 'Material não encontrado'}, status=404)

        procedimentos = material.procedimentos.prefetch_related('etapas')
        data = []

        for procedimento in procedimentos:
            etapas = procedimento.etapas.all()
            data.append({
                'procedimento_id': procedimento.id,
                'data_inicio': procedimento.data_inicio,
                'etapas': [
                    {
                        'id': etapa.id,
                        'etapa': etapa.etapa,
                        'status': etapa.status,  # Status da etapa
                        'data_realizacao': etapa.data_realizacao
                    }
                    for etapa in etapas
                ]
            })

        return Response(data)


class FalhaCreateView(generics.CreateAPIView):
    queryset = Falha.objects.all()
    serializer_class = FalhaSerializer
    permission_classes = [IsAuthenticated, IsTecnicoRole]

class RastreabilidadeView(APIView):
    permission_classes = [IsAuthenticated, IsEnfermagemRole]

    def get(self, request):
        serial = request.query_params.get('serial', None)
        materiais = Material.objects.all()

        if serial:
            materiais = materiais.filter(serial=serial)

        resultado = []
        for material in materiais:
            procedimentos = material.procedimentos.all()
            total_procedimentos = procedimentos.count()
            falhas = Falha.objects.filter(etapa__procedimento__material=material)
            resultado.append({
                'serial': material.serial,
                'nome': material.nome,
                'total_processos': total_procedimentos,
                'total_falhas': falhas.count(),
                'falhas': [{'etapa': f.etapa.etapa, 'descricao': f.descricao, 'data': f.data_ocorrencia} for f in falhas],
            })
        return Response(resultado)
    
class ExportRelatorioView(APIView):
    permission_classes = [IsAuthenticated, IsEnfermagemRole]

    def get(self, request):
        formato = request.query_params.get('formato', 'pdf')  # pdf ou xlsx
        materiais = Material.objects.all()
        data = []

        for material in materiais:
            procedimentos_concluidos = material.procedimentos.filter(etapas__count=4).distinct()
            if procedimentos_concluidos.exists():
                falhas = Falha.objects.filter(etapa__procedimento__material=material)
                data.append({
                    'serial': material.serial,
                    'nome': material.nome,
                    'quantidade_falhas': falhas.count()
                })

        if formato == 'xlsx':
            df = pd.DataFrame(data)
            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            response = HttpResponse(output, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="relatorio.xlsx"'
            return response

        elif formato == 'pdf':
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer)
            y = 800
            for item in data:
                p.drawString(100, y, f"{item['serial']} - {item['nome']} - Falhas: {item['quantidade_falhas']}")
                y -= 20
            p.save()
            buffer.seek(0)
            return HttpResponse(buffer, content_type='application/pdf')

        return Response({"erro": "Formato inválido. Use 'pdf' ou 'xlsx'"}, status=400)