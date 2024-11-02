<script setup>
defineProps(['error', 'router']);

const router = useRouter();

const goBack = () => {
  router.go(-1); 
};
</script>

<template>

  <UseHead title="Error"/>

<div class="h-screen w-full">
  <div class="h-screen flex justify-center items-center">
    <div class="flex items-center justify-center h-auto w-full cursor-default p-10 m-auto">
      <div class="tracking-wider text-center">
        <img src="~/assets/img/error-animate.gif" alt="error" class="w-auto h-40 m-auto bg-[#cbd2d7] rounded-full mb-3 border-4">  
        <p class="text-5xl mb-1 font-bold">{{ error.statusCode }}</p>
        <p class="text-2xl mb-1 font-semibold">Oops, Access denied :( </p>
        <p class="text-sm">{{ error.message }}</p>
        <div class="flex justify-center">
          <UButton label="Go back" icon="i-lucide-move-left" class="rounded-full bg-[#79838c] py-4 px-8 mt-5 font-bold dark:text-white" @click="goBack"/>
        </div>
      </div>
    </div>
  </div>
</div>
</template>
