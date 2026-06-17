# Amigo Fiel

Plataforma web e mobile para adocao responsavel, perfis de ONGs, perfis de lojas parceiras e marketplace pet.

## Dono e mantenedor

Este projeto e mantido por:

- [Eduardo Lopes / EduLps1](https://github.com/EduLps1)

Repositorio oficial:

- [EduLps1/DevWebMob_Amigo-Fiel](https://github.com/EduLps1/DevWebMob_Amigo-Fiel)

## Stack

| Camada | Tecnologia | Funcao |
| --- | --- | --- |
| Linguagens | Python, TypeScript, HTML5/CSS3, JavaScript | Backend, mobile e templates |
| Banco de dados | PostgreSQL | Persistencia local |
| Backend | Django 5.2.6 | Regras de negocio, ORM e Admin |
| Frontend web | Django Templates | Interface web classica |
| API | Django REST Framework | Dados JSON para o mobile |
| Auth API | SimpleJWT | Access token e refresh token |
| CORS | django-cors-headers | Integracao Ionic 8100 -> Django 8000 |
| Frontend mobile | Ionic + Angular | App mobile web |
| Nativo futuro | Capacitor | Preparacao para build mobile |

## Estrutura

```text
.
|-- mobile/                  # Ionic + Angular
|-- scripts/                 # Scripts locais de inicializacao
|-- sistema/                 # Projeto Django
|   |-- AmigoFiel/           # App principal
|   |   |-- api/             # API REST/JWT/mobile
|   |   |-- management/      # Comandos utilitarios locais
|   |   |-- models.py
|   |   |-- views.py
|   |   `-- urls.py
|   |-- chat/
|   |-- templates/
|   `-- manage.py
|-- requirements.txt
`-- .env.example
```

## Funcionalidades atuais

- Cadastro web de usuarios por tipo:
  - adotante
  - empresa
  - ONG
- Login web com sessao/cookies.
- Login API/mobile com JWT.
- Endpoint de refresh token.
- Endpoint `/api/auth/me/` para identificar usuario logado no app.
- Permissoes por role na API:
  - `administrador`
  - `adotante`
  - `empresa`
  - `ong`
- Home web com destaques.
- Home mobile baseada no mesmo conceito visual do web.
- Particoes mobile espelhando o web:
  - `/`
  - `/login`
  - `/cadastro`
  - `/adotar`
  - `/produtos`
  - `/lojas`
  - `/ongs`
- Endpoints publicos mobile:
  - `/api/mobile/home/`
  - `/api/mobile/pets/`
  - `/api/mobile/produtos/`
  - `/api/mobile/lojas/`
  - `/api/mobile/ongs/`

## Configuracao local

Crie o arquivo `.env` a partir do exemplo:

```powershell
Copy-Item .env.example .env
notepad .env
```

Configure principalmente:

```text
POSTGRES_DB=amigofiel
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_SSLMODE=disable
```

O arquivo `.env` nao deve ser versionado.

## Instalar dependencias

Backend:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Mobile:

```powershell
cd mobile
npm.cmd install
```

## Banco de dados

Crie o banco PostgreSQL local:

```sql
CREATE DATABASE amigofiel;
```

Rode as migrations:

```powershell
cd sistema
..\.venv\Scripts\python.exe manage.py migrate
```

Criar ou resetar admin local e limpar dados populados:

```powershell
..\.venv\Scripts\python.exe manage.py reset_local_data --admin-username eduadmin --admin-email seuemail@email.com --confirm-delete
```

## Rodar o projeto

### Django web + API

Na raiz do projeto:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-django-dev.ps1
```

URLs:

- Web local: http://127.0.0.1:8000/
- Web na rede: http://10.90.8.79:8000/
- API: http://127.0.0.1:8000/api/

### Ionic mobile

Em outro PowerShell, na raiz do projeto:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\start-mobile-dev.ps1
```

URLs:

- Mobile local: http://localhost:8100/
- Mobile no celular: http://10.90.8.79:8100/

Observacao: `0.0.0.0` aparece no terminal apenas como endereco de escuta do servidor. Para acessar pelo navegador, use `127.0.0.1`, `localhost` ou o IP da maquina.

## Testes e validacao

Backend:

```powershell
cd sistema
..\.venv\Scripts\python.exe manage.py check
..\.venv\Scripts\python.exe manage.py test
```

Mobile:

```powershell
cd mobile
node_modules\.bin\tsc.cmd -p tsconfig.app.json --noEmit
```

## Seguranca

Medidas ja aplicadas:

- Remocao de segredos hardcoded do `settings.py`.
- Configuracao via `.env`.
- Cookies web com `HttpOnly` e `SameSite=Lax`.
- Protecao CSRF no login web.
- Logout web apenas por POST.
- API isolada com JWT.
- Roles centralizadas para permissoes API.

Pontos futuros:

- Endpoint de cadastro API para o Ionic.
- Testes unitarios completos para JWT, refresh, roles e coexistencia web/API.
- Auditoria de dependencias npm antes de build final.
- Hardening para ambiente de producao.

## Licenca

Veja [LICENSE](LICENSE).
