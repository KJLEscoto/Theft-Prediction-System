<template>
  <UseHead title="Detected Motions - Admin" />

  <div class="h-auto w-full p-5 flex flex-col gap-5">
    <h1 class="text-lg font-semibold text-custom-800 dark:text-white">
      List of Potential Theft
    </h1>

    <span v-if="!user.role || !['client', 'admin', 'superadmin'].includes(user.role)">
      <UIcon class="animate-spin text-center" name="i-heroicons-arrow-path-solid"/>
      In a moment...
    </span>

    <span v-else>
      <TableDetected />
    </span>
  </div>
</template>

<script setup>
import { user } from '~/assets/js/userLogged';


definePageMeta({
  layout: "sidebar",
});
</script>
