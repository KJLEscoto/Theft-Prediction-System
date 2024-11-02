<template>
<div class="m-2 w-auto h-auto">

  <!-- desktop view -->
  <UDropdown 
    v-model="isOpen" 
    :items="items" 
    :popper="{ placement: 'right', arrow: 'true', offsetDistance: 10 }" 
    :ui="{background: 'dark:bg-custom-950', width: 'w-auto', arrow: {background: 'dark:before:bg-custom-400'}}" 
    class="w-full border rounded-sm border-custom-600 lg:block hidden" >
      <div 
        v-if="!user.role || !['client', 'admin', 'superadmin'].includes(user.role)" 
        class="mx-auto w-auto">
          <UIcon class="animate-spin" name="i-heroicons-arrow-path-solid"/>
      </div>
      <div v-else class="w-auto flex justify-start items-center gap-2 p-4" >
        <div class="rounded-full bg-custom-400 dark:bg-custom-500 h-10 w-10 flex justify-center items-center">
          <img draggable="false" v-if="user.avatar" class="w-full h-full border-2 border-custom-400 rounded-full" :src="user.avatar">
          <span v-else class="font-bold text-2xl">{{ initial }}</span>
        </div>
        <div class="border-l border-custom-400 pl-2 w-auto">
          <p class="tracking-wide lg:truncate lg:max-w-[150px] max-w-full capitalize">{{ user.name }}</p>
          <p class="text-custom-500 dark:text-custom-400 font-semibold text-sm tracking-wider">{{ user.role }}</p>
        </div>
      </div>
  </UDropdown>

  <!-- mobile view -->
  <div class="w-full border rounded-sm border-custom-600 flex justify-between lg:hidden">
    <div class="w-auto flex justify-start items-center gap-2 p-4 cursor-pointer" 
      @click="viewProfile">
      <div 
        v-if="!user.role || !['client', 'admin', 'superadmin'].includes(user.role)" 
        class="mx-auto w-auto">
          <UIcon class="animate-spin" name="i-heroicons-arrow-path-solid"/>
      </div>
      <div v-else class="rounded-full bg-custom-400 dark:bg-custom-500 h-10 w-10 flex justify-center items-center">
        <img draggable="false" v-if="user.avatar" class="w-full h-full border-2 border-custom-400 rounded-full" :src="user.avatar">
        <span v-else class="font-bold text-2xl">{{ initial }}</span>
      </div>
      <div class="border-l border-custom-400 pl-2 w-auto">
        <p class="tracking-wide lg:truncate lg:max-w-[150px] max-w-full capitalize">{{ user.name }}</p>
        <p class="text-custom-500 dark:text-custom-400 font-semibold text-sm tracking-wider">{{ user.role }}</p>
      </div>
    </div>
    <UButton 
      class="bg-red-500 dark:bg-red-500 hover:bg-red-600 h-10 mr-5 my-auto dark:hover:bg-red-400 text-white dark:text-white rounded" 
      label="Logout" 
      icon="i-lucide-log-out"
      @click="handleLogout" />
  </div>
</div>
</template>

<script setup>
import { user, initial } from '~/assets/js/userLogged';
import { name, playSound } from '~/assets/js/sound'

const isOpen = ref(true)

const toast = useToast()

const handleLogout = () => {
  if (confirm("You would like to log out?") == true) {

  name.value = 'logoff_1'
  playSound()

  toast.add({
    title: 'Logout Successfully!',
    icon: 'i-lucide-log-out',
    timeout: 2000,
    ui: {
      background : 'dark:bg-orange-700 bg-orange-300', 
      progress: {
        background: 'dark:bg-white bg-orange-700 rounded-full'
      }, 
      ring: 'ring-1 ring-orange-700 dark:ring-custom-900',
      default: {
        closeButton: { 
          color: 'white',
        }
      },
      icon: 'text-custom-900'
    },
  })
  
  navigateTo('/auth')
  } else {
  console.log('Cancelled.')
  }
}

const viewProfile = () => {
  if (user.role === 'client') {
    navigateTo('/client/settings');
  } else if (user.role === 'admin' || user.role === 'superadmin') {
    navigateTo('/admin/settings');
  } else {
    alert('Error occured! Try Again.')
  }
};


const items = [
  [{
    label: 'View Profile',
    icon: 'i-lucide-circle-user-round',
    click: viewProfile
  },
  {
    label: 'Logout',
    icon: 'i-lucide-log-out',
    click: handleLogout
  }],
]

</script>