<template>
  <div class="lg:h-screen h-[90%] w-full rounded-lg p-5">
    <section
      v-if="props.isLive"
      class="flex items-center justify-center lg:h-full h-auto w-auto bg-black dark:bg-black relative"
    >
      <img
        :src="props.videoUrl"
        draggable="false"
        class="h-full w-full block border-none"
      />

      <div class="flex justify-between absolute bottom-0 w-full items-center">
        <section
          class="text-white dark:text-custom-300 w-auto h-auto py-1 px-2 text-sm cursor-default bg-custom-700 dark:bg-custom-800"
        >
          <h1 class="text-lg font-bold">{{ currentDate }}</h1>
          <p class="font-bold">{{ currentTime }}</p>
        </section>

        <section v-if="props.isLive" class="absolute right-4">
          <div
            class="flex justify-start gap-1 animate-pulse items-center bg-red-600 dark:bg-gray-900 rounded px-2 py-1 dark:border dark:border-red-500 text-white dark:text-red-500 cursor-default text-xs font-bold"
          >
            <UIcon name="i-lucide-radio" class="text-base" />
            <p>LIVE</p>
          </div>
        </section>
      </div>
    </section>

    <section
      v-else
      class="flex flex-col gap-3 items-center justify-center lg:h-full h-[500px] w-full cursor-default bg-black dark:bg-black"
    >
      <div class="text-red-500 grid justify-center">
        <UIcon class="w-auto h-10 m-auto" name="i-lucide-video-off" />
        <p class="text-xs tracking-wider font-bold">No Camera Available.</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  videoUrl: {
    type: String,
    required: true,
  },
  isLive: {
    type: Boolean,
    default: false,
  },
});

// For date and time
const currentDate = ref("");
const currentTime = ref("");

const updateDateTime = () => {
  const now = new Date();
  currentDate.value = now.toLocaleDateString();
  currentTime.value = now.toLocaleTimeString();
};

onMounted(() => {
  updateDateTime();
  setInterval(updateDateTime, 1000);
});
</script>
