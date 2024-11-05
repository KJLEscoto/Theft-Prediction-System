<template>
  <UseHead title="Avatars - Admin" />

  <div class="h-auto w-full p-5 flex flex-col gap-5">
    <h1 class="text-lg font-semibold text-custom-800 dark:text-white">
      List of Avatars
    </h1>

    <span v-if="!user.role || !['client', 'admin', 'superadmin'].includes(user.role)">
      <UIcon class="animate-spin text-center" name="i-heroicons-arrow-path-solid"/>
      In a moment...
    </span>

    <div v-else class="flex flex-col gap-5 h-auto w-full">
      <h1 class="-mb-3">Total Avatars</h1>

      <!-- Increment/Decrement Section -->
      <section class="flex gap-1 items-center">
        <UButton
          @click="decrementDisplayCount"
          class="dark:text-white"
          icon="i-lucide-minus"
        />
        <UInput
          placeholder="0"
          isDisable.value="false"
          v-model.number="items"
          type="number"
          color="gray"
          class="w-auto"
          :ui="{
            rounded: 'rounded',
            color: {
              gray: {
                outline: 'dark:bg-custom-100 dark:text-custom-900 border-none',
              },
            },
          }"
        />

        <UButton
          @click="increment"
          class="dark:text-white"
          icon="i-lucide-plus"
        />
        <span>
          <UButton
            @click="onSubmit"
            :label="set.label.value"
            :loading-icon="set.icon.value"
            :loading="set.bool.value"
            class="flex justify-center w-full items-center rounded dark:text-white text-white bg-green-600 hover:bg-green-700 dark:bg-green-700 hover:dark:bg-green-800"
            type="submit"
          />
        </span>
      </section>

      <!-- Avatars Display Section -->
      <div
        class="flex flex-wrap gap-5 p-5 bg-white dark:bg-custom-800 rounded justify-center m-auto w-full max-h-[70vh] overflow-y-scroll"
      >
        <span
          v-if="avatars.length"
          v-for="(imgSrc, index) in avatars"
          :key="index"
        >
          <img
            class="w-24 h-24 border border-red-600 dark:border-red-800"
            draggable="false"
            :src="imgSrc"
            alt="avatar image"
          />
        </span>
        <div v-else class="text-center text-custom-800 dark:text-white">
          No items.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { items, avatars, totalItems, fetchAvatars } from "~/assets/js/avatar";
import type { FormSubmitEvent } from "#ui/types";
import { name, playSound } from "~/assets/js/sound";
import { user } from "~/assets/js/userLogged";

definePageMeta({
  layout: "sidebar",
});

// const isDisabled = ref(true);

const set = {
  bool: ref(false),
  label: ref("Set"),
  icon: ref(""),
};

function increment() {
  items.value++;
  // isDisabled.value = false;
}

function decrementDisplayCount() {
  if (items.value > 0) {
    items.value--;
  }
  // isDisabled.value = false;
}

async function onSubmit(event: FormSubmitEvent<any>) {
  event.preventDefault(); // Prevent the default form submission, if necessary
  console.log("Typed number in input box:", totalItems.value);
  const params = {
    avatar_count: items.value,
  };
  try {
    const response = await $fetch(`http://127.0.0.1:8000/api/avatars/1`, {
      method: "PUT",
      body: params,
    });

    if (response) {
      console.log(response);

      const toast = useToast();
      name.value = "success_1";

      set.bool.value = true;
      set.icon.value = "i-lucide-loader-circle";
      set.label.value = "";

      setTimeout(() => {
        playSound();

        toast.add({
          title: "Avatar Set Successfully!",
          icon: "i-lucide-smile-plus",
          timeout: 2000,
          ui: {
            background: "dark:bg-green-700 bg-green-300",
            progress: {
              background: "dark:bg-white bg-green-700 rounded-full",
            },
            ring: "ring-1 ring-green-700 dark:ring-custom-900",
            default: {
              closeButton: {
                color: "white",
              },
            },
            icon: "text-custom-900",
          },
        });

        set.label.value = "Set";
        set.bool.value = false;
        navigateTo(`/admin/avatars`);
      }, 800);
      // isDisabled.value = true;
    }
  } catch {}
}

onMounted(() => {
  fetchAvatars();
});
</script>
