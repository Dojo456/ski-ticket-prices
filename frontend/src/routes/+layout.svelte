<script lang="ts">
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import { onMount } from 'svelte';
	let { children } = $props();
	import { initializeApp } from 'firebase/app';
	import { getAnalytics } from 'firebase/analytics';
	import { getFirestore } from 'firebase/firestore';
	import { db } from '$lib/firebase.svelte';

	onMount(async () => {
		// Your web app's Firebase configuration
		// For Firebase JS SDK v7.20.0 and later, measurementId is optional
		const firebaseConfig = {
			apiKey: 'AIzaSyCu34hGcOhrJj0jF458Da0C6wN3sb6op3g',
			authDomain: 'personal-website-8f505.firebaseapp.com',
			databaseURL: 'https://ski-ticket-prices.firebaseio.com',
			projectId: 'personal-website-8f505',
			storageBucket: 'personal-website-8f505.appspot.com',
			messagingSenderId: '477534951771',
			appId: '1:477534951771:web:3969fca3f2e5238f03627e',
			measurementId: 'G-91TP9YRKDK'
		};

		// Initialize Firebase
		const app = initializeApp(firebaseConfig, 'ski-ticket-prices');
		const analytics = getAnalytics(app);
		db.set(getFirestore(app));
	});
</script>

<div class="min-h-screen bg-gray-50">
	<Navbar />
	{@render children()}
	<footer class="mt-auto border-t bg-white py-6">
		<div class="mx-auto max-w-6xl px-4 text-center text-sm text-gray-600">
			© {new Date().getFullYear()} SkiPrice. Find the best deals on ski lift tickets.
		</div>
	</footer>
</div>

<style>
	:global(body) {
		/* Prevent layout shift in Firefox */
		overflow-y: scroll;
		scrollbar-width: stable;
	}

	:global(.btn) {
		@apply rounded bg-blue-500 px-4 py-2 text-white transition-colors hover:bg-blue-600;
	}
</style>
