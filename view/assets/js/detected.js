import { reactive } from "vue";
import { formatDate } from "./formatDate";

export const detected = reactive([]);

const mapNotificationData = (data) => {
  return {
    id: data.id,
    username: data.user.username,
    screenshot: data.screenshots,
    date_captured: formatDate(data.created_at),
    deleted_at: data.deleted_at,
    name: `${data.user.first_name} ${
      data.user.middle_initial ? data.user.middle_initial + ". " : ""
    }${data.user.last_name}`,
    motions: data.motions.map((motion) => ({
      id: motion.id,
      name: motion.name,
      threshold: motion.threshold,
      img: `/Snapshots/${motion.video_path}`,
    })),
  };
};

// Fetch all notifications
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

    // Clear existing notifications
    detected.splice(0, detected.length);

    // Populate notifications based on fetched data
    data.forEach((item) => {
      console.log("Mapping and pushing data:", item);
      detected.push(mapNotificationData(item));
    });
  } catch (error) {
    console.error("Error fetching detected:", error.message);
  }
}
