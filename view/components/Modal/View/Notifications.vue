<template>
  <UModal
    prevent-close
    :ui="{
      background: 'bg-custom-50 dark:bg-custom-900',
      rounded: 'rounded',
    }"
  >
    <div class="h-auto w-full p-7 flex flex-col gap-3">
      <!-- Header -->
      <section class="flex justify-between items-end">
        <h1 class="text-lg font-semibold text-red-500">
          POTENTIAL THEFT DETECTED
        </h1>
        <UButton
          icon="i-lucide-x"
          @click="closeModal"
          class="flex justify-center items-center text-sm rounded-full dark:bg-red-600 dark:hover:bg-red-600/75 bg-red-600 hover:bg-red-600/75 dark:text-custom-100"
          size="2xs"
        />
      </section>

      <hr class="border-custom-300 dark:border-custom-700" />

      <!-- Notification Details -->
      <section class="flex flex-col gap-1">
        <!-- <h1 class="font-medium">
          <span class="font-bold capitalize text-red-500"
            >POTENTIAL THEFT DETECTED</span
          >
        </h1> -->

        <div v-if="user.role == 'superadmin' || user.role == 'admin'">
          <p class="font-medium text-sm dark:opacity-50 -mb-1">Detected by:</p>      
          <h1 class="dark:opacity-70 text-lg font-bold">
            <span class="truncate capitalize">{{ notification.name }}</span> | {{ notification.username }}
          </h1>
        </div>


        <!-- <p class="text-sm font-medium">
          Description:
          <span class="dark:text-custom-300 text-custom-800 font-normal">{{
            notification.description
          }}</span>
        </p> -->

        <!-- <p class="text-sm font-medium">
          Threshold:
          <span
            v-if="notification.threshold <= 74"
            class="text-green-500 font-extrabold"
            >{{ notification.threshold }}%</span
          >
          <span v-else class="text-red-500 font-extrabold"
            >{{ notification.threshold }}%</span
          >
        </p> -->

        <div
          class="flex justify-center items-center mt-2 w-full bg-white dark:bg-custom-950 border dark:border-custom-700"
        >
          <UCarousel 
            v-if="notification.screenshot" 
            v-slot="{ item }" 
            :items="items" 
            :ui="{ item: 'basis-full' }" 
            class="overflow-hidden w-full h-auto bg-white dark:bg-custom-950 mx-auto relative"
            :prev-button="{
              color: 'gray',
              icon: 'i-heroicons-arrow-left-20-solid',
            }"
            :next-button="{
              color: 'gray',
              icon: 'i-heroicons-arrow-right-20-solid',
            }"
            arrows>
            <img :src="item.img" class="w-[70%] h-auto mx-auto" draggable="false">
            <div class="absolute w-full text-center text-xs font-semibold py-1 px-3 bottom-0">
              <span class="bg-white dark:bg-custom-950 p-1 px-3 capitalize rounded-t">{{ item.name }} - 
                <span
                  v-if="item.threshold <= 74.99"
                  class="text-green-500 font-extrabold"
                  >{{ item.threshold }}%</span
                >
                <span v-else class="text-red-500 font-extrabold"
                  >{{ item.threshold }}%</span
                >
              </span>
            </div>
          </UCarousel>

          <div
            v-else
            class="w-auto h-[250px] font-bold text-sm flex justify-center items-center text-red-700"
          >
            No screenshot available.
          </div>
        </div>

        <span
          class="text-xs text-custom-400 font-semibold flex gap-1 items-center justify-center"
        >
          Date Captured:
          <span class="font-bold">
            {{ formatDate(notification.date_captured) || "--" }}</span
          >
        </span>
      </section>
    </div>
  </UModal>
</template>

<script setup>
import { formatDate } from "~/assets/js/formatDate";
import { user } from "~/assets/js/userLogged";

// Receive notification data as a prop
const props = defineProps({
  notification: {
    type: Object,
    required: true,
  },
});

const items = [
  {
    name: 'looking around',
    img: 'https://picsum.photos/1920/1080?random=1',
    threshold: '88.00'
  },
  {
    name: 'reaching',
    img: 'https://picsum.photos/1920/1080?random=2',
    threshold: '73.97'
  },
  {
    name: 'concealing',
    img: 'https://picsum.photos/1920/1080?random=3',
    threshold: '88.00'
  }
]

const modal = useModal();

const closeModal = () => {
  modal.close();
};
</script>
