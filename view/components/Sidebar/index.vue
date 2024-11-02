<script setup>
import { user } from '~/assets/js/userLogged';

const open = ref(false);

const loading = ref(true)

const loadUser = async () => {
  await fetchUser();
};

onMounted(() => {
  if (!localStorage.getItem('_token')) {
    navigateTo(`/auth`);
  } else {
    loadUser(); // Load user data when the component mounts
  }
  loading.value = false
});
</script>

<template>
<div class="relative">

  <!--mobile-->
  <div class="fixed top-0 left-0 z-30 w-full bg-custom-100 dark:bg-custom-900">
    <div 
      v-show="!open" 
      class="flex shadow lg:hidden items-center justify-between h-full p-5 tracking-wide border-b border-custom-500" >
      <div class="flex gap-3 items-center justify-start">
        <div class="font-semibold text-xl max-w-52">
          <p class="truncate">
            Hi, 
            <span v-if="!user.role || !['client', 'admin', 'superadmin'].includes(user.role)">
              <UIcon class="animate-spin" name="i-heroicons-arrow-path-solid"/>
            </span>
            <span v-else>{{ user.username }}!</span> 
          </p>
        </div>

        <ToggleDarkMode />
      </div>

      <UIcon 
        name="i-lucide-align-justify" 
        class="cursor-pointer left-2 top-2 w-auto h-7 text-custom-600 hover:text-custom-500" 
        @click="open = true" />
    </div>

    <div 
      v-if="open" 
      class="border-b border-custom-500 shadow-xl lg:hidden block" >
      <SidebarMenu @click="open = false"/>
      <UIcon 
        name="i-lucide-x" 
        class="cursor-pointer right-5 top-5 w-auto h-7 absolute text-red-600 hover:text-red-500" 
        @click="open = false" />

      <div class="border-t border-custom-500">
        <UserItem 
          class="shadow-md" 
          @click="open = false" />
      </div>

    </div>

  </div>

  <!--desktop-->
  <div class="lg:flex hidden fixed bg-custom-100 border-custom-500 dark:bg-custom-900 h-screen border-r w-[250px] z-10 flex-col justify-between">
    <SidebarMenu />
    <div class="border-t border-custom-500">
      <UserItem /> 
    </div>
  </div>
</div>
</template>
