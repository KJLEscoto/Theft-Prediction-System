<script setup>
import { ref, computed, watch } from 'vue';
import { user, fetchUser } from '~/assets/js/userLogged';

const loading = ref(true)

const loadUser = async () => {
  await fetchUser();
};

onMounted(() => {
  loadUser();
  loading.value = false
});

const route = useRoute();

const clientItems = ref([
  { title: 'Monitor', path: '/client/monitor', icon: 'i-lucide-monitor' },
  { title: 'Notifications', path: '/client/notifications', icon: 'i-lucide-bell' },
  { title: 'Settings', path: '/client/settings', icon: 'i-lucide-settings-2' },
]);

const adminItems = ref([
  { title: 'Dashboard', path: '/admin/dashboard', icon: 'i-lucide-layout-dashboard' },
  { title: 'Motions', path: '/admin/motions', icon: 'i-lucide-hand' },
  { title: 'Detected', path: '/admin/detected', icon: 'i-lucide-triangle-alert' },
  { title: 'Users', path: '/admin/users', icon: 'i-lucide-users-round' },
  { title: 'Avatars', path: '/admin/avatars', icon: 'i-lucide-smile' },
  { title: 'Settings', path: '/admin/settings', icon: 'i-lucide-settings' },
]);

// Computed property for menu items based on user role
const items = computed(() => {
  return user.role === 'admin' || user.role === 'superadmin' ? adminItems.value : clientItems.value;
});

// Set the active item based on the current route path
const activeItem = ref(items.value.find(item => route.path.startsWith(item.path)));

// Watch for changes in route.path or items
watch(
  () => [route.path, items.value],
  () => {
    activeItem.value = items.value.find(item => route.path.startsWith(item.path));
  },
  { immediate: true } // Ensures it runs initially as well
);
</script>

<template>
<div class="w-full tracking-wide">
  <header class="p-5 text-xl border-custom-500 border-b flex lg:gap-0 gap-3 items-center lg:justify-between justify-start ">
    <div class="font-semibold max-w-40">
      <p class="truncate">
        Hi, 
        <span v-if="!user.role || !['client', 'admin', 'superadmin'].includes(user.role)">
          <UIcon class="animate-spin" name="i-heroicons-arrow-path-solid"/>
        </span>
        <span v-else>{{ user.username }}!</span> 
      </p>
    </div>

    <ToggleDarkMode class="block" :popper="{ placement: 'right', arrow: true }" />
  </header>

  <section class="grow overflow-y-auto lg:max-h-[79vh] max-h-[30vh] w-auto">

    <div v-if="!user.role || !['client', 'admin', 'superadmin'].includes(user.role)">
      <div class="text-center p-10">
        <UIcon class="animate-spin" name="i-heroicons-arrow-path-solid"/>
        <p>Loading...</p>
      </div>
    </div>

    <!-- v-else  -->
    <div v-else class="grid gap-2 w-full p-5">
      <nuxt-link
        :to="item.path"
        v-for="(item, index) in items"
        :key="index"
        class="flex gap-2 items-center px-5 dark:hover:bg-custom-600 hover:bg-white py-2 transition cursor-pointer rounded-sm relative"
        :class="[activeItem && activeItem.path === item.path ? 'bg-custom-200 dark:bg-custom-700' : '']"
      >
        <UIcon :name="item.icon" class="text-lg" />
        <label>{{ item.title }}</label>
      </nuxt-link>
    </div>
  </section>
</div>
</template>
