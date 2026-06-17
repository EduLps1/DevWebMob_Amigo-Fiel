from django.db.models import Count, Q
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from AmigoFiel.models import Pet, ProdutoEmpresa, UsuarioEmpresarial, UsuarioOng
from .serializers import (
    AmigoFielTokenObtainPairSerializer,
    MobileLojaSerializer,
    MobileOngSerializer,
    MobilePetSerializer,
    MobileProdutoSerializer,
    UserMeSerializer,
)


class AmigoFielTokenObtainPairView(TokenObtainPairView):
    serializer_class = AmigoFielTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserMeSerializer(request.user).data)


class MobileHomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        pets = Pet.objects.select_related("tutor", "ong").order_by("-criado_em")[:8]
        produtos = (
            ProdutoEmpresa.objects.select_related("empresa", "empresa__user")
            .filter(ativo=True)
            .order_by("-criado_em")[:8]
        )
        lojas = (
            UsuarioEmpresarial.objects.select_related("user")
            .annotate(qtd_produtos_ativos=Count("produtos", filter=Q(produtos__ativo=True)))
            .order_by("-qtd_produtos_ativos", "razao_social")[:8]
        )
        ongs = (
            UsuarioOng.objects.select_related("user")
            .annotate(qtd_pets=Count("pets"))
            .order_by("-qtd_pets", "nome_fantasia")[:8]
        )
        context = {"request": request}

        return Response(
            {
                "pets": MobilePetSerializer(pets, many=True, context=context).data,
                "produtos": MobileProdutoSerializer(produtos, many=True, context=context).data,
                "lojas": MobileLojaSerializer(lojas, many=True, context=context).data,
                "ongs": MobileOngSerializer(ongs, many=True, context=context).data,
            }
        )


class MobilePetsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q = (request.GET.get("q") or "").strip()
        pets = Pet.objects.select_related("tutor", "ong").order_by("-criado_em")
        if q:
            pets = pets.filter(Q(nome__icontains=q) | Q(raca__icontains=q) | Q(descricao__icontains=q))
        return Response(MobilePetSerializer(pets[:30], many=True, context={"request": request}).data)


class MobileProdutosView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q = (request.GET.get("q") or "").strip()
        produtos = (
            ProdutoEmpresa.objects.select_related("empresa", "empresa__user")
            .filter(ativo=True)
            .order_by("nome")
        )
        if q:
            produtos = produtos.filter(Q(nome__icontains=q) | Q(descricao__icontains=q))
        return Response(MobileProdutoSerializer(produtos[:30], many=True, context={"request": request}).data)


class MobileLojasView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q = (request.GET.get("q") or "").strip()
        lojas = (
            UsuarioEmpresarial.objects.select_related("user")
            .annotate(qtd_produtos_ativos=Count("produtos", filter=Q(produtos__ativo=True)))
            .order_by("-qtd_produtos_ativos", "razao_social")
        )
        if q:
            lojas = lojas.filter(Q(razao_social__icontains=q) | Q(user__username__icontains=q))
        return Response(MobileLojaSerializer(lojas[:30], many=True, context={"request": request}).data)


class MobileOngsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q = (request.GET.get("q") or "").strip()
        ongs = (
            UsuarioOng.objects.select_related("user")
            .annotate(qtd_pets=Count("pets"))
            .order_by("-qtd_pets", "nome_fantasia")
        )
        if q:
            ongs = ongs.filter(Q(nome_fantasia__icontains=q) | Q(user__username__icontains=q))
        return Response(MobileOngSerializer(ongs[:30], many=True, context={"request": request}).data)
