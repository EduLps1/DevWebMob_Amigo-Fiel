# Amigo Fiel Mobile

App Ionic + Angular para consumir a API Django via JWT.

## Configuracao local

Instale as dependencias:

```powershell
npm.cmd install
```

Edite `src/environments/environment.ts` e ajuste `apiBaseUrl`:

```ts
export const environment = {
  production: false,
  apiBaseUrl: 'http://SEU_IP_DA_VM:8000/api'
};
```

No Django, rode o servidor exposto na rede:

```powershell
python manage.py runserver 0.0.0.0:8000
```

No app Ionic, rode:

```powershell
npm.cmd start
```

O Ionic sobe na porta `8100`. O celular deve acessar:

```text
http://SEU_IP_DA_VM:8100
```

## Autenticacao

Arquivos principais:

- `src/app/core/auth/auth.service.ts`: login, logout, refresh e persistencia com Capacitor Preferences.
- `src/app/core/auth/auth.interceptor.ts`: anexa `Authorization: Bearer <token>` e tenta refresh automatico em respostas `401`.

Rotas Django usadas:

- `POST /api/auth/token/`
- `POST /api/auth/refresh/`
- `GET /api/auth/me/`
