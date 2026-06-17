import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { IonButton, IonContent, IonInput, IonSelect, IonSelectOption } from '@ionic/angular/standalone';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [FormsModule, IonButton, IonContent, IonInput, IonSelect, IonSelectOption, RouterLink],
  templateUrl: './signup.page.html',
  styleUrl: './signup.page.scss'
})
export class SignupPage {
  userType: 'comum' | 'empresa' | 'ong' = 'comum';
}
