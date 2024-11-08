import type { Resort, PriceData } from './types';
import { collection, getDocs, query, orderBy, Firestore, where } from 'firebase/firestore';

export async function fetchResorts(db: Firestore): Promise<Resort[]> {
	const resortsRef = collection(db, 'resorts');
	const querySnapshot = await getDocs(resortsRef);

	const resorts: Resort[] = [];
	querySnapshot.forEach((doc) => {
		const data = doc.data();
		resorts.push({
			id: data.id,
			name: data.name,
			location: data.location,
			logo: data.logo
		});
	});

	return resorts;
}

export async function fetchPriceData(db: Firestore, date?: Date): Promise<PriceData[]> {
	const pricesRef = collection(db, 'prices');

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
			resortId: data.resortId,
			date: data.date,
			price: data.price,
			currency: data.currency
		});
	});

	return prices;
}
