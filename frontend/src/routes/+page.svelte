<script lang="ts">
	import SearchBar from '../lib/components/SearchBar.svelte';
</script>

<svelte:head>
	<title>Lift Tickets Calendar</title>
</svelte:head>

<main class="mx-auto max-w-6xl px-4 py-8">
	<div class="mb-8">
		<h1 class="text-3xl font-bold text-gray-900">Find the Best Lift Ticket Prices</h1>
		<p class="mt-2 text-gray-600">
			Compare daily rates across top ski resorts and plan your perfect powder day.
		</p>
	</div>

	<div class="mb-8">
		<h2 class="mb-4 text-2xl font-semibold text-gray-900">How does it work?</h2>
		<div class="space-y-4">
			<div class="flex items-start gap-4">
				<span
					class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 font-semibold text-blue-600"
					>1</span
				>
				<p class="text-gray-600">Select your desired ski dates and location</p>
			</div>
			<div class="flex items-start gap-4">
				<span
					class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 font-semibold text-blue-600"
					>2</span
				>
				<p class="text-gray-600">Compare prices from multiple resorts in the area</p>
			</div>
			<div class="flex items-start gap-4">
				<span
					class="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 font-semibold text-blue-600"
					>3</span
				>
				<p class="text-gray-600">
					Book directly through the resort's website at the best available rate
				</p>
			</div>
		</div>
	</div>

	<div class="mb-8">
		<SearchBar />
	</div>
</main>
