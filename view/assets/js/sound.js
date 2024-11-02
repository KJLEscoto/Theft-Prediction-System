import { ref, watch } from 'vue'

export const name = ref('');
let sound = null;

// Ensure Audio is only initialized on the client-side
watch(name, (newType) => {
    if (newType) {
      sound = new Audio(`/${newType}.mp3`); // Construct the correct file path
    }
});

// Export function to stop and reset the alert sound
export const stopSound = () => {
if (sound) {
    sound.pause();
    sound.currentTime = 0; // Reset audio to the start
}
};

// Export function to play the alert sound
export const playSound = () => {
    if (sound) {
        sound.play().catch((error) => {
        console.error('Audio play failed:', error);
    });
    }
};
