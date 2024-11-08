<script lang="ts">
	import { fetchResorts, fetchPriceData } from '$lib/data';
	import { db } from '$lib/firebase.svelte';
	import type { PriceData, Resort } from '$lib/types';
	import { onMount } from 'svelte';

	let priceData = $state<PriceData[] | null>(null);
	let resorts = $state<Resort[] | null>(null);

	onMount(() => {
		db.subscribe(async (db) => {
			if (db) {
				priceData = await fetchPriceData(db);
				resorts = await fetchResorts(db);
			}
		});
	});

	function getAveragePrice(resortId: string) {
		if (!priceData) return 0;

		const resortPrices = priceData.filter((p) => p.resortId === resortId);
		const total = resortPrices.reduce((sum, p) => sum + p.price, 0);
		return total / resortPrices.length;
	}
</script>

<main class="mx-auto max-w-6xl px-4 py-8">
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-gray-900">Our Ski Resorts</h1>
		<p class="mt-2 text-gray-600">Explore our collection of premier ski destinations.</p>
	</div>

	<div class="grid grid-cols-1 gap-8 md:grid-cols-3">
		{#if resorts}
			{#each resorts as resort}
				<div class="rounded-lg bg-white p-6 shadow-md">
					<h2 class="text-2xl font-bold text-gray-900">{resort.name}</h2>
					<p class="mt-2 text-gray-600">Average price: ${getAveragePrice(resort.id)}</p>
					<p class="mt-2 text-gray-600">Resort ID: {resort.id}</p>
				</div>
			{/each}
		{:else}
			<div>Loading...</div>
		{/if}
	</div>
</main>
