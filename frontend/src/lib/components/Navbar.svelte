<script lang="ts">
	import { page } from '$app/stores';
</script>

<nav class="sticky top-0 z-50 h-16 w-full border-b bg-white">
	<div class="mx-auto max-w-6xl px-4">
		<div class="flex h-16 items-center justify-between">
			<a href="/">
				<div class="flex items-center gap-2">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-8 w-8 text-blue-600"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
					>
						<path d="M4 19l16-16m-2 16l-4-4m-8-8l4 4" />
					</svg>
					<span class="text-xl font-bold text-gray-900">SkiPrice</span>
				</div>
			</a>
			<div class="flex items-center gap-6">
				<a href="/" class="text-gray-600 hover:text-gray-900">Home</a>
				<a href="/dates" class="text-gray-600 hover:text-gray-900">Calendar</a>
				<a href="/resorts" class="text-gray-600 hover:text-gray-900">Resorts</a>
			</div>
		</div>
	</div>
</nav>
