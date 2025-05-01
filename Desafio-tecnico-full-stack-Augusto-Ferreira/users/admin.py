from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Material, Procedimento, EtapaProcesso

# Registra o modelo User com uma interface personalizada no Django Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configurações personalizadas para o modelo User no painel administrativo.
    Herda de BaseUserAdmin para utilizar a interface padrão de usuário, mas com algumas customizações.
    """

    # Define os campos a serem exibidos nas seções do formulário de edição do usuário
    fieldsets = (
        (None, {"fields": ("username", "password")}),  # Campos principais de login
        (_("Informações pessoais"), {"fields": ("first_name", "last_name", "email")}),  # Campos pessoais
        (_("Permissões"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),  # Permissões de acesso
        (_("Datas importantes"), {"fields": ("last_login", "date_joined")}),  # Informações de login
        (_("Perfil"), {"fields": ("role",)}),  # Campo adicional 'role' para o perfil do usuário
    )

    # Define os campos que aparecem ao adicionar um novo usuário
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "role"),  # Campos para criação do usuário
        }),
    )

    # Configura os campos a serem exibidos na lista de usuários
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")

    # Configura filtros disponíveis na visualização de lista de usuários
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")

    # Campos pesquisáveis na lista de usuários
    search_fields = ("username", "first_name", "last_name", "email")

    # Ordenação dos registros na lista de usuários
    ordering = ("username",)


# Registra o modelo Material com uma interface personalizada no Django Admin
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """
    Configurações do modelo Material no painel administrativo.
    Define como o material será exibido e filtrado na interface de administração.
    """

    # Define os campos a serem exibidos na lista de materiais
    list_display = ("nome", "tipo", "data_validade", "serial")  # Campos a exibir

    # Campos pesquisáveis na lista de materiais
    search_fields = ("nome", "serial")  # Permite buscar pelo nome ou pelo serial do material


# Registra o modelo Procedimento com uma interface personalizada no Django Admin
@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    """
    Configurações do modelo Procedimento no painel administrativo.
    Define como o procedimento será exibido e filtrado na interface de administração.
    """

    # Define os campos a serem exibidos na lista de procedimentos
    list_display = ("id", "material", "data_inicio")

    # Campos pesquisáveis na lista de procedimentos
    search_fields = ("material__nome", "material__serial")  # Permite buscar pelo nome ou serial do material associado


# Registra o modelo EtapaProcesso com uma interface personalizada no Django Admin
@admin.register(EtapaProcesso)
class EtapaProcessoAdmin(admin.ModelAdmin):
    """
    Configurações do modelo EtapaProcesso no painel administrativo.
    Define como a etapa do processo será exibida e filtrada na interface de administração.
    """

    # Define os campos a serem exibidos na lista de etapas do processo
    list_display = ("id", "procedimento", "etapa", "data_realizacao")

    # Filtros disponíveis para a visualização da lista de etapas
    list_filter = ("etapa",)

    # Campos pesquisáveis na lista de etapas do processo
    search_fields = ("procedimento__material__nome", "procedimento__material__serial")  # Permite buscar pelo material associado
