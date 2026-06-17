import { HttpErrorResponse, HttpHandlerFn, HttpInterceptorFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { from, switchMap, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { environment } from '../../../environments/environment';
import { AuthService } from './auth.service';

const AUTH_ENDPOINTS = ['/auth/token/', '/auth/refresh/'];

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const authService = inject(AuthService);

  if (shouldSkipAuth(request)) {
    return next(request);
  }

  return from(authService.getAccessToken()).pipe(
    switchMap((token) => next(withBearerToken(request, token))),
    catchError((error) => handleAuthError(error, request, next, authService))
  );
};

function handleAuthError(
  error: unknown,
  request: HttpRequest<unknown>,
  next: HttpHandlerFn,
  authService: AuthService
) {
  if (!(error instanceof HttpErrorResponse) || error.status !== 401 || hasRetried(request)) {
    return throwError(() => error);
  }

  return from(authService.refreshAccessToken()).pipe(
    switchMap((token) => {
      if (!token) {
        return throwError(() => error);
      }

      const retryRequest = withBearerToken(
        request.clone({ setHeaders: { 'X-Auth-Retry': 'true' } }),
        token
      );
      return next(retryRequest);
    }),
    catchError((refreshError) => throwError(() => refreshError))
  );
}

function withBearerToken(request: HttpRequest<unknown>, token: string | null): HttpRequest<unknown> {
  if (!token) {
    return request;
  }

  return request.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  });
}

function shouldSkipAuth(request: HttpRequest<unknown>): boolean {
  const apiBaseUrl = environment.apiBaseUrl.replace(/\/$/, '');
  const isApiRequest = request.url.startsWith(apiBaseUrl) || request.url.startsWith('/api/');
  const isAuthEndpoint = AUTH_ENDPOINTS.some((endpoint) => request.url.includes(endpoint));

  return !isApiRequest || isAuthEndpoint;
}

function hasRetried(request: HttpRequest<unknown>): boolean {
  return request.headers.get('X-Auth-Retry') === 'true';
}
