from django.urls import path
from .views import EtapaProcessoCreateView, EtapasPorMaterialView, ExportRelatorioView, FalhaCreateView, RastreabilidadeView, UserCreateView, UserListView, UserMeView, UserRoleUpdateView

urlpatterns = [
    # Registro de usuário
    path('register/', UserCreateView.as_view(), name='register'),

    # Visualizar o usuário logado
    path('me/', UserMeView.as_view(), name='user-me'),
    
    # Listagem de todos os usuários
    path('list/', UserListView.as_view(), name='user-list'),

    # Atualizar papel do usuário
    path('update-role/<int:pk>/', UserRoleUpdateView.as_view(), name='update-role'),
    
    # Criar etapa de processo
    path('etapas/', EtapaProcessoCreateView.as_view(), name='etapa-create'),
    
    # Visualizar etapas de um material específico
    path('etapas/<str:serial>/', EtapasPorMaterialView.as_view(), name='etapas-por-material'),

    # Rastreabilidade do processo de esterilização
    path('rastreabilidade/', RastreabilidadeView.as_view(), name='rastreabilidade'),
    
    # Exportação de relatório de processos
    path('relatorio/', ExportRelatorioView.as_view(), name='relatorio-export'),
    
    # Criar falha no processo de esterilização
    path('falhas/', FalhaCreateView.as_view(), name='falha-create'),
]
