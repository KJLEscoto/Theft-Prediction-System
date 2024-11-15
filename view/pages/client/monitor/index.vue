<template>
  <UseHead title="Monitor - Client" />

  <div class="lg:h-screen h-[700px] w-full">
    <div
      class="h-screen flex items-center justify-center gap-1"
      v-if="
        !user.role || !['client', 'admin', 'superadmin'].includes(user.role)
      "
    >
      <UIcon
        class="animate-spin text-center"
        name="i-heroicons-arrow-path-solid"
      />
      In a moment...
    </div>

    <!-- diri isLive (true or false) false -->
    <div v-else>
      <Camera videoUrl="http://127.0.0.1:5000/video_feed" :isLive="isLive" />
    </div>

    <!-- <UButton
      label="Alert!"
      class="absolute top-52 right-10 rounded"
      @click="detectedBy"
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
import {
  detected as detectAlias,
  fetchAllNotifications,
} from "~/assets/js/detected";

const isLive = ref(true);

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
  console.log("This is your phone number", user.phone_number);
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
      contacts.value = data.map((contact) => `+63` + contact.contact_number); // Prefix +63 to contact numbers

      // Include user's phone number in the contacts list
      if (user.phone_number) {
        const formattedUserPhone = `+63${user.phone_number}`;
        contacts.value.push(formattedUserPhone);
      }

      console.log("Fetched contacts:", contacts.value);
    } else {
      // If no contacts found, add user's phone number with +63 prefix
      contacts.value = user.phone_number ? [`+63${user.phone_number}`] : [];
      console.log(
        "No contacts found, only user's phone added:",
        contacts.value
      );
    }
  } catch (error) {
    console.log("Error fetching contacts:", error);
  }
};

const detectedBy = async () => {
  await fetchAllNotifications();
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/notification/${
        detectAlias[detectAlias.length - 1].id
      }`,
      {
        method: "PUT",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("_token"), // Use 'Bearer' prefix for token
        },
      }
    );

    if (response) {
      console.log("success updated", response);
    }
  } catch (error) {
    console.log(error);
  }
};

const potential_detected = async () => {
  showToast();
  await detectedBy();
  await fetchContact();
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
    // console.log("hi", data);

    // calls the notification functions if the condiition is met
    if (latestEntryTime > lastCheckTime.value) {
      // sendSms(new Date(latestEntryTime))
      // console.log("hi");
      potential_detected();

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
