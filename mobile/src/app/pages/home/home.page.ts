import { Component, inject, signal } from '@angular/core';
import {
  IonButton,
  IonInput,
  IonContent
} from '@ionic/angular/standalone';
import { FormsModule } from '@angular/forms';
import { CurrencyPipe } from '@angular/common';
import { RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';

import { AuthService } from '../../core/auth/auth.service';
import { MobileHome, MobileLoja, MobileOng, MobilePet, MobileProduto } from '../../core/mobile-home/mobile-home.models';
import { MobileHomeService } from '../../core/mobile-home/mobile-home.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CurrencyPipe,
    FormsModule,
    RouterLink,
    IonButton,
    IonContent,
    IonInput
  ],
  templateUrl: './home.page.html',
  styleUrl: './home.page.scss'
})
export class HomePage {
  private readonly authService = inject(AuthService);
  private readonly mobileHomeService = inject(MobileHomeService);

  readonly user = this.authService.currentUser;
  readonly loading = signal(false);
  readonly homeLoading = signal(false);
  readonly error = signal('');
  readonly home = signal<MobileHome | null>(null);

  username = '';
  password = '';
  showPassword = false;

  constructor() {
    void this.loadHome();
  }

  async login(): Promise<void> {
    this.loading.set(true);
    this.error.set('');

    try {
      await this.authService.login({
        username: this.username,
        password: this.password
      });
      await this.authService.loadCurrentUser();
    } catch {
      this.error.set('Usuario ou senha invalidos.');
    } finally {
      this.loading.set(false);
    }
  }

  async logout(): Promise<void> {
    await this.authService.logout();
  }

  async loadHome(): Promise<void> {
    this.homeLoading.set(true);

    try {
      this.home.set(await firstValueFrom(this.mobileHomeService.getHome()));
    } finally {
      this.homeLoading.set(false);
    }
  }

  petSubtitle(pet: MobilePet): string {
    return [pet.especie, pet.raca, pet.cidade].filter(Boolean).join(' - ');
  }

  productSubtitle(produto: MobileProduto): string {
    return produto.empresa_nome;
  }

  lojaSubtitle(loja: MobileLoja): string {
    return loja.cidade || 'Loja parceira';
  }

  ongSubtitle(ong: MobileOng): string {
    return ong.cidade || 'ONG parceira';
  }
}
