
// Formats minutes as "X hrs X mins", leaving out any part that is 0.
export function formatTime(totalMinutes) {
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;

  if (hours === 0) return minutes > 1 ? `${minutes} mins` : `${minutes} min`;
  if (minutes === 0) return hours > 1 ? `${hours} hrs` : `${hours} hr`;
  let details = `${hours} hr`;
  if (hours > 1) details += `s`;
  details += ` ${minutes} min`;
  if (minutes > 1) details += `s`;
  return details;
}
