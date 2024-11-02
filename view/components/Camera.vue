<template>
    <div class="lg:h-full h-[90%] w-full  rounded-lg">

      <section 
        v-show="!camera" 
        class="flex flex-col gap-3 items-center justify-center h-full w-full cursor-default bg-custom-950 dark:bg-black">

        <div class="text-red-500 grid justify-center">
          <UIcon 
            class="w-auto h-10 m-auto" 
            name="i-lucide-video-off" />
          <p class="text-xs tracking-wider font-bold">
            No Camera Detected.
          </p>
        </div>

        <div class="cursor-default text-white flex gap-2 items-center">
          Choose Camera: 
          <USelect
            color="white"
            size="2xs"
            :options="options"
            placeholder="Select"
            v-model="selectedCamera"/>

            <div>
              <UButton 
                class="rounded"
                size="2xs"
                :label="save.label.value"
                :loading="save.bool.value" 
                :loading-icon="save.icon.value"
                @click="handleClick"/>
            </div>
        </div>


      </section>

      <section 
        v-show="camera" 
        class="flex items-center justify-center h-full w-full bg-custom-950 dark:bg-black relative">
      
        <img :src="videoFeedUrl" class="h-full w-full object-cover block border-none"/>

        <div class="flex justify-between absolute top-0 w-full items-center">
          <section class="text-white w-auto h-auto rounded-ss-sm rounded-br py-1 px-2 text-sm opacity-70 cursor-default bg-slate-700">
            <h1 class="text-lg font-semibold">{{ currentDate }}</h1>
            <p class="font-bold">{{ currentTime }}</p>
          </section>

          <section 
            v-if="isLive" 
            class="absolute right-4">

            <div class="flex justify-start gap-1 animate-pulse items-center bg-red-600 dark:bg-gray-900 rounded px-2 py-1 dark:border dark:border-red-500 text-white dark:text-red-500 cursor-default text-xs font-bold">
              <UIcon 
                name="i-lucide-radio" 
                class="text-base"/>
              <p>LIVE</p>
            </div>

          </section>
        </div>
      </section>

    </div>
</template>

<script setup lang="ts">

// for camera
const camera = ref(true);
const videoFeedUrl = ref('http://127.0.0.1:5000/video_feed') // URL of the Flask server

const props = defineProps({
  videoUrl: {
    type: String,
    required: true,
  },
  isLive: {
    type: Boolean,
    default: true
  }
});

const options = [
  {
    label: 'camera 1',
    value: 'camera 1 value hehe taena'
  },
  {
    label: 'camera 2',
    value: 'camera 2 value hehe kupal'
  },
]

const save = {
    label: ref('Save'),
    bool: ref(false),
    icon: ref('')
}

const selectedCamera = ref('');

const handleClick = () => {
  save.label.value = '';
  save.bool.value = true;
  save.icon.value = 'i-lucide-loader-circle'

  setTimeout(() => {
    save.label.value = 'Save';
    save.bool.value = false;
    console.log('selected camera:', selectedCamera.value) // here
    // camera.value = true;
  }, 1300);
};

// Watch for changes in videoUrl
watch(() => props.videoUrl, () => {
  videoFeedUrl.value = props.videoUrl;
});

// For date and time
const currentDate = ref('');
const currentTime = ref('');

const updateDateTime = () => {
  const now = new Date();
  currentDate.value = now.toLocaleDateString();
  currentTime.value = now.toLocaleTimeString();
};

onMounted(() => {
  updateDateTime();
  setInterval(updateDateTime, 1000); // Update every second
});
</script>