<script lang="ts">
	import { page } from '$app/stores';
	import Calendar from '$lib/components/Calendar.svelte';
	import SearchBar from '$lib/components/SearchBar.svelte';
	import { fetchResorts, fetchPriceData } from '$lib/data';
	import { db } from '$lib/firebase.svelte';
	import type { PriceData, Resort } from '$lib/types';
	import { parseDateIgnoreTZ } from '$lib/utils';
	import { onMount } from 'svelte';

	// Get search parameters
	const startDateParam = $page.url.searchParams.get('startDate');
	const endDateParam = $page.url.searchParams.get('endDate');
	const locationParam = $page.url.searchParams.get('location');

	let priceData = $state<PriceData[] | null>(null);
	let resorts = $state<Resort[] | null>(null);

	// Parse dates
	const startDate = startDateParam ? parseDateIgnoreTZ(startDateParam) : new Date();
	const endDate = endDateParam ? parseDateIgnoreTZ(endDateParam) : new Date();

	const location = locationParam ?? 'All Locations';

	// Set anchor date to start of search period
	const anchorDate = new Date(startDate);

	onMount(() => {
		db.subscribe(async (db) => {
			if (db) {
				priceData = await fetchPriceData(db);
				resorts = await fetchResorts(db);
			}
		});
	});
</script>

<main class="mx-auto max-w-6xl px-4 pb-8">
	<div class="mt-4 flex w-full flex-row items-center gap-4">
		<div class="w-1/4">
			<SearchBar defaultStartDate={startDate} defaultEndDate={endDate} defaultLocation={location} />
		</div>
		{#if priceData && resorts}
			<Calendar prices={priceData} {resorts} {anchorDate} {startDate} {endDate} />
		{:else}
			<div class="flex h-64 items-center justify-center">
				<div class="text-lg text-gray-600">Loading...</div>
			</div>
		{/if}
	</div>
</main>
