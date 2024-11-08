<script lang="ts">
	import { page } from '$app/stores';
	import { fetchResorts, fetchPriceData } from '$lib/data';
	import { db } from '$lib/firebase.svelte';
	import type { PriceData, Resort } from '$lib/types';
	import { onMount } from 'svelte';

	const date = $page.params.date;

	let priceData = $state<PriceData[] | null>(null);

	onMount(() => {
		db.subscribe(async (db) => {
			if (db) {
				priceData = await fetchPriceData(db);
			}
		});
	});

	function formatPrice(price: number, currency: string) {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency
		}).format(price);
	}
</script>

<main class="mx-auto max-w-6xl px-4 py-8">
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-gray-900">Lift Ticket</h1>
	</div>
</main>
