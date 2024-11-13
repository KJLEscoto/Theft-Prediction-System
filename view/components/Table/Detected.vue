<template>
  <section class="items-center grid gap-5">
    <div
      class="flex sm:gap-0 gap-5 sm:flex-row flex-col-reverse sm:justify-between justify-center"
    >
      <!-- Search Input -->
      <div class="flex gap-1 justify-start items-end">
        <UInput
          v-model="q"
          name="q"
          placeholder="Search..."
          icon="i-heroicons-magnifying-glass-20-solid"
          autocomplete="off"
          color="gray"
          size="sm"
          :ui="{
            rounded: 'rounded',
            color: {
              gray: { outline: 'dark:bg-custom-100 dark:text-custom-900' },
            },
            icon: { trailing: { pointer: '' } },
          }"
          class="w-full sm:w-auto sm:-mb-0 -mb-5"
        >
          <template #trailing>
            <UButton
              v-show="q !== ''"
              color="gray"
              variant="link"
              icon="i-heroicons-x-mark-20-solid"
              :padded="false"
              @click="q = ''"
              class="hover:text-red-400 dark:hover:text-red-600 text-red-700 dark:text-red-400"
            />
          </template>
        </UInput>
      </div>
      <!-- Pagination -->
      <UPagination
        :model-value="currentPage"
        :page-count="pageCount"
        :total="total"
        :ui="{
          color: 'gray',
          wrapper: 'flex items-center gap-1',
          rounded: '!rounded-full min-w-[30px] justify-center',
          default: {
            activeButton: {
              variant: 'outline',
            },
          },
        }"
        @update:model-value="updatePage"
        class="flex justify-center"
      />
    </div>

    <!-- Motion Table -->
    <UTable
      :columns="tableHeaders"
      :rows="paginatedData"
      sort-asc-icon="i-heroicons-arrow-up"
      sort-desc-icon="i-heroicons-arrow-down"
      class="max-h-[70vh] max-w-full overflow-auto border rounded border-custom-300 dark:border-custom-800"
      :ui="{
        thead:
          'sticky top-0 z-10 dark:bg-custom-700 bg-custom-300 cursor-default',
        tbody: 'bg-custom-100 dark:bg-custom-950',
      }"
    >
      <!-- Custom Template for Row Index -->
      <template #id-data="{ index }">
        <span>{{ (currentPage - 1) * pageCount + index + 1 }}</span>
      </template>

      <!-- Custom Template for Actions -->
      <template #action-data="{ row }">
        <div class="flex justify-start gap-2">
          <UTooltip text="View" :popper="{ arrow: true, placement: 'bottom' }">
            <UIcon
              name="i-lucide-eye"
              class="text-xl hover:opacity-50 text-blue-500"
              @click="viewAction(row)"
            />
          </UTooltip>
          <!-- <UTooltip text="Delete" :popper="{ arrow: true, placement: 'bottom' }">
            <UIcon 
              name="i-lucide-trash-2" 
              class="text-xl hover:opacity-50 text-red-500" 
              @click="deleteAction(row)" />
          </UTooltip> -->
        </div>
      </template>
    </UTable>

    <!-- Pagination -->
    <div class="flex justify-center">
      <span class="text-xs">
        Showing
        <span class="font-medium">{{ startItem }}</span>
        -
        <span class="font-medium">{{ endItem }}</span>
        of
        <span class="font-medium">{{ total }}</span>
        results
      </span>
    </div>
  </section>
</template>

<script setup>
// Imports
import { ModalViewNotifications } from "#components";
import { detected, fetchAllNotifications } from "~/assets/js/detected";

// Reactive Data
const currentPage = ref(1);
const pageCount = ref(20);
const q = ref("");

// Table Headers
const tableHeaders = [
  { key: "id", label: "#" },
  // { key: "motion_detected", label: "Motion" },
  { key: "username", label: "Detected By" },
  { key: "date_captured", label: "Date" },
  { key: "action", label: "Action" },
];

// Filtered and Paginated Data
const filteredRows = computed(() => {
  if (!q.value) return detected;
  return detected.filter((motion) =>
    Object.values(motion).some((value) =>
      String(value).toLowerCase().includes(q.value.toLowerCase())
    )
  );
});

// Pagination and Search Logic
const total = computed(() => filteredRows.value.length);
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageCount.value;
  return filteredRows.value.slice(start, start + pageCount.value);
});

// Open Modal and pass selected motion
const viewAction = (notification) => {
  const modal = useModal();
  modal.open(ModalViewNotifications, { notification }); // Pass motion as prop
};

// Update Page on Pagination
const updatePage = (page) => (currentPage.value = page);

// Helper Computed Values
const startItem = computed(() => (currentPage.value - 1) * pageCount.value + 1);
const endItem = computed(() =>
  Math.min(currentPage.value * pageCount.value, total.value)
);

// Watch Search Query
watch(q, () => (currentPage.value = 1));

onMounted(() => {
  loadNotifications();
});
const loadNotifications = async () => {
  await fetchAllNotifications();
};
</script>
