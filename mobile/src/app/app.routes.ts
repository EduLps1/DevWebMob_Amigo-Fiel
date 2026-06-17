import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/home/home.page').then((m) => m.HomePage)
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.page').then((m) => m.LoginPage)
  },
  {
    path: 'cadastro',
    loadComponent: () => import('./pages/signup/signup.page').then((m) => m.SignupPage)
  },
  {
    path: 'adotar',
    loadComponent: () => import('./pages/catalog/catalog.page').then((m) => m.CatalogPage),
    data: { section: 'pets' }
  },
  {
    path: 'produtos',
    loadComponent: () => import('./pages/catalog/catalog.page').then((m) => m.CatalogPage),
    data: { section: 'produtos' }
  },
  {
    path: 'lojas',
    loadComponent: () => import('./pages/catalog/catalog.page').then((m) => m.CatalogPage),
    data: { section: 'lojas' }
  },
  {
    path: 'ongs',
    loadComponent: () => import('./pages/catalog/catalog.page').then((m) => m.CatalogPage),
    data: { section: 'ongs' }
  }
];
