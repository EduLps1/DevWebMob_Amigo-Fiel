import { CurrencyPipe } from '@angular/common';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { IonButton, IonContent, IonInput } from '@ionic/angular/standalone';
import { Observable, firstValueFrom } from 'rxjs';

import { MobileHomeService } from '../../core/mobile-home/mobile-home.service';
import { MobileLoja, MobileOng, MobilePet, MobileProduto } from '../../core/mobile-home/mobile-home.models';

type Section = 'pets' | 'produtos' | 'lojas' | 'ongs';
type CatalogItem = Record<string, unknown>;
type CatalogResponse = MobilePet[] | MobileProduto[] | MobileLoja[] | MobileOng[];

const SECTION_META: Record<Section, { title: string; subtitle: string; empty: string }> = {
  pets: {
    title: 'Procurando Adotar',
    subtitle: 'Pets disponiveis cadastrados por tutores e ONGs.',
    empty: 'Sem pets cadastrados ainda.'
  },
  produtos: {
    title: 'Produtos',
    subtitle: 'Marketplace pet com lojas parceiras.',
    empty: 'Sem produtos cadastrados ainda.'
  },
  lojas: {
    title: 'Lojas',
    subtitle: 'Empresas parceiras do Amigo Fiel.',
    empty: 'Sem lojas cadastradas ainda.'
  },
  ongs: {
    title: 'ONGs',
    subtitle: 'ONGs e protetores parceiros da plataforma.',
    empty: 'Sem ONGs cadastradas ainda.'
  }
};

@Component({
  selector: 'app-catalog',
  standalone: true,
  imports: [CurrencyPipe, FormsModule, IonButton, IonContent, IonInput, RouterLink],
  templateUrl: './catalog.page.html',
  styleUrl: './catalog.page.scss'
})
export class CatalogPage {
  private readonly route = inject(ActivatedRoute);
  private readonly mobileHomeService = inject(MobileHomeService);

  readonly section = signal<Section>((this.route.snapshot.data['section'] as Section) || 'pets');
  readonly items = signal<CatalogItem[]>([]);
  readonly loading = signal(false);

  query = '';

  get meta() {
    return SECTION_META[this.section()];
  }

  constructor() {
    void this.load();
  }

  async load(): Promise<void> {
    this.loading.set(true);
    const section = this.section();

    try {
      const request: Observable<CatalogResponse> =
        section === 'pets'
          ? this.mobileHomeService.getPets(this.query)
          : section === 'produtos'
            ? this.mobileHomeService.getProdutos(this.query)
            : section === 'lojas'
              ? this.mobileHomeService.getLojas(this.query)
              : this.mobileHomeService.getOngs(this.query);

      this.items.set((await firstValueFrom(request)) as unknown as CatalogItem[]);
    } finally {
      this.loading.set(false);
    }
  }

  titleOf(item: CatalogItem): string {
    return String(item['nome'] || item['razao_social'] || item['nome_fantasia'] || 'Item');
  }

  subtitleOf(item: CatalogItem): string {
    const section = this.section();
    if (section === 'pets') {
      return [item['especie'], item['raca'], item['cidade']].filter(Boolean).join(' - ');
    }
    if (section === 'produtos') {
      return String(item['empresa_nome'] || '');
    }
    return String(item['cidade'] || 'Parceiro Amigo Fiel');
  }

  imageOf(item: CatalogItem): string {
    return String(item['image_url'] || 'assets/img/amigo-fiel-logo.png');
  }

  priceOf(item: CatalogItem): number | null {
    if (this.section() !== 'produtos') {
      return null;
    }
    return Number(item['preco'] || 0);
  }
}
