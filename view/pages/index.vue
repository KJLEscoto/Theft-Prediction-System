<template>
  <div class="h-auto w-full relative">
    <ToggleDarkMode class="fixed lg:top-20 z-50 top-5 left-5 lg:left-20 duration-200" />
    <div class="lg:h-screen w-full h-auto flex flex-col items-center justify-center text-center gap-5">

      <img class="-mb-10 rounded-full w-[350px] h-auto" draggable="false" src="/cypher-logo-nobg.png" alt="logo">
      
      <h1 class=" font-extrabold cursor-default lg:text-4xl text-3xl">THEFT PREDICTION</h1>
    
      <p class="cursor-default text-gray-700 dark:text-gray-400">
        Protect what matters with <strong>AI-powered prediction</strong>. <br>
        The security surveillance system should be more than just cameras!
      </p>

      <div class="mt-5">          
        <UButton 
          class="px-12 py-4 rounded-full dark:text-custom-100 dark:bg-custom-600 hover:dark:bg-custom-600/75"
          icon="i-lucide-cctv" 
          label="Start Monitoring"
          @click="handleClick"
          :loading="start.bool.value" 
          :loading-icon="start.icon.value" />
      </div>

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