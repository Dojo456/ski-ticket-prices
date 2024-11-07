interface Resort {
  id: string;
  name: string;
  location: string;
  logo?: string;
}

interface PriceData {
  resortId: string;
  date: string;
  price: number;
  currency: string;
}

export type { Resort, PriceData }; 