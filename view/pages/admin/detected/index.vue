<template>

  <UseHead title="Detected Motions - Admin"/>

  <div class="h-auto w-full p-5 flex flex-col gap-5">
    <h1 class="text-lg font-semibold text-custom-800 dark:text-white">List of Detected Motions (diria ang tanan notifications)</h1>
    <TableDetected />
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'sidebar'
})

</script>