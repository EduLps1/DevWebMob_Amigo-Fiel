from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from AmigoFiel.models import Pet, ProdutoEmpresa, UsuarioEmpresarial, UsuarioOng
from .roles import get_user_profile_id, get_user_role


class UserMeSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    profile_id = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "role",
            "profile_id",
        )
        read_only_fields = fields

    def get_role(self, obj):
        return get_user_role(obj)

    def get_profile_id(self, obj):
        return get_user_profile_id(obj)


class AmigoFielTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["email"] = user.email
        token["role"] = get_user_role(user)
        token["profile_id"] = get_user_profile_id(user)
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserMeSerializer(self.user).data
        return data


class MobilePetSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    detail_path = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = ("id", "nome", "especie", "raca", "cidade", "image_url", "detail_path")

    cidade = serializers.SerializerMethodField()

    def get_cidade(self, obj):
        if obj.tutor:
            return obj.tutor.cidade
        if obj.ong:
            return obj.ong.cidade
        return ""

    def get_image_url(self, obj):
        return build_media_url(self.context.get("request"), obj.imagem)

    def get_detail_path(self, obj):
        return f"/pet/{obj.slug}/"


class MobileProdutoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    empresa_nome = serializers.CharField(source="empresa.razao_social")
    detail_path = serializers.SerializerMethodField()

    class Meta:
        model = ProdutoEmpresa
        fields = ("id", "nome", "empresa_nome", "preco", "image_url", "detail_path")

    def get_image_url(self, obj):
        return build_media_url(self.context.get("request"), obj.imagem)

    def get_detail_path(self, obj):
        return f"/{obj.empresa.user.username}/{obj.slug}/"


class MobileLojaSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    detail_path = serializers.SerializerMethodField()

    class Meta:
        model = UsuarioEmpresarial
        fields = ("id", "razao_social", "cidade", "image_url", "detail_path")

    def get_image_url(self, obj):
        return build_media_url(self.context.get("request"), obj.foto)

    def get_detail_path(self, obj):
        return f"/Co./{obj.user.username}/"


class MobileOngSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    detail_path = serializers.SerializerMethodField()

    class Meta:
        model = UsuarioOng
        fields = ("id", "nome_fantasia", "cidade", "image_url", "detail_path")

    def get_image_url(self, obj):
        return build_media_url(self.context.get("request"), obj.foto)

    def get_detail_path(self, obj):
        return f"/ONG/{obj.user.username}/"


def build_media_url(request, image_field):
    if not image_field:
        return None

    try:
        url = image_field.url
    except ValueError:
        return None

    if request:
        return request.build_absolute_uri(url)
    return url
