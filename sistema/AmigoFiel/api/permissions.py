from rest_framework.permissions import BasePermission

from .roles import (
    ROLE_ADMINISTRADOR,
    ROLE_ADOTANTE,
    ROLE_EMPRESA,
    ROLE_ONG,
    get_user_role,
)


class HasRole(BasePermission):
    required_roles = ()

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and get_user_role(request.user) in self.required_roles
        )


class IsAdministrador(HasRole):
    required_roles = (ROLE_ADMINISTRADOR,)


class IsAdotante(HasRole):
    required_roles = (ROLE_ADOTANTE,)


class IsEmpresa(HasRole):
    required_roles = (ROLE_EMPRESA,)


class IsOng(HasRole):
    required_roles = (ROLE_ONG,)


class IsEmpresaOrAdministrador(HasRole):
    required_roles = (ROLE_EMPRESA, ROLE_ADMINISTRADOR)


class IsOngOrAdministrador(HasRole):
    required_roles = (ROLE_ONG, ROLE_ADMINISTRADOR)


class IsAdotanteOrAdministrador(HasRole):
    required_roles = (ROLE_ADOTANTE, ROLE_ADMINISTRADOR)
