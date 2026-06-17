ROLE_ADMINISTRADOR = "administrador"
ROLE_ADOTANTE = "adotante"
ROLE_EMPRESA = "empresa"
ROLE_ONG = "ong"


def get_user_role(user):
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser or user.is_staff:
        return ROLE_ADMINISTRADOR
    if hasattr(user, "perfil_empresa"):
        return ROLE_EMPRESA
    if hasattr(user, "perfil_ong"):
        return ROLE_ONG
    if hasattr(user, "perfil_comum"):
        return ROLE_ADOTANTE
    return None


def get_user_profile_id(user):
    if not user or not user.is_authenticated:
        return None
    for attr in ("perfil_empresa", "perfil_ong", "perfil_comum"):
        if hasattr(user, attr):
            return getattr(user, attr).pk
    return None
