import { APP_INITIALIZER, ApplicationConfig, LOCALE_ID, inject } from '@angular/core';
import { provideRouter, RouteReuseStrategy } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { IonicRouteStrategy, provideIonicAngular } from '@ionic/angular/standalone';

import { routes } from './app.routes';
import { authInterceptor } from './core/auth/auth.interceptor';
import { AuthService } from './core/auth/auth.service';

function initializeAuthSession() {
  const authService = inject(AuthService);
  return () => authService.initializeSession();
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideIonicAngular(),
    provideRouter(routes),
    provideHttpClient(withInterceptors([authInterceptor])),
    {
      provide: APP_INITIALIZER,
      useFactory: initializeAuthSession,
      multi: true
    },
    { provide: LOCALE_ID, useValue: 'pt-BR' },
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy }
  ]
};
