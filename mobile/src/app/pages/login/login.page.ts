import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { IonButton, IonContent, IonInput } from '@ionic/angular/standalone';

import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, IonButton, IonContent, IonInput, RouterLink],
  templateUrl: './login.page.html',
  styleUrl: './login.page.scss'
})
export class LoginPage {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  readonly loading = signal(false);
  readonly error = signal('');

  username = '';
  password = '';
  showPassword = false;

  async login(): Promise<void> {
    this.loading.set(true);
    this.error.set('');

    try {
      await this.authService.login({ username: this.username, password: this.password });
      await this.router.navigateByUrl('/');
    } catch {
      this.error.set('Usuario ou senha invalidos.');
    } finally {
      this.loading.set(false);
    }
  }
}
