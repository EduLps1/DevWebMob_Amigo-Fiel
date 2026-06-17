# AmigoFiel/migrations/0015_seed_produtos_empr3000.py
from django.db import migrations
from django.contrib.auth.hashers import make_password
from decimal import Decimal

def seed_produtos_empr3000_forward(apps, schema_editor):
    from django.utils.text import slugify
    User = apps.get_model("auth", "User")
    UsuarioEmpresarial = apps.get_model("AmigoFiel", "UsuarioEmpresarial")
    ProdutoEmpresa = apps.get_model("AmigoFiel", "ProdutoEmpresa")

    def unique_slug_prod(empresa, base):
        slug = base[:120]
        i = 1
        while ProdutoEmpresa.objects.filter(empresa=empresa, slug=slug).exists():
            suf = f"-{i}"
            slug = f"{base[:120-len(suf)]}{suf}"
            i += 1
        return slug

    # Criar ou buscar empresa Empr3000
    user_empr3000, user_created = User.objects.get_or_create(
        username="empr3000",
        defaults={
            "email": "contato@empr3000.com.br",
            "is_active": True,
        },
    )
    if user_created:
        user_empr3000.password = make_password("empr3000")
        user_empr3000.save(update_fields=["password"])
        print("Usuario 'empr3000' criado com sucesso")
    else:
        print("Usuario 'empr3000' ja existe")

    empresa, empresa_created = UsuarioEmpresarial.objects.get_or_create(
        user=user_empr3000,
        defaults={
            "razao_social": "Empr3000 Pet Shop Ltda",
            "cnpj": "30.000.000/0001-00",
            "telefone": "(63) 3000-3000",
            "slogan": "Loja especializada em produtos pet premium",
            "cidade": "Palmas",
        },
    )
    if empresa_created:
        print("Empresa 'Empr3000' criada com sucesso")
    else:
        print("Empresa 'Empr3000' ja existe")

    # Lista de produtos para criar
    produtos_data = [
        {
            "nome": "Ração Premium Filhote 15kg",
            "categoria": "racoes",
            "descricao": "Ração super premium para filhotes de todas as raças. Rica em proteínas, vitaminas e minerais essenciais para o desenvolvimento saudável. Fórmula balanceada com DHA para desenvolvimento cerebral.",
            "descricao_curta": "Nutrição completa para filhotes em crescimento",
            "preco": Decimal("189.90"),
            "desconto_percentual": Decimal("15.00"),
            "estoque": 45,
        },
        {
            "nome": "Brinquedo Interativo Kong Classic",
            "categoria": "brinquedos",
            "descricao": "Brinquedo interativo resistente feito de borracha natural. Ideal para cães que adoram mastigar e brincar. Pode ser recheado com petiscos para maior diversão. Disponível em vários tamanhos.",
            "descricao_curta": "Diversão garantida e resistência extrema",
            "preco": Decimal("45.90"),
            "desconto_percentual": Decimal("0.00"),
            "estoque": 78,
        },
        {
            "nome": "Shampoo Hipoalergênico 500ml",
            "categoria": "higiene",
            "descricao": "Shampoo especialmente desenvolvido para pets com pele sensível. Fórmula hipoalergênica sem parabenos, livre de corantes artificiais. pH balanceado, deixa o pelo macio e brilhante.",
            "descricao_curta": "Cuidado suave para pele sensível",
            "preco": Decimal("38.90"),
            "desconto_percentual": Decimal("10.00"),
            "estoque": 62,
        },
        {
            "nome": "Cama Ortopédica Grande - 90x70cm",
            "categoria": "camas",
            "descricao": "Cama ortopédica de espuma viscoelástica de alta densidade. Proporciona conforto superior e suporte para articulações. Capa removível e lavável. Ideal para cães idosos ou com problemas articulares.",
            "descricao_curta": "Conforto terapêutico para seu pet",
            "preco": Decimal("259.90"),
            "desconto_percentual": Decimal("20.00"),
            "estoque": 12,
        },
        {
            "nome": "Kit Petiscos Naturais 500g",
            "categoria": "petiscos",
            "descricao": "Mix de petiscos naturais desidratados: tiras de frango, chips de batata-doce e cubos de fígado bovino. Sem conservantes ou corantes artificiais. 100% natural, rico em proteínas.",
            "descricao_curta": "Snacks saudáveis e irresistíveis",
            "preco": Decimal("42.90"),
            "desconto_percentual": Decimal("5.00"),
            "estoque": 95,
        },
        {
            "nome": "Coleira GPS com Rastreador",
            "categoria": "acessorios",
            "descricao": "Coleira inteligente com GPS integrado e conectividade 4G. Rastreamento em tempo real pelo app. Bateria com duração de até 7 dias. À prova d'água (IP67). Histórico de localização e cerca virtual.",
            "descricao_curta": "Tecnologia para nunca perder seu pet",
            "preco": Decimal("349.90"),
            "desconto_percentual": Decimal("25.00"),
            "estoque": 23,
        },
    ]

    # Criar os produtos
    produtos_criados = 0
    produtos_existentes = 0

    for prod_data in produtos_data:
        base_slug = slugify(prod_data["nome"])
        slug = unique_slug_prod(empresa, base_slug)
        
        produto, created = ProdutoEmpresa.objects.get_or_create(
            empresa=empresa,
            slug=slug,
            defaults={
                "nome": prod_data["nome"],
                "categoria": prod_data["categoria"],
                "descricao": prod_data["descricao"],
                "descricao_curta": prod_data["descricao_curta"],
                "preco": prod_data["preco"],
                "desconto_percentual": prod_data["desconto_percentual"],
                "estoque": prod_data["estoque"],
            },
        )
        
        if created:
            produtos_criados += 1
            desconto_str = f" ({prod_data['desconto_percentual']}% OFF)" if prod_data['desconto_percentual'] > 0 else ""
            print(f"Produto criado: {prod_data['nome']} - R$ {prod_data['preco']}{desconto_str}")
        else:
            produtos_existentes += 1
            print(f"Produto ja existe: {prod_data['nome']}")

    print(f"\n{'='*60}")
    print("RESUMO DA OPERACAO")
    print(f"{'='*60}")
    print(f"Produtos criados: {produtos_criados}")
    print(f"Produtos ja existentes: {produtos_existentes}")
    print(f"Total de produtos Empr3000: {ProdutoEmpresa.objects.filter(empresa=empresa).count()}")
    print(f"{'='*60}\n")


def seed_produtos_empr3000_backward(apps, schema_editor):
    """
    Reverter a migration (opcional - pode deixar os dados ou remover)
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('AmigoFiel', '0014_produtoempresa_desconto_percentual_and_more'),
    ]

    operations = [
        migrations.RunPython(
            seed_produtos_empr3000_forward,
            seed_produtos_empr3000_backward,
        ),
    ]
