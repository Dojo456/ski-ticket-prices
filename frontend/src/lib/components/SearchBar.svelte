<script lang="ts">
	import { enhance } from '$app/forms';

	interface Props {
		defaultStartDate?: Date;
		defaultEndDate?: Date;
		defaultLocation?: string;
	}

	const { defaultStartDate, defaultEndDate, defaultLocation }: Props = $props();

	let startDate = $state<string>(
		defaultStartDate?.toISOString().split('T')[0] ?? new Date().toISOString().split('T')[0]
	);
	let endDate = $state<string>(
		defaultEndDate
			? defaultEndDate.toISOString().split('T')[0]
			: new Date(new Date().setDate(new Date().getDate() + 14)).toISOString().split('T')[0]
	);
	let location = $state<string>(defaultLocation ?? 'All Locations');

	let clientError = $state<string | null>(null);

	$effect(() => {
		if (startDate > endDate) {
			endDate = startDate;
		}
	});

	// Client-side validation function
	function validateDates(formData: FormData): string | null {
		const startDate = formData.get('startDate')?.toString();
		const endDate = formData.get('endDate')?.toString();

		function parseDate(date: string): Date {
			const [year, month, day] = date.split('-');
			const offset = new Date().getTimezoneOffset();
			return new Date(
				`${year}-${month}-${day}T00:00:00${offset > 0 ? '-' : '+'}${Math.floor(offset / 60)}:${Math.abs(offset % 60)}`
			);
		}

		if (!startDate || !endDate) {
			return 'Start date and end date are required';
		}

		const startDateObj = parseDate(startDate);
		const endDateObj = parseDate(endDate);
		const today = new Date();

		if (endDateObj < startDateObj) {
			return 'End date must be after start date';
		}

		if (startDateObj < today) {
			return 'Start date cannot be in the past';
		}

		const maxRange = new Date(startDateObj);
		maxRange.setMonth(maxRange.getMonth() + 3);
		if (endDateObj > maxRange) {
			return 'Search range cannot exceed 3 months';
		}

		return null;
	}

	function handleSubmit(event: SubmitEvent) {
		event.preventDefault();
		clientError = validateDates(new FormData(event.target as HTMLFormElement));

		if (clientError === null) {
			window.location.href = `/search?startDate=${startDate}&endDate=${endDate}&location=${location}`;
		}
	}
</script>

<div class="rounded-lg bg-white p-6 shadow-md">
	<h2 class="text-lg font-semibold">Search for Dates</h2>
	<form class="wrap mt-4 gap-4 space-y-6" onsubmit={handleSubmit}>
		<div class="flex flex-row flex-wrap gap-4">
			<div class="min-w-44 grow">
				<label for="location" class="mb-1 block text-sm font-medium text-gray-700">Location</label>
				<select
					id="location"
					name="location"
					class="w-full rounded-md border border-gray-300 px-4 py-2 focus:border-blue-500 focus:ring-blue-500"
					bind:value={location}
				>
					<option value="All Locations">All Locations</option>
				</select>
			</div>

			<div class="min-w-44 grow">
				<label for="start-date" class="mb-1 block text-sm font-medium text-gray-700"
					>Start Date</label
				>
				<input
					type="date"
					id="start-date"
					name="startDate"
					class="w-full rounded-md border border-gray-300 px-4 py-2 focus:border-blue-500 focus:ring-blue-500"
					bind:value={startDate}
					required
				/>
			</div>

			<div class="min-w-44 grow">
				<label for="end-date" class="mb-1 block text-sm font-medium text-gray-700">End Date</label>
				<input
					type="date"
					id="end-date"
					name="endDate"
					class="w-full rounded-md border border-gray-300 px-4 py-2 focus:border-blue-500 focus:ring-blue-500"
					bind:value={endDate}
					required
				/>
			</div>
		</div>

		<div class="flex justify-center">
			<button
				type="submit"
				class="rounded-md bg-blue-600 px-6 py-2.5 font-semibold text-white transition-colors duration-200 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
			>
				Search
			</button>
		</div>

		{#if clientError}
			<div class="rounded-md bg-red-50 p-4">
				<div class="flex">
					<div class="flex-shrink-0">
						<svg
							class="h-5 w-5 text-red-400"
							viewBox="0 0 20 20"
							fill="currentColor"
							aria-hidden="true"
						>
							<path
								fill-rule="evenodd"
								d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.28 7.22a.75.75 0 00-1.06 1.06L8.94 10l-1.72 1.72a.75.75 0 101.06 1.06L10 11.06l1.72 1.72a.75.75 0 101.06-1.06L11.06 10l1.72-1.72a.75.75 0 00-1.06-1.06L10 8.94 8.28 7.22z"
							/>
						</svg>
					</div>
					<div class="ml-3">
						<h3 class="text-sm font-medium text-red-800">
							{clientError}
						</h3>
					</div>
				</div>
			</div>
		{/if}
	</form>
</div>
