<script lang="ts">
	import Calendar from '$lib/components/Calendar.svelte';
	import { resorts, priceData } from '$lib/data';
</script>

<div class="min-h-screen bg-gray-50">
	<header class="bg-white shadow-sm">
		<div class="mx-auto max-w-6xl p-4">
			<h1 class="text-2xl font-bold text-gray-900">Ski Resort Lift Tickets</h1>
			<p class="text-gray-600">Compare lift ticket prices across different resorts</p>
		</div>
	</header>

	<main class="py-8">
		<Calendar {resorts} prices={priceData} />
	</main>
</div>
