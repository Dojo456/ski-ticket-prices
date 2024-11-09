interface Location {
	name: string;
}

interface PriceData {
	date: string;
	price: number;
	locationName: string;
}

export type { Location, PriceData };
