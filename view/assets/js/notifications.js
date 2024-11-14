import { reactive } from "vue";
import { formatDate } from "./formatDate";

export const notifications = reactive([]); // Start with an empty array

// Map notification data including motions
const mapNotificationData = (data) => {
  return {
    date_captured: formatDate(data.created_at),
    deleted_at: data.deleted_at,
    username: data.user.username,
    name: `${data.user.first_name} ${
      data.user.middle_initial ? data.user.middle_initial + ". " : ""
    }${data.user.last_name}`,
    motions: data.motions.map((motion) => ({
      name: motion.name,
      img: `/Snapshots/${motion.video_path}`, // Assuming this path leads to a screenshot or relevant image
      threshold: motion.threshold,
    })),
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

    // Clear existing notifications
    notifications.splice(0, notifications.length);

    // Populate notifications based on fetched data
    data.forEach((item) => {
      notifications.push(mapNotificationData(item));
    });
  } catch (error) {
    console.error("Error fetching notifications:", error.message);
  }
}
