<script setup lang="ts">
const colorMode = useColorMode()
const toggleText = computed(() => (isDark.value ? 'Turn Light' : 'Turn Dark'));
const isDark = computed({
  get () {
    return colorMode.value === 'dark'
  },
  set () {
    colorMode.preference = colorMode.value === 'dark' ? 'light' : 'dark'
  }
})
</script>
<template>
  <UTooltip 
    :text="toggleText" 
    :popper="{ arrow: true, placement: 'right' }" 
    :ui="{ background: 'dark:bg-custom-800 bg-custom-50', arrow: { background: 'dark:before:bg-custom-950 before:bg-custom-300'}}" >
    <ClientOnly>
      <UButton
        :icon="isDark ? 'i-heroicons-moon-20-solid' : 'i-heroicons-sun-20-solid'"
        color="gray"
        variant="ghost"
        aria-label="Theme"
        @click="isDark = !isDark"
        class="rounded-full dark:hover:bg-custom-800" />
      <template #fallback>
        <div class="w-8 h-8" />
      </template>
    </ClientOnly>  
  </UTooltip> 
</template>
