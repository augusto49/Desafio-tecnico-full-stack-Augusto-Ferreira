from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Material, Procedimento, EtapaProcesso


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Informações pessoais"), {"fields": ("first_name", "last_name", "email")}),
        (_("Permissões"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Datas importantes"), {"fields": ("last_login", "date_joined")}),
        (_("Perfil"), {"fields": ("role",)}),  # <-- campo personalizado
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "role"),
        }),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "data_validade", "serial")
    search_fields = ("nome", "serial")


@admin.register(Procedimento)
class ProcedimentoAdmin(admin.ModelAdmin):
    list_display = ("id", "material", "data_inicio")
    search_fields = ("material__nome", "material__serial")


@admin.register(EtapaProcesso)
class EtapaProcessoAdmin(admin.ModelAdmin):
    list_display = ("id", "procedimento", "etapa", "data_realizacao")
    list_filter = ("etapa",)
    search_fields = ("procedimento__material__nome", "procedimento__material__serial")
