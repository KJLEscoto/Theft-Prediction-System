
import { reactive } from 'vue';

export const motions = reactive([]); // Start with an empty array

// Initialize the motion object
const mapMotionData = (data) => {
  return {
    id: data.id,
    name: data.name,
    description: data.description,
    video_path: data.video_path,
    threshold: data.threshold,
    date_added: data.created_at,
    deleted_at: data.deleted_at
  };
};

export async function fetchMotions() {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/motions', {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`No data found in response: ${response.statusText}`);
    }

    const data = await response.json();
    // console.log('Fetched motion data:', data);
    
    // Clear existing motions (if needed)
    motions.splice(0, motions.length); 

    // Populate motions based on fetched data
    data.forEach(item => {
        motions.push(mapMotionData(item)); // Use push to add new motions
    });

  } catch (error) {
    console.error('Error fetching motions:', error.message);
  }
}
