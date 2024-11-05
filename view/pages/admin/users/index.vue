<template>

  <UseHead title="Users - Admin"/>

  <div class="h-auto w-full flex flex-col gap-5 p-5">
    <header class="flex justify-between">
      <h1 class="text-lg font-semibold text-custom-800 dark:text-white cursor-default">List of Users</h1>

      <div class="block sm:hidden">
        <UButton 
          label="Add User" 
          icon="i-lucide-user-round-plus"
          class="dark:text-custom-200 bg-custom-400 hover:bg-custom-500 dark:bg-custom-700 dark:hover:bg-custom-800 rounded p-2"
          to="/admin/users/create" 
          size="xs" />
      </div>
    </header>

    <span v-if="!user.role || !['client', 'admin', 'superadmin'].includes(user.role)">
      <UIcon class="animate-spin text-center" name="i-heroicons-arrow-path-solid"/>
      In a moment...
    </span>
    
    <span v-else>
      <TableUsers />
    </span>
  </div>
</template>

<script setup>
import { user } from '~/assets/js/userLogged';


definePageMeta({
  layout: 'sidebar'
})

</script>
