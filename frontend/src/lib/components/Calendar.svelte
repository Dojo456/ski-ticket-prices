<script lang="ts">
	import type { PriceData, Resort } from '$lib/types';

	export let prices: PriceData[];
	export let resorts: Resort[];

	let currentDate = new Date();

	$: monthDates = getMonthDates(currentDate);

	function getMonthDates(date: Date) {
		const dates = [];
		const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
		const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

		for (let d = new Date(firstDay); d <= lastDay; d.setDate(d.getDate() + 1)) {
			dates.push(new Date(d));
		}

		return dates;
	}

	function formatPrice(price: number, currency: string) {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency
		}).format(price);
	}

	function getPriceForDate(resortId: string, date: Date) {
		const dateStr = date.toISOString().split('T')[0];
		return prices.find((p) => p.resortId === resortId && p.date === dateStr);
	}

	function previousMonth() {
		currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1);
	}

	function nextMonth() {
		currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1);
	}

	// Modify getMonthWeeks to return a flat array of dates
	function getMonthWeeks(date: Date) {
		const weeks = [];
		const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
		const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

		// Start from the beginning of the week containing the first day
		const start = new Date(firstDay);
		start.setDate(start.getDate() - start.getDay());

		// End at the last day of the week containing the last day
		const end = new Date(lastDay);
		end.setDate(end.getDate() + (6 - end.getDay()));

		// Generate all dates
		for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
			weeks.push(new Date(d));
		}

		return weeks;
	}

	$: allDates = getMonthWeeks(currentDate);
	$: weeks = Array.from({ length: allDates.length / 7 }, (_, i) =>
		allDates.slice(i * 7, (i + 1) * 7)
	);

	function getCheapestResortForDate(date: Date) {
		const dateStr = date.toISOString().split('T')[0];
		const pricesForDate = prices
			.filter((p) => p.date === dateStr)
			.sort((a, b) => a.price - b.price);

		if (pricesForDate.length === 0) return null;

		const cheapestPrice = pricesForDate[0];
		const resort = resorts.find((r) => r.id === cheapestPrice.resortId);

		return {
			resort,
			price: cheapestPrice.price,
			currency: cheapestPrice.currency
		};
	}
</script>

<div class="mx-auto w-full max-w-6xl p-4">
	<div class="mb-4 flex items-center justify-between">
		<button class="btn" on:click={previousMonth}>&larr; Previous</button>
		<h2 class="text-xl font-bold">
			{currentDate.toLocaleString('default', { month: 'long', year: 'numeric' })}
		</h2>
		<button class="btn" on:click={nextMonth}>Next &rarr;</button>
	</div>

	<div class="overflow-x-auto">
		<table class="fi w-full table-fixed border-collapse">
			<thead>
				<tr>
					<th class="border p-2 text-center">Sun</th>
					<th class="border p-2 text-center">Mon</th>
					<th class="border p-2 text-center">Tue</th>
					<th class="border p-2 text-center">Wed</th>
					<th class="border p-2 text-center">Thu</th>
					<th class="border p-2 text-center">Fri</th>
					<th class="border p-2 text-center">Sat</th>
				</tr>
			</thead>
			<tbody>
				{#each weeks as week}
					<tr>
						{#each week as date}
							{@const cheapestData = getCheapestResortForDate(date)}
							<td
								class="h-24 w-24 border p-3 align-top {date.getMonth() !== currentDate.getMonth()
									? 'bg-gray-50'
									: ''}"
							>
								<div class="mb-1 text-sm text-gray-500">
									{date.toLocaleDateString('en-US', {
										month: 'short',
										day: 'numeric'
									})}
								</div>
								{#if cheapestData}
									<div class="flex flex-col gap-1 overflow-hidden">
										<span class="truncate font-mono text-lg">
											{formatPrice(cheapestData.price, cheapestData.currency)}
										</span>
										<span class="truncate text-sm font-medium text-gray-700">
											{cheapestData.resort?.name}
										</span>
									</div>
								{:else}
									<span class="text-gray-400">-</span>
								{/if}
							</td>
						{/each}
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>

<style>
	.btn {
		@apply rounded bg-blue-500 px-4 py-2 text-white transition-colors hover:bg-blue-600;
	}
</style>
