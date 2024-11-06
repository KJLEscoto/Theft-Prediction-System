<template>
  <UseHead title="Monitor - Client" />

  <div class="lg:h-screen h-[700px] w-full p-5">
    <span
      v-if="
        !user.role || !['client', 'admin', 'superadmin'].includes(user.role)
      "
    >
      <UIcon
        class="animate-spin text-center"
        name="i-heroicons-arrow-path-solid"
      />
      In a moment...
    </span>

    <span v-else>
      <Camera videoUrl="http://127.0.0.1:5000/video_feed" :isLive="true" />
    </span>

    <!-- <UButton
      label="Alert!"
      class="absolute top-52 right-10 rounded"
      @click="showToast"
    /> -->
  </div>
</template>

<script setup>
definePageMeta({
  layout: "sidebar",
});

import { name, playSound, stopSound } from "~/assets/js/sound";
import { fetchAvatars } from "~/assets/js/avatar";
import { user } from "~/assets/js/userLogged";
import { ref } from "vue";

// for toast
const toast = useToast();
const lastCheckTime = ref(null);

const onClick = () => {
  navigateTo("/client/notifications");
  stopSound();
  toast.clear();
};

const contacts = ref([]);

const fetchContact = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/user/contact/enabled",
      {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("_token"),
        },
      }
    );
    const data = await response.json();

    // Check if data is an array and contains contact information
    if (Array.isArray(data) && data.length) {
      contacts.value = data.map((contact) => `+63` + contact.contact_number); // Save only contact numbers
      console.log("Fetched contacts:", contacts.value);
    } else {
      console.log("No contacts found.");
    }
  } catch (error) {
    console.log("Error fetching contacts:", error);
  }
};

const detected = async () => {
  showToast();

  await fetchContact();

  console.log("kani na jud final", contacts.value);
  const params = {
    phone_numbers: contacts.value,
    message: "Potential Theft Detected",
  };
  try {
    const response = await fetch("http://127.0.0.1:8000/api/alert-sms", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("_token"),
      },
      body: JSON.stringify(params),
    });

    if (response.ok) {
      const data = await response.json();
      console.log("successful, na send na", data);
    } else {
      console.log("Error:", response.statusText);
    }
  } catch (error) {
    console.log("error sa pag send sa message", error);
  }
};

const showToast = async () => {
  playSound();
  toast.add({
    title: "Motion Detected!",
    click: onClick,
    icon: "i-lucide-triangle-alert",
    ui: {
      background: "dark:bg-red-700 bg-red-300",
      progress: {
        background: "dark:bg-white bg-red-700 rounded-full",
      },
      ring: "ring-1 ring-red-700 dark:ring-custom-900",
      default: {
        closeButton: {
          color: "white",
        },
      },
      icon: "text-custom-900",
    },
  });
};

// checks for any detected motion from the database
const checkForNewEntries = async () => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/notifications", {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("_token"), // Use 'Bearer' prefix for token
      },
    });

    const data = await response.json();
    const latestEntry = data.length ? data[data.length - 1] : null;
    const latestEntryTime = new Date(latestEntry.created_at).toISOString();

    // calls the notification functions if the condiition is met
    if (latestEntryTime > lastCheckTime.value) {
      // sendSms(new Date(latestEntryTime))
      detected();

      // updates the latest detected motion
      lastCheckTime.value = latestEntryTime;
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

// kicks start the app on mount
onMounted(async () => {
  name.value = "alert_1";
  fetchAvatars();
  await fetchContact();
  console.log("dara ang contacts", contacts.value);
  try {
    // fetches the latest entry time on mount
    const response = await fetch("http://127.0.0.1:8000/api/notifications", {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("_token"), // Use 'Bearer' prefix for token
      },
    });
    const data = await response.json();
    const latestEntry = data[data.length - 1];

    // initializes the variable lastCheckTime
    lastCheckTime.value = new Date(latestEntry.created_at).toISOString();

    // loop logic to monitor the motions
    setInterval(checkForNewEntries, 5000); // Check every seconds
  } catch (error) {
    console.error("Error initializing last check time:", error);
  }
});
</script>
