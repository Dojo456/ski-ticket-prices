export function parseDateIgnoreTZ(date: string) {
	const timezoneOffset = new Date().getTimezoneOffset();
	// Convert offset to hours and minutes
	const hours = Math.floor(Math.abs(timezoneOffset) / 60)
		.toString()
		.padStart(2, '0');
	const minutes = (Math.abs(timezoneOffset) % 60).toString().padStart(2, '0');
	// Create offset string with correct sign
	const offsetStr = `${timezoneOffset <= 0 ? '+' : '-'}${hours}:${minutes}`;

	return new Date(date + 'T00:00:00' + offsetStr);
}
