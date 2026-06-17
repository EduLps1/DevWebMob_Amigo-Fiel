export interface MobilePet {
  id: number;
  nome: string;
  especie: string;
  raca: string;
  cidade: string;
  image_url: string | null;
  detail_path: string;
}

export interface MobileProduto {
  id: number;
  nome: string;
  empresa_nome: string;
  preco: string;
  image_url: string | null;
  detail_path: string;
}

export interface MobileLoja {
  id: number;
  razao_social: string;
  cidade: string;
  image_url: string | null;
  detail_path: string;
}

export interface MobileOng {
  id: number;
  nome_fantasia: string;
  cidade: string;
  image_url: string | null;
  detail_path: string;
}

export interface MobileHome {
  pets: MobilePet[];
  produtos: MobileProduto[];
  lojas: MobileLoja[];
  ongs: MobileOng[];
}
