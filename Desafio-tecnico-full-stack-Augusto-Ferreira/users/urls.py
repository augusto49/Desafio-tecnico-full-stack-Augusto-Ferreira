from django.urls import path
from .views import EtapaProcessoCreateView, EtapasPorMaterialView, ExportRelatorioView, FalhaCreateView, RastreabilidadeView, UserCreateView, UserListView, UserMeView, UserRoleUpdateView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('me/', UserMeView.as_view(), name='user-me'),
    
    path('list/', UserListView.as_view(), name='user-list'),
    path('update-role/<int:pk>/', UserRoleUpdateView.as_view(), name='update-role'),
    
    path('etapas/', EtapaProcessoCreateView.as_view(), name='etapa-create'),
    path('etapas/<str:serial>/', EtapasPorMaterialView.as_view(), name='etapas-por-material'),

    path('rastreabilidade/', RastreabilidadeView.as_view(), name='rastreabilidade'),
    path('relatorio/', ExportRelatorioView.as_view(), name='relatorio-export'),
    path('falhas/', FalhaCreateView.as_view(), name='falha-create'),
]
