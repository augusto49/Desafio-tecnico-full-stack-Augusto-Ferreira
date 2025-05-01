from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'administrativo'

class IsTecnicoRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'tecnico'

class IsEnfermagemRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'enfermagem'
    