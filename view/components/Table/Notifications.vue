<template>
  <section class="grid gap-5 items-center">
    <!-- Search Input and Pagination -->
    <div
      class="flex flex-col-reverse sm:flex-row sm:justify-between justify-center sm:gap-0 gap-5 lg:items-end"
    >
      <!-- Search Input -->
      <div class="flex items-center gap-1">
        <UInput
          v-model="q"
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
          <!-- Clear Button for Search Input -->
          <template #trailing>
            <UButton
              v-show="q"
              icon="i-heroicons-x-mark-20-solid"
              color="gray"
              variant="link"
              class="text-red-700 dark:text-red-400 hover:text-red-400 dark:hover:text-red-600"
              @click="q = ''"
              :padded="false"
            />
          </template>
        </UInput>
      </div>

      <!-- Pagination and Item Count -->
      <div class="grid items-center gap-2">
        <div class="lg:flex justify-end hidden">
          <span class="text-xs">
            Showing
            <span class="font-medium">{{ startItem }}</span>
            -
            <span class="font-medium">{{ endItem }}</span>
            of
            <span class="font-medium">{{ totalNotifications }}</span>
            results
          </span>
        </div>
        <UPagination
          :model-value="currentPage"
          :page-count="pageCount"
          :total="totalNotifications"
          class="flex justify-center"
          @update:model-value="updatePage"
          :ui="{
            color: 'gray',
            wrapper: 'flex items-center gap-1',
            rounded: '!rounded-full min-w-[30px] justify-center',
            default: { activeButton: { variant: 'outline' } },
          }"
        />
      </div>
    </div>

    <!-- Table for Notifications -->
    <UTable
      :columns="tableHeaders"
      :rows="paginatedData"
      sort-asc-icon="i-heroicons-arrow-up"
      sort-desc-icon="i-heroicons-arrow-down"
      class="max-h-[70vh] max-w-full overflow-auto border rounded border-custom-300 dark:border-custom-800"
      :ui="{
        thead: 'sticky top-0 z-10 dark:bg-custom-700 bg-custom-300',
        tbody: 'bg-custom-100 dark:bg-custom-950',
      }"
    >
      <!-- Loading State -->
      <template #loading-state>
        <div class="flex items-center justify-center h-32 gap-2">
          <UIcon name="i-lucide-loader-circle" class="animate-spin text-2xl" />
          <p>In a moment...</p>
        </div>
      </template>

      <!-- Table ID Column -->
      <template #id-data="{ index }">
        <span>{{ (currentPage - 1) * pageCount + index + 1 }}</span>
      </template>

      <!-- Action Buttons for Each Row -->
      <template #action-data="{ row }">
        <UTooltip
          text="View"
          :popper="{ arrow: true, placement: 'right' }"
          :ui="{
            background: 'dark:bg-custom-800 bg-custom-50',
            arrow: {
              background: 'dark:before:bg-custom-700 before:bg-custom-300',
            },
          }"
        >
          <UIcon
            name="i-lucide-eye"
            class="text-xl hover:opacity-75 text-blue-500"
            @click="openModal(row)"
          />
        </UTooltip>
      </template>
    </UTable>

    <!-- Item Count for Small Screens -->
    <div class="lg:hidden flex justify-center">
      <span class="text-xs">
        Showing
        <span class="font-medium">{{ startItem }}</span>
        -
        <span class="font-medium">{{ endItem }}</span>
        of
        <span class="font-medium">{{ totalNotifications }}</span>
        results
      </span>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ModalViewNotifications } from "#components";
// import { formatDate } from "~/assets/js/formatDate";
import { notifications, fetchNotifications } from "~/assets/js/notifications";
import { user, fetchUser } from "~/assets/js/userLogged"; // Adjust the path as needed

const { username } = useRoute().params;

const currentPage = ref(1);
const pageCount = ref(20);
const q = ref("");

// Table headers
const tableHeaders = [
  { key: "id", label: "#" },
  { key: "date_captured", label: "Date" },
  { key: "motion_detected", label: "Motion Detected" },
  { key: "action", label: "Action" },
];

// Filter rows based on the search query
const filteredRows = computed(() =>
  q.value
    ? notifications.filter((item) =>
        Object.values(item).some((value) =>
          String(value).toLowerCase().includes(q.value.toLowerCase())
        )
      )
    : notifications
);

// Paginated data
const totalNotifications = computed(() => filteredRows.value.length);
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageCount.value;
  return filteredRows.value.slice(start, start + pageCount.value);
});

const updatePage = (page: number) => {
  currentPage.value = page;
};

const startItem = computed(() => (currentPage.value - 1) * pageCount.value + 1);
const endItem = computed(() =>
  Math.min(currentPage.value * pageCount.value, totalNotifications.value)
);

// Open modal and pass selected notification data
const openModal = (notification: any) => {
  const modal = useModal();
  modal.open(ModalViewNotifications, { notification });
};

// Watch search query
watch(q, () => {
  currentPage.value = 1;
});

onMounted(() => {
  loadNotifications();
  paginatedData;
});

const loadNotifications = async () => {
  await fetchUser();
  if (username) {
    await fetchNotifications(username);
  } else {
    await fetchNotifications(user.username);
  }

  console.log("settings", notifications);
};
</script>
