<template>
  <div class="h-auto w-full relative">
    <ToggleDarkMode class="fixed lg:top-20 z-50 top-5 left-5 lg:left-20 duration-200" />
    <div class="lg:grid-cols-2 grid-cols-1 lg:grid flex flex-col-reverse lg:h-screen h-auto w-auto lg:gap-20 gap-10 lg:p-20 p-16">
      <section class="m-auto">
        <div class="flex items-center gap-2">
          <img 
            class="w-14 h-14" 
            src="/icon.png" 
            alt="icon">
          <h1 class="font-bold cursor-default lg:text-4xl text-3xl lg:text-start text-center">Empower Your Security</h1>
        </div>
        <p class="mt-5 cursor-default lg:text-start text-justify text-gray-700 dark:text-gray-400">
          Protect what matters with <strong>AI-powered prediction</strong>. 
          The security surveillance system should be more than just cameras!
        </p>
        <div class="flex lg:justify-start justify-center mt-10">
          <UButton 
            class="px-12 py-4 rounded-full dark:text-custom-100 dark:bg-custom-600 hover:dark:bg-custom-600/75"
            icon="i-lucide-cctv" 
            label="Start Monitoring"
            @click="handleClick"
            :loading="start.bool.value" 
            :loading-icon="start.icon.value" />
        </div>
      </section>
      <section class="m-auto">
        <img 
          src="/assets/img/cctv-animate.gif" 
          alt="cctv"
          class="shadow-md lg:scale-125 scale-100 border-8 rounded-full border-custom-500 dark:border-custom-300">
      </section>

      <!-- display all avatars -->
      <!-- <div v-for="(avatarUrl, index) in avatars" :key="index">
        <img class="w-20 h-20 border rounded-full bg-custom-400" :src="avatarUrl">
      </div> -->

      <!-- selected avatar -->
      <!-- <img class="w-20 h-20 border rounded-full bg-custom-400" :src="avatars[0]"> -->

    </div>
  </div>

</template>

<script setup>
import { name, playSound } from '~/assets/js/sound'

const start = {
    bool: ref(false),
    icon: ref('')
}

name.value = 'start_1'

const handleClick = () => {
  start.bool.value = true;
  start.icon.value = 'i-lucide-loader-circle'

  playSound()

  setTimeout(() => {
    navigateTo('/auth');
    start.bool.value = false;
  }, 2300);
};

</script>