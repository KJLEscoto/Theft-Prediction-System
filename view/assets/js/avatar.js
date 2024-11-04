import { ref, watchEffect } from "vue";

const AVATAR_BASE_URL = "https://robohash.org/set_set3/bgset_bg1/";

const items = ref(120); // Reactive item count
const totalItems = computed(() => items.value);

/**
 * Generate an array of avatar URLs based on the current item count.
 * @returns {string[]} Array of avatar image URLs.
 */
function generateAvatars() {
  return Array.from(
    { length: items.value },
    (_, i) => `${AVATAR_BASE_URL}${i + 1}.png?size=1000x1000`
  );
}

const avatars = ref(generateAvatars());

// Watch items and update avatars accordingly
watchEffect(() => {
  avatars.value = generateAvatars();
});

/**
 * Get a specific avatar URL by index.
 * @param {number} index - The index of the avatar.
 * @returns {string|null} The avatar URL or null if out of bounds.
 */
function getSpecificAvatar(index) {
  if (index >= 0 && index < avatars.value.length) {
    return avatars.value[index]; // Return specific avatar URL
  }
  return null; // Handle out-of-bounds index
}

export async function fetchAvatars() {
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/avatars`, {
      method: "GET",
    });

    if (response) {
      const data = await response.json();
      items.value = data[0].avatar_count;
    }
  } catch (error) {
    console.error("Error fetching notifications:", error.message);
  }
}

export { items, avatars, totalItems, getSpecificAvatar };
