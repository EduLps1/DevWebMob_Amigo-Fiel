from getpass import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from AmigoFiel.models import (
    Carrinho,
    Favorito,
    ItemCarrinho,
    ItemPedido,
    ParceriaOngEmpresa,
    Pedido,
    Pet,
    ProdutoEmpresa,
    ProdutoOngVinculo,
    UsuarioComum,
    UsuarioEmpresarial,
    UsuarioOng,
)


class Command(BaseCommand):
    help = (
        "Cria/atualiza uma conta administradora exclusiva e limpa os dados locais "
        "de usuarios, perfis, itens e interacoes."
    )

    def add_arguments(self, parser):
        parser.add_argument("--admin-username", required=True)
        parser.add_argument("--admin-email", default="")
        parser.add_argument("--admin-password", default="")
        parser.add_argument(
            "--confirm-delete",
            action="store_true",
            help="Obrigatorio para apagar os dados locais existentes.",
        )

    def handle(self, *args, **options):
        if not options["confirm_delete"]:
            raise CommandError(
                "Operacao bloqueada. Rode novamente com --confirm-delete para confirmar a limpeza."
            )

        username = options["admin_username"].strip()
        email = options["admin_email"].strip()
        password = options["admin_password"]

        if not username:
            raise CommandError("--admin-username nao pode ficar vazio.")

        if not password:
            password = getpass("Senha do admin: ")
            password_confirmation = getpass("Confirme a senha do admin: ")
            if password != password_confirmation:
                raise CommandError("As senhas informadas nao conferem.")

        if not password:
            raise CommandError("A senha do admin nao pode ficar vazia.")

        User = get_user_model()

        with transaction.atomic():
            admin_user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email},
            )
            admin_user.email = email or admin_user.email
            admin_user.is_active = True
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password(password)
            admin_user.save()

            deleted = self._delete_project_data(admin_user)

        action = "criada" if created else "atualizada"
        self.stdout.write(self.style.SUCCESS(f"Conta admin '{username}' {action} com sucesso."))
        self.stdout.write(self.style.SUCCESS("Limpeza local concluida."))
        for label, count in deleted:
            self.stdout.write(f"- {label}: {count}")

    def _delete_project_data(self, admin_user):
        User = get_user_model()
        deletion_order = [
            ("mensagens do chat", self._optional_model("chat", "Message")),
            ("conversas do chat", self._optional_model("chat", "Conversation")),
            ("favoritos", Favorito),
            ("itens de pedido", ItemPedido),
            ("pedidos", Pedido),
            ("itens de carrinho", ItemCarrinho),
            ("carrinhos", Carrinho),
            ("vinculos produto/ong", ProdutoOngVinculo),
            ("parcerias empresa/ong", ParceriaOngEmpresa),
            ("produtos", ProdutoEmpresa),
            ("pets", Pet),
            ("perfis comuns", UsuarioComum),
            ("perfis empresariais", UsuarioEmpresarial),
            ("perfis de ong", UsuarioOng),
        ]

        deleted = []
        for label, model in deletion_order:
            if model is None:
                deleted.append((label, 0))
                continue
            count = model.objects.count()
            model.objects.all().delete()
            deleted.append((label, count))

        old_users = User.objects.exclude(pk=admin_user.pk)
        old_user_count = old_users.count()
        old_users.delete()
        deleted.append(("usuarios antigos", old_user_count))
        return deleted

    def _optional_model(self, app_label, model_name):
        try:
            from django.apps import apps

            return apps.get_model(app_label, model_name)
        except LookupError:
            return None
