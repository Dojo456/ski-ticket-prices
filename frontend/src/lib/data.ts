import type { Resort, PriceData } from './types';
import { collection, getDocs, query, orderBy, Firestore, where } from 'firebase/firestore';

export async function fetchResorts(db: Firestore): Promise<Resort[]> {
	const resortsRef = collection(db, 'resorts');
	const querySnapshot = await getDocs(resortsRef);

	const resorts: Resort[] = [];
	querySnapshot.forEach((doc) => {
		const data = doc.data();
		resorts.push({
			name: data.name,
			location: data.location,
			logo: data.logo
		});
	});

	return resorts;
}

export async function fetchPriceData(db: Firestore, date?: string): Promise<PriceData[]> {
	const pricesRef = collection(db, 'lift_tickets');

	let q;
	if (date) {
		q = query(pricesRef, orderBy('date'), where('date', '==', date));
	} else {
		q = query(pricesRef, orderBy('date'));
	}
	const querySnapshot = await getDocs(q);

	const prices: PriceData[] = [];
	querySnapshot.forEach((doc) => {
		const data = doc.data();
		prices.push({
			resortName: data.resort_name,
			date: data.date,
			price: data.price
		});
	});

	return prices;
}
