<template>
  <UseHead :title="`${userDetails.username} - Users - Admin`" />

  <div class="flex flex-col p-5 gap-10 w-full h-auto">
    <section>
      <UBreadcrumb :links="links">
        <template #divider>
          <UIcon name="i-lucide-chevron-right" class="text-lg" />
        </template>

        <template #default="{ link, isActive }">
          <div
            :class="{
              'dark:text-white text-custom-800 text-lg cursor-default':
                isActive,
              'text-custom-300 hover:text-custom-500 hover:dark:text-custom-300 dark:text-custom-500 text-lg':
                !isActive,
            }"
            class="rounded-full"
          >
            {{ link.label }}
          </div>
        </template>
      </UBreadcrumb>
    </section>

    <section class="flex items-center justify-center h-4/5 w-full">
      <div class="flex flex-col gap-5 w-full sm:w-3/4">
        <div class="flex justify-between">
          <div
            class="flex items-center gap-1 font-semibold cursor-default w-1/2"
          >
            <UIcon name="i-lucide-book-user" class="text-xl" />
            <h1 class="text-xl font-bold">User Details</h1>
          </div>

          <div class="flex justify-end w-1/2 gap-x-2">
            <div>
              <UButton
                label="Back"
                icon="i-lucide-move-left"
                class="flex items-center justify-center w-full rounded dark:bg-red-600 dark:hover:bg-red-500 bg-red-700 hover:bg-red-600 dark:text-custom-100"
                to="/admin/users"
              />
            </div>
            <span>
              <UButton
                v-if="user.role === 'superadmin'"
                label="Edit"
                icon="i-lucide-edit"
                class="flex cursor-pointer justify-center w-full items-center rounded dark:text-white"
                :to="`/admin/users/${username}/update`"
              />
              <UTooltip text="Only superadmin can edit" v-else>
                <UButton
                  disabled
                  class="opacity-20 cursor-not-allowed rounded"
                  label="Edit"
                  icon="i-lucide-edit"
                />
              </UTooltip>
            </span>
          </div>
        </div>

        <div
          class="flex flex-col h-auto max-h-max w-full gap-5 lg:p-10 p-5 rounded dark:bg-custom-900 bg-custom-100 border border-custom-300 dark:border-custom-700"
        >
          <h1 class="font-semibold text-lg">Profile</h1>
          <hr class="dark:border-custom-700 border-custom-200" />

          <div class="lg:flex gap-10 h-auto w-full">
            <section
              class="lg:m-auto mx-auto my-10 flex flex-col gap-3 justify-center items-center cursor-default"
            >
              <img
                v-if="userDetails.avatar"
                draggable="false"
                class="w-52 h-52 border-4 border-custom-400 dark:border-custom-300 rounded-full"
                :src="userDetails.avatar"
              />
              <span
                v-else
                class="font-black text-[150px] w-52 h-52 dark:bg-custom-700 bg-custom-400 flex items-center justify-center rounded-full"
                >{{ initial }}</span
              >

              <div class="flex gap-2 h-full items-center justify-center">
                <UKbd
                  class="text-center rounded-full"
                  :value="userDetails.status"
                  :class="{
                    'dark:border bg-green-600 dark:border-green-700 text-custom-100 dark:text-green-400 cursor-default px-2 py-1 lowercase':
                      userDetails.status === 'active',
                    'dark:border bg-red-600 dark:border-red-700 text-custom-100 dark:text-red-400 cursor-default px-2 py-1 lowercase':
                      userDetails.status === 'inactive',
                  }"
                />
                <UKbd
                  class="text-center rounded-full px-2 py-1 bg-custom-700 text-custom-100 dark:text-custom-200 dark:bg-custom-900 dark:border dark:border-custom-500"
                  :value="userDetails.role"
                />
              </div>
            </section>

            <section class="lg:w-3/5 w-full flex flex-col gap-5">
              <div class="p-5 dark:bg-custom-800 bg-custom-50 space-y-2">
                <section class="flex justify-between items-center flex-wrap">
                  <div class="flex items-center gap-2 text-xl">
                    <p class="font-bold">Name:</p>
                    <p class="capitalize font-medium dark:text-custom-300">
                      {{ userDetails.name }}
                    </p>
                  </div>

                  <div
                    v-if="userDetails.gender === 'female'"
                    class="flex items-center gap-1 rounded-full cursor-default bg-pink-500 dark:bg-pink-500 text-white px-2 py-1"
                  >
                    <UIcon name="i-game-icons-female" class="h-4 w-4" />
                    <p class="capitalize text-xs font-medium">
                      {{ userDetails.gender }}
                    </p>
                  </div>

                  <div
                    v-else-if="userDetails.gender === 'male'"
                    class="flex items-center gap-1 rounded-full cursor-default bg-blue-500 dark:bg-blue-500 text-white px-2 py-1"
                  >
                    <UIcon name="i-game-icons-male" class="h-4 w-4" />
                    <p class="capitalize text-xs font-medium">
                      {{ userDetails.gender }}
                    </p>
                  </div>

                  <div v-else class="text-sm cursor-default">Undefined</div>
                </section>

                <section class="flex items-center gap-2">
                  <UIcon name="i-heroicons-phone-16-solid" class="h-auto w-5" />
                  <p class="capitalize text-base dark:text-custom-300">
                    +63{{ userDetails.phone_number }}
                  </p>
                </section>

                <section class="flex items-center gap-2">
                  <UIcon
                    name="i-heroicons-envelope-16-solid"
                    class="h-auto w-5"
                  />
                  <p class="text-base dark:text-custom-300">
                    {{ userDetails.email }}
                  </p>
                </section>
              </div>

              <div class="p-5 dark:bg-custom-800 bg-custom-50 space-y-2">
                <section class="flex items-center gap-2">
                  <h1 class="font-medium">Username:</h1>
                  <p class="text-base dark:text-custom-300">
                    {{ userDetails.username }}
                  </p>
                </section>

                <section class="flex gap-2 justify-between items-center">
                  <div class="flex gap-2">
                    <h1 class="font-medium">Password:</h1>
                    <!-- dli ma display ang password kay naka hashed (for safety) pero kung dli i-hashed kay ma retrieve-->
                    <p class="text-base dark:text-custom-300">
                      {{ passwordDisplay }}
                    </p>
                    <!-- <p class="text-base dark:text-custom-300">********</p>  -->
                  </div>
                  <!-- <button @click="togglePasswordVisibility" class="text-blue-500 underline">
                  {{ isPasswordVisible ? 'Hide' : 'Show' }}
                </button> -->
                  <UTooltip
                    :text="
                      isPasswordVisible ? 'Hide Password' : 'Show Password'
                    "
                    :popper="{ arrow: true }"
                    :ui="{
                      background: 'dark:bg-custom-800 bg-custom-50',
                      arrow: {
                        background:
                          'dark:before:bg-custom-950 before:bg-custom-300',
                      },
                    }"
                  >
                    <div
                      class="flex gap-1 items-center cursor-pointer hover:opacity-60"
                      @click="togglePasswordVisibility"
                    >
                      <UIcon
                        :name="
                          isPasswordVisible
                            ? 'i-fluent-eye-off-24-filled'
                            : 'i-fluent-eye-12-filled'
                        "
                      />
                    </div>
                  </UTooltip>
                </section>
              </div>

              <div class="p-5 dark:bg-custom-800 bg-custom-50 space-y-2">
                <div class="space-y-2">
                  <section class="flex gap-2">
                    <h1 class="font-medium">Account created:</h1>
                    <p class="dark:text-custom-300">
                      {{ formatDate(userDetails.created_at) }}
                    </p>
                  </section>
                  <section class="flex gap-2">
                    <h1 class="font-medium">Account updated:</h1>
                    <p class="dark:text-custom-300">
                      {{ formatDate(userDetails.updated_at) }}
                    </p>
                  </section>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </section>

    <hr
      v-if="userDetails.role == 'client'"
      class="border-custom-300 dark:border-custom-800"
    />

    <section
      v-if="userDetails.role == 'client'"
      class="flex flex-col gap-3 w-full sm:w-3/4 mx-auto"
    >
      <div class="flex items-center gap-1 font-semibold cursor-default w-1/2">
        <UIcon name="i-lucide-book-open-text" class="text-xl" />
        <h1 class="text-xl font-bold">Notifications Log</h1>
      </div>
      <p class="mb-0 lg:-mb-6">
        These are the list of motions detected by this user.
      </p>
      <TableNotifications />
    </section>
  </div>
