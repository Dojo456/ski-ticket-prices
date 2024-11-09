import type { Location, PriceData } from './types';
import { collection, getDocs, query, orderBy, Firestore, where } from 'firebase/firestore';

export async function fetchLocations(db: Firestore): Promise<Location[]> {
	const locationsRef = collection(db, 'locations');
	const querySnapshot = await getDocs(locationsRef);

	const locations: Location[] = [];
	querySnapshot.forEach((doc) => {
		const data = doc.data();
		locations.push({
			name: data.name
		});
	});

	return locations;
}

export async function fetchPriceData(db: Firestore, date?: string): Promise<PriceData[]> {
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
			locationName: data.location_name,
			date: data.date,
			price: data.price
		});
	});

	return prices;
}
