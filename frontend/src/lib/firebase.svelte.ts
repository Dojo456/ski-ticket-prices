import type { Firestore } from 'firebase/firestore';
import { writable } from 'svelte/store';

export const db = writable<Firestore | null>(null);
