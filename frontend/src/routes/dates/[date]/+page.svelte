<script lang="ts">
	import { page } from '$app/stores';
	import { fetchResorts, fetchPriceData } from '$lib/data';
	import { db } from '$lib/firebase.svelte';
	import type { PriceData, Resort } from '$lib/types';
	import { onMount } from 'svelte';

	const date = $page.params.date;
	const timezone = new Date().toISOString().split('T')[1];
	const dateObj = new Date(date + 'T' + timezone);

	let priceData = $state<PriceData[] | null>(null);

	onMount(() => {
		db.subscribe(async (db) => {
			if (db) {
				priceData = await fetchPriceData(db, date);
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

<svelte:head>
	<title
		>Prices For {dateObj.toLocaleDateString('en-US', {
			month: 'long',
			day: 'numeric',
			year: 'numeric'
		})}
	</title>
</svelte:head>

<main class="mx-auto max-w-6xl px-4 py-8">
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-gray-900">
			Lift Ticket Prices for {dateObj.toLocaleDateString('en-US', {
				month: 'long',
				day: 'numeric',
				year: 'numeric'
			})}
		</h1>
	</div>

	{#if priceData}
		{#if priceData.length > 0}
			<div class="overflow-x-auto">
				<table class="min-w-full divide-y divide-gray-200">
					<thead class="bg-gray-50">
						<tr>
							<th
								scope="col"
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Resort</th
							>
							<th
								scope="col"
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>Price</th
							>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-200 bg-white">
						{#each priceData as price}
							<tr>
								<td class="whitespace-nowrap px-6 py-4">{price.resortName}</td>
								<td class="whitespace-nowrap px-6 py-4">{formatPrice(price.price, 'USD')}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{:else}
			<p>
				No data found for {dateObj.toLocaleDateString('en-US', {
					month: 'long',
					day: 'numeric',
					year: 'numeric'
				})}
			</p>
		{/if}
	{:else}
		<p>Loading...</p>
	{/if}
</main>
