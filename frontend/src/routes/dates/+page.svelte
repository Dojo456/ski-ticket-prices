<script lang="ts">
	import { page } from '$app/stores';
	import Calendar from '$lib/components/Calendar.svelte';
	import { fetchResorts, fetchPriceData } from '$lib/data';
	import { db } from '$lib/firebase.svelte';
	import type { PriceData, Resort } from '$lib/types';
	import { onMount } from 'svelte';

	let priceData = $state<PriceData[] | null>(null);
	let resorts = $state<Resort[] | null>(null);

	onMount(() => {
		db.subscribe(async (db) => {
			if (db) {
				fetchPriceData(db).then((data) => (priceData = data));
				fetchResorts(db).then((data) => (resorts = data));
			}
		});
	});

	const monthParam = $page.url.searchParams.get('month');
	const yearParam = $page.url.searchParams.get('year');
	const locationParam = $page.url.searchParams.get('location');
	const startDateParam = $page.url.searchParams.get('startDate');
	const endDateParam = $page.url.searchParams.get('endDate');

	const today = new Date();

	const startDate = startDateParam ? new Date(startDateParam) : undefined;
	const endDate = endDateParam ? new Date(endDateParam) : undefined;

	const anchorDate = new Date(
		yearParam ? parseInt(yearParam) : today.getFullYear(),
		monthParam ? parseInt(monthParam) - 1 : today.getMonth()
	);

	function previousMonth() {
		const newDate = new Date(anchorDate);
		newDate.setMonth(newDate.getMonth() - 1);

		window.location.href = `/dates?year=${newDate.getFullYear()}&month=${newDate.getMonth() + 1}`;
	}

	function nextMonth() {
		const newDate = new Date(anchorDate);
		newDate.setMonth(newDate.getMonth() + 1);

		window.location.href = `/dates?year=${newDate.getFullYear()}&month=${newDate.getMonth() + 1}`;
	}
</script>

<svelte:head>
	<title>Calendar</title>
</svelte:head>

<main class="mx-auto max-w-6xl px-4 pb-8">
	<div class="mb-4 mt-4 flex items-center justify-between">
		<button class="btn" onclick={previousMonth}> &larr; Previous </button>
		<h2 class="text-2xl font-bold">
			Lift Tickets for {anchorDate.toLocaleString('default', { month: 'long', year: 'numeric' })}
		</h2>
		<button class="btn" onclick={nextMonth}> Next &rarr; </button>
	</div>

	<Calendar resorts={resorts ?? []} prices={priceData ?? []} {anchorDate} {startDate} {endDate} />
</main>
