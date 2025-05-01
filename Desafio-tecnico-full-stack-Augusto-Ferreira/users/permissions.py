from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """
    Permissão personalizada que verifica se o usuário possui o papel de 'administrativo'.
    O usuário deve estar autenticado e ter o papel 'administrativo' para acessar a vista.

    Método:
        has_permission: Verifica se o usuário está autenticado e se o seu papel é 'administrativo'.
    """
    def has_permission(self, request, view):
        """
        Verifica se o usuário tem permissão para acessar a vista.
        
        A permissão é concedida apenas se o usuário estiver autenticado e 
        tiver o papel de 'administrativo'.
        """
        return request.user.is_authenticated and request.user.role == 'administrativo'


class IsTecnicoRole(BasePermission):
    """
    Permissão personalizada que verifica se o usuário possui o papel de 'tecnico'.
    O usuário deve estar autenticado e ter o papel 'tecnico' para acessar a vista.

    Método:
        has_permission: Verifica se o usuário está autenticado e se o seu papel é 'tecnico'.
    """
    def has_permission(self, request, view):
        """
        Verifica se o usuário tem permissão para acessar a vista.
        
        A permissão é concedida apenas se o usuário estiver autenticado e 
        tiver o papel de 'tecnico'.
        """
        return request.user.is_authenticated and request.user.role == 'tecnico'


class IsEnfermagemRole(BasePermission):
    """
    Permissão personalizada que verifica se o usuário possui o papel de 'enfermagem'.
    O usuário deve estar autenticado e ter o papel 'enfermagem' para acessar a vista.

    Método:
        has_permission: Verifica se o usuário está autenticado e se o seu papel é 'enfermagem'.
    """
    def has_permission(self, request, view):
        """
        Verifica se o usuário tem permissão para acessar a vista.
        
        A permissão é concedida apenas se o usuário estiver autenticado e 
        tiver o papel de 'enfermagem'.
        """
        return request.user.is_authenticated and request.user.role == 'enfermagem'
