export function formatDate(dateString) {
  const date = new Date(dateString);

  const options = {
    timeZone: "UTC", // Ensure the date is interpreted in UTC
    month: "short",
    day: "2-digit",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
    hour12: true,
  };

  return date.toLocaleDateString("en-US", options).replace(",", "");
}
