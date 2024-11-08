import { reactive } from "vue";
import { formatDate } from "./formatDate";

export const detected = reactive([]);

const mapNotificationData = (data) => {
  return {
    id: data.id,
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

// fetch all notifications
export async function fetchAllNotifications() {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/notifications`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("_token"), // Use 'Bearer' prefix for token
      },
    });
    if (!response.ok) {
      throw new Error(`No data found in response: ${response.statusText}`);
    }

    const data = await response.json();
    console.log("Fetched user data:", data);
    // Clear existing notifications (if needed)
    detected.splice(0, detected.length);

    // Populate notifications based on fetched data
    data.forEach((item) => {
      console.log("pushing: ", item);
      detected.push(mapNotificationData(item)); // Use push to add new notifications
    });
  } catch (error) {
    console.error("Error fetching notifications:", error.message);
  }
}
