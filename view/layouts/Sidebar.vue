<template>
  <div class="lg:flex grid items-start w-full h-auto ">
    <section class="grid inset-y-0 left-0 h-auto z-50">
      <Sidebar />
    </section>
    <section class="w-full h-auto lg:ml-64 ml-0 mt-20 lg:mt-0">
      <slot />
    </section>
  </div>
</template>
