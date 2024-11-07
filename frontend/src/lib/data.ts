import type { Resort, PriceData } from './types';

export const resorts: Resort[] = [
	{
		id: 'vail',
		name: 'Vail',
		location: 'Colorado, USA',
		logo: '/images/vail.png'
	},
	{
		id: 'whistler',
		name: 'Whistler Blackcomb',
		location: 'British Columbia, Canada',
		logo: '/images/whistler.png'
	}
	// Add more resorts as needed
];

// Generate sample price data for the next 30 days
const generateSamplePrices = (): PriceData[] => {
	const prices: PriceData[] = [];
	const today = new Date();

	resorts.forEach((resort) => {
		for (let i = 0; i < 30; i++) {
			const date = new Date(today);
			date.setDate(date.getDate() + i);

			prices.push({
				resortId: resort.id,
				date: date.toISOString().split('T')[0],
				price: Math.floor(Math.random() * (200 - 80) + 80),
				currency: 'USD'
			});
		}
	});

	return prices;
};

export const priceData = generateSamplePrices();
