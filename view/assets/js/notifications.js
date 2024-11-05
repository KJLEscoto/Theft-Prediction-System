import { reactive } from "vue";
import { formatDate } from "./formatDate";

export const notifications = reactive([]); // Start with an empty array

// Initialize the motion object
const mapNotificationData = (data) => {
  return {
    motion_detected: data.motion.name,
    username: data.user.username,
    description: data.motion.description,
    screenshot: data.screenshots,
    threshold: data.motion.threshold,
    date_captured: formatDate(data.created_at),
    deleted_at: data.deleted_at,
    name: `${data.user.first_name} ${
      data.user.middle_initial ? data.user.middle_initial + ". " : ""
    }${data.user.last_name}`,
  };
};

export async function fetchNotifications(username) {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/notification/${username}`,
      {
        method: "GET",
      }
    );

    if (!response.ok) {
      throw new Error(`No data found in response: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Fetched notifications data:", data);

    // Clear existing notifications (if needed)
    notifications.splice(0, notifications.length);

    // Populate notifications based on fetched data
    data.forEach((item) => {
      notifications.push(mapNotificationData(item)); // Use push to add new notifications
    });
  } catch (error) {
    console.error("Error fetching notifications:", error.message);
  }
}
