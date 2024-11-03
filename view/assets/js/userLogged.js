import { reactive, ref, computed } from "vue";
import { avatars, getSpecificAvatar } from "~/assets/js/avatar"; // Assuming avatar array is coming from this file

// Define a function to fetch a specific avatar by index
export function fetchSpecificAvatar(index) {
  return getSpecificAvatar(index); // Call the imported function and return the result
}

// Reactive user object with default properties
export const user = reactive({
  first_name: "",
  last_name: "",
  middle_initial: "",
  gender: "",
  phone_number: "",
  email: "",
  role: "",
  status: "",
  username: "",
  password: "",
  avatar: ref(fetchSpecificAvatar(1)), // Default to the first avatar
  created_at: "",
  updated_at: "",

  get name() {
    return `${this.first_name} ${
      this.middle_initial ? this.middle_initial + ". " : ""
    }${this.last_name}`;
  },
});

// Allow previewAvatar to be either a string (URL) or null
export const previewAvatar = ref(null); // Set to null initially

export function setPreviewAvatar(selectedAvatar) {
  previewAvatar.value = selectedAvatar; // Assign the selected avatar (string)
}

// Fetch user data from the API and update the reactive state
export async function fetchUser() {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/user`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("_token"), // Use 'Bearer' prefix for token
      },
    });
    if (response.ok) {
      const data = await response.json();
      // Update user properties with the fetched data
      user.first_name = data.first_name;
      user.last_name = data.last_name;
      user.middle_initial = data.middle_initial;
      user.gender = data.gender;
      user.password = data.password;
      user.phone_number = data.phone_number;
      user.avatar = fetchSpecificAvatar(data.avatar); // Fetch avatar based on index
      user.email = data.email;
      user.role = data.role || user.role;
      user.status = data.status || user.status;
      user.username = data.username || user.username;
      user.created_at = data.created_at || user.created_at;
      user.updated_at = data.updated_at || user.updated_at;

      // Set previewAvatar to null initially to show the user.avatar first
      previewAvatar.value = null;
    } else {
      console.error("No data found in response:", response);
    }
  } catch (error) {
    console.log("dili okay ang response");
    console.error("Error fetching user:", error);
    if (error.response) {
      console.error("Error response:", error.response);
    } else {
      console.error("Network error");
    }
  }
}

// Compute the user's initial for display purposes
export const initial = computed(() => user.name.charAt(0).toUpperCase());