</template>

<script setup>
definePageMeta({ layout: "sidebar" });

import { user } from "~/assets/js/userLogged";
import { useRoute } from "vue-router";
import { formatDate } from "~/assets/js/formatDate";
import { getSpecificAvatar } from "~/assets/js/avatar";

const { username } = useRoute().params;

const isPasswordVisible = ref(false);

// Computed property to show either the masked or full password
const passwordDisplay = computed(() => {
  if (isPasswordVisible.value) {
    return userDetails.password; // Show full password
  }
  // Mask the password: Show the first 3 and last characters, and replace the middle with asterisks
  return userDetails.password
    ? userDetails.password.substring(0, 3) +
        "***" +
        userDetails.password.slice(-1)
    : "";
});

// Function to toggle password visibility
const togglePasswordVisibility = () => {
  isPasswordVisible.value = !isPasswordVisible.value;
};

const links = [{ label: "Users", to: "/admin/users" }, { label: "Details" }];

const userDetails = reactive({
  name: "",
  role: "",
  status: "",
  phone_number: "",
  email: "",
  gender: "",
  username: "",
  password: "",
  created_at: "",
  updated_at: "",
  avatar: "https://robohash.org/set_set3/bgset_bg1/24.png?size=1000x1000",
});

const initial = computed(() => userDetails.name.charAt(0).toUpperCase());

async function getUser() {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/users/${username}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("_token")}`,
        },
      }
    );

    if (response.ok) {
      const data = await response.json();
      Object.assign(
        (userDetails.name = `${data.user.first_name} ${data.user.middle_initial}. ${data.user.last_name}`)
      );

      userDetails.role = data.user.role;
      userDetails.status = data.user.status;
      userDetails.phone_number = data.user.phone_number;
      userDetails.email = data.user.email;
      userDetails.gender = data.user.gender;
      userDetails.username = data.user.username;
      userDetails.password = data.user.password;
      userDetails.created_at = data.user.created_at;
      userDetails.updated_at = data.user.updated_at;
      userDetails.avatar = getSpecificAvatar(data.user.avatar);
    } else {
      console.error("Error fetching user:", await response.json());
    }
  } catch (error) {
    console.error("Error fetching user:", error);
  }
}

// function statusClass(value) {
//   return {
//     'dark:border bg-green-600 dark:border-green-700 text-custom-100 dark:text-green-400 cursor-default px-2': value === 'active',
//     'dark:border bg-red-600 dark:border-red-700 text-custom-100 dark:text-red-400 cursor-default px-2': value === 'inactive'
//   };
// }

onMounted(getUser);
</script>
