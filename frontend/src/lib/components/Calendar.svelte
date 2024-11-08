<script lang="ts">
	import type { PriceData, Resort } from '$lib/types';

	interface Props {
		prices: PriceData[];
		resorts: Resort[];
		anchorDate: Date;
		startDate?: Date;
		endDate?: Date;
	}

	const { prices, resorts, startDate, endDate, anchorDate }: Props = $props();

	const today = new Date();

	function formatPrice(price: number, currency: string) {
		return new Intl.NumberFormat('en-US', {
			style: 'currency',
			currency
		}).format(price);
	}

	function getMonthWeeks(date: Date) {
		const weeks = [];
		const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
		const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);

		const start = new Date(firstDay);
		start.setDate(start.getDate() - start.getDay());

		const end = new Date(lastDay);
		end.setDate(end.getDate() + (6 - end.getDay()));

		for (let d = new Date(start); d <= end; d.setDate(d.getDate() + 1)) {
			weeks.push(new Date(d));
		}

		return weeks;
	}

	const allDates = $derived(getMonthWeeks(anchorDate));
	const weeks = $derived(
		Array.from({ length: allDates.length / 7 }, (_, i) => allDates.slice(i * 7, (i + 1) * 7))
	);

	$inspect(weeks);

	$inspect(startDate);
	$inspect(endDate);

	function getCheapestResortForDate(date: Date) {
		const pricesForDate = prices
			.filter((p) => {
				return p.date === date.toISOString().split('T')[0];
			})
			.sort((a, b) => a.price - b.price);

		if (pricesForDate.length === 0) return null;

		const cheapestPrice = pricesForDate[0];
		const resort = resorts.find((r) => r.name === cheapestPrice.resortName);

		return {
			resort,
			price: cheapestPrice.price
		};
	}

	const highlightToday = startDate && endDate ? false : true;
</script>

<div class="rounded-lg bg-white p-6 pt-0 shadow-md">
	<table class="w-full table-fixed border-collapse">
		<thead>
			<tr>
				{#each ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] as day}
					<th class="border-b border-gray-200 p-2 text-center text-sm font-medium text-gray-600"
						>{day}</th
					>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each weeks as week}
				<tr>
					{#each week as date}
						{@const cheapestData = getCheapestResortForDate(date)}
						{@const isCurrentDate = date.toDateString() === today.toDateString()}
						{@const withinRange =
							startDate && endDate ? date >= startDate && date <= endDate : false}
						<td class="border border-gray-100 p-0">
							<a
								href="/dates/{date.toISOString().split('T')[0]}"
								class="block transition-colors duration-200"
							>
								<div
									class="block h-24 p-2
									{date.getMonth() !== anchorDate.getMonth() ? 'bg-gray-200' : 'hover:bg-blue-50'} 
										{(isCurrentDate && highlightToday) || withinRange ? 'bg-blue-100' : ''}
										
										"
								>
									<div class="mb-1 flex items-center justify-between text-sm">
										<span class="text-gray-600">
											{date.toLocaleDateString('en-US', {
												month: 'short',
												day: 'numeric'
											})}
										</span>
										{#if isCurrentDate && highlightToday}
											<span class="rounded bg-blue-100 px-2 py-0.5 text-xs text-blue-600"
												>Today</span
											>
										{/if}
									</div>
									{#if cheapestData}
										<div class="flex flex-col overflow-hidden">
											<span class="truncate font-mono text-lg font-medium text-blue-600">
												{formatPrice(cheapestData.price, 'USD')}
											</span>
											<span class="truncate text-sm font-medium text-gray-700">
												{cheapestData.resort?.name}
											</span>
										</div>
									{:else}
										<span class="text-gray-400">No prices available</span>
									{/if}
								</div>
							</a>
						</td>
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>
