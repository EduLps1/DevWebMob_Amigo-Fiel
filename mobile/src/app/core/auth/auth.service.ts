import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { Preferences } from '@capacitor/preferences';
import { firstValueFrom } from 'rxjs';

import { environment } from '../../../environments/environment';
import {
  AuthUser,
  LoginCredentials,
  LoginResponse,
  RefreshResponse,
  TokenPair
} from './auth.models';

const ACCESS_TOKEN_KEY = 'amigo_fiel.access_token';
const REFRESH_TOKEN_KEY = 'amigo_fiel.refresh_token';
const USER_KEY = 'amigo_fiel.user';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = environment.apiBaseUrl.replace(/\/$/, '');
  private readonly userSignal = signal<AuthUser | null>(null);

  readonly currentUser = this.userSignal.asReadonly();
  readonly isAuthenticated = computed(() => this.userSignal() !== null);

  async initializeSession(): Promise<void> {
    const storedUser = await Preferences.get({ key: USER_KEY });

    if (!storedUser.value) {
      this.userSignal.set(null);
      return;
    }

    try {
      this.userSignal.set(JSON.parse(storedUser.value) as AuthUser);
    } catch {
      await this.logout();
    }
  }

  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await firstValueFrom(
      this.http.post<LoginResponse>(`${this.apiBaseUrl}/auth/token/`, credentials)
    );

    await this.persistSession(response, response.user);
    return response;
  }

  async refreshAccessToken(): Promise<string | null> {
    const refresh = await this.getRefreshToken();

    if (!refresh) {
      await this.logout();
      return null;
    }

    try {
      const response = await firstValueFrom(
        this.http.post<RefreshResponse>(`${this.apiBaseUrl}/auth/refresh/`, { refresh })
      );
      await Preferences.set({ key: ACCESS_TOKEN_KEY, value: response.access });

      if (response.refresh) {
        await Preferences.set({ key: REFRESH_TOKEN_KEY, value: response.refresh });
      }

      return response.access;
    } catch {
      await this.logout();
      return null;
    }
  }

  async loadCurrentUser(): Promise<AuthUser | null> {
    const user = await firstValueFrom(this.http.get<AuthUser>(`${this.apiBaseUrl}/auth/me/`));
    this.userSignal.set(user);
    await Preferences.set({ key: USER_KEY, value: JSON.stringify(user) });
    return user;
  }

  async logout(): Promise<void> {
    await Promise.all([
      Preferences.remove({ key: ACCESS_TOKEN_KEY }),
      Preferences.remove({ key: REFRESH_TOKEN_KEY }),
      Preferences.remove({ key: USER_KEY })
    ]);
    this.userSignal.set(null);
  }

  async getAccessToken(): Promise<string | null> {
    const result = await Preferences.get({ key: ACCESS_TOKEN_KEY });
    return result.value;
  }

  async getRefreshToken(): Promise<string | null> {
    const result = await Preferences.get({ key: REFRESH_TOKEN_KEY });
    return result.value;
  }

  private async persistSession(tokens: TokenPair, user: AuthUser): Promise<void> {
    await Promise.all([
      Preferences.set({ key: ACCESS_TOKEN_KEY, value: tokens.access }),
      Preferences.set({ key: REFRESH_TOKEN_KEY, value: tokens.refresh }),
      Preferences.set({ key: USER_KEY, value: JSON.stringify(user) })
    ]);
    this.userSignal.set(user);
  }
}
