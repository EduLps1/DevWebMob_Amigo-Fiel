import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { environment } from '../../../environments/environment';
import { MobileHome, MobileLoja, MobileOng, MobilePet, MobileProduto } from './mobile-home.models';

@Injectable({
  providedIn: 'root'
})
export class MobileHomeService {
  private readonly http = inject(HttpClient);
  private readonly apiBaseUrl = environment.apiBaseUrl.replace(/\/$/, '');

  getHome() {
    return this.http.get<MobileHome>(`${this.apiBaseUrl}/mobile/home/`);
  }

  getPets(query = '') {
    return this.http.get<MobilePet[]>(`${this.apiBaseUrl}/mobile/pets/`, {
      params: query ? { q: query } : {}
    });
  }

  getProdutos(query = '') {
    return this.http.get<MobileProduto[]>(`${this.apiBaseUrl}/mobile/produtos/`, {
      params: query ? { q: query } : {}
    });
  }

  getLojas(query = '') {
    return this.http.get<MobileLoja[]>(`${this.apiBaseUrl}/mobile/lojas/`, {
      params: query ? { q: query } : {}
    });
  }

  getOngs(query = '') {
    return this.http.get<MobileOng[]>(`${this.apiBaseUrl}/mobile/ongs/`, {
      params: query ? { q: query } : {}
    });
  }
}
