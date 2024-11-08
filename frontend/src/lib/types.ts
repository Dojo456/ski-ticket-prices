interface Resort {
	name: string;
	location: string;
	logo?: string;
}

interface PriceData {
	date: string;
	price: number;
	resortName: string;
}

export type { Resort, PriceData };
