<template>
  <div class="h-auto w-full p-5 gap-5 flex flex-col justify-between">
    <header class="flex justify-between w-full items-center">
      <h1 class="text-lg font-semibold text-custom-800 dark:text-white">
        Settings
      </h1>
      <UButton
        class="bg-red-500 dark:bg-red-500 hover:bg-red-600 dark:hover:bg-red-400 text-white dark:text-white rounded"
        label="Logout"
        icon="i-lucide-log-out"
        @click="handleLogout"
      />
    </header>

    <div class="flex flex-col gap-5 h-auto w-full">
      <div
        class="flex flex-col h-auto max-h-max w-full gap-5 lg:p-10 p-5 rounded dark:bg-custom-900 bg-custom-100 border border-custom-300 dark:border-custom-700"
      >
        <div class="flex justify-between items-center">
          <h1 class="font-semibold text-lg">Profile</h1>

          <UButton
            v-if="user.role === 'client'"
            class="flex cursor-pointer justify-center items-center rounded dark:text-white"
            label="Edit"
            icon="i-lucide-edit"
            :to="`/client/settings/${user.username}`"
          />

          <UButton
            v-if="user.role === 'admin' || user.role === 'superadmin'"
            class="flex cursor-pointer justify-center items-center rounded dark:text-white"
            label="Edit"
            icon="i-lucide-edit"
            :to="`/admin/settings/${user.username}`"
          />
        </div>

        <hr class="dark:border-custom-700 border-custom-200" />

        <div class="lg:flex gap-10 h-auto w-full">
          <section
            class="lg:m-auto mx-auto my-10 flex flex-col gap-3 justify-center items-center cursor-default"
          >
            <img
              v-if="user.avatar"
              draggable="false"
              class="w-52 h-52 border-4 border-custom-400 dark:border-custom-300 rounded-full"
              :src="user.avatar"
            />
            <span
              v-else
              class="font-black text-[150px] w-52 h-52 dark:bg-custom-700 bg-custom-400 flex items-center justify-center rounded-full"
              >{{ initial }}</span
            >

            <div class="flex gap-2 h-full items-center justify-center">
              <UKbd
                class="text-center rounded-full"
                :value="user.status"
                :class="{
                  'dark:border bg-green-600 dark:border-green-700 text-custom-100 dark:text-green-400 cursor-default px-2 py-1 lowercase':
                    user.status === 'active',
                  'dark:border bg-red-600 dark:border-red-700 text-custom-100 dark:text-red-400 cursor-default px-2 py-1 lowercase':
                    user.status === 'inactive',
                }"
              />
              <UKbd
                class="text-center rounded-full px-2 py-1 bg-custom-700 text-custom-100 dark:text-custom-200 dark:bg-custom-900 dark:border dark:border-custom-500"
                :value="user.role"
              />
            </div>
          </section>

          <section class="lg:w-3/5 w-full flex flex-col gap-5">
            <div class="p-5 dark:bg-custom-800 bg-custom-50 space-y-2">
              <section class="flex justify-between items-center flex-wrap">
                <div class="flex items-center gap-2 text-xl">
                  <p class="font-bold">Name:</p>
                  <p class="capitalize dark:text-custom-300 font-medium">
                    {{ user.name }}
                  </p>
                </div>

                <div
                  v-if="user.gender === 'female'"
                  class="flex items-center gap-1 rounded-full cursor-default bg-pink-500 dark:bg-pink-500 text-white px-2 py-1"
                >
                  <UIcon name="i-game-icons-female" class="h-4 w-4" />
                  <p class="capitalize text-xs font-medium">
                    {{ user.gender }}
                  </p>
                </div>

                <div
                  v-else-if="user.gender === 'male'"
                  class="flex items-center gap-1 rounded-full cursor-default bg-blue-500 dark:bg-blue-500 text-white px-2 py-1"
                >
                  <UIcon name="i-game-icons-male" class="h-4 w-4" />
                  <p class="capitalize text-xs font-medium">
                    {{ user.gender }}
                  </p>
                </div>

                <div v-else class="text-sm">Others</div>
              </section>

              <section class="flex items-center gap-2">
                <UIcon name="i-heroicons-phone-16-solid" class="h-auto w-5" />
                <p class="capitalize text-base dark:text-custom-300">
                  +63{{ user.phone_number }}
                </p>
              </section>

              <section class="flex items-center gap-2">
                <UIcon
                  name="i-heroicons-envelope-16-solid"
                  class="h-auto w-5"
                />
                <p class="text-base dark:text-custom-300">{{ user.email }}</p>
              </section>
            </div>

            <div class="p-5 dark:bg-custom-800 bg-custom-50 space-y-2">
              <section class="flex items-center gap-2">
                <h1 class="font-medium">Username:</h1>
                <p class="text-base dark:text-custom-300">
                  {{ user.username }}
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
                  :text="isPasswordVisible ? 'Hide Password' : 'Show Password'"
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
                    {{ formatDate(user.created_at) }}
                  </p>
                </section>
                <section class="flex gap-2">
                  <h1 class="font-medium">Account updated:</h1>
                  <p class="dark:text-custom-300">
                    {{ formatDate(user.updated_at) }}
                  </p>
                </section>
              </div>
            </div>
          </section>
        </div>
      </div>

      <div
        v-if="user.role === 'client'"
        class="flex flex-col h-auto w-full gap-5 lg:p-10 p-5 rounded dark:bg-custom-900 bg-custom-100 border border-custom-300 dark:border-custom-700"
      >
        <h1 class="font-semibold text-lg">Phone Associated</h1>

        <hr class="dark:border-custom-700 border-custom-200" />

        <section class="md:flex grid w-full gap-5">
          <UForm
            :state="state"
            @submit="onSubmit"
            :validate="validate"
            @error="onError"
            class="space-y-2 w-full flex flex-col gap-5"
          >
            <UFormGroup class="grid gap-2" name="phone" :ui="{ error: 'mt-1' }">
              <template #label>
                <div class="flex items-center justify-start gap-1">
                  <UIcon name="i-lucide-phone" class="text-lg" />
                  <p class="text-base">
                    Add Phone
                    <span class="font-bold text-red-700 dark:text-red-400"
                      >(max: 3 only)</span
                    >
                  </p>
                  {{ state.errors }}
                </div>
              </template>

              <template #default="{ error }">
                <div class="relative w-full">
                  <div
                    class="flex gap-1 items-center absolute z-10 left-2 top-[10px] border-r pr-1 border-r-custom-900"
                  >
                    <UIcon name="i-emojione-v1-flag-for-philippines" />
                    <div
                      class="font-medium cursor-default text-xs dark:text-custom-900"
                    >
                      +63
                    </div>
                  </div>

                  <UInput
                    class="w-full"
                    v-model="state.user.contact_number"
                    :disabled="phones.length == 3"
                    color="gray"
                    size="md"
                    :ui="{
                      rounded: 'rounded',
                      color: error
                        ? {
                            red: {
                              outline:
                                'bg-red-100 dark:bg-red-50 pl-16 text-custom-900 dark:text-custom-900 focus:ring-1 focus:ring-red-400 border border-red-700 focus:border-red-400 active:ring-red-400 active:border-red-400',
                            },
                          }
                        : {
                            gray: {
                              outline:
                                'dark:bg-custom-100 pl-16 dark:text-custom-900 border-none',
                            },
                          },
                    }"
                  />
                </div>
              </template>

              <template #error="{ error }">
                <span
                  :class="[
                    error
                      ? 'text-red-500 dark:text-red-400 text-xs font-bold'
                      : 'text-primary-500 dark:text-primary-400',
                  ]"
                >
                  {{ error ? error : undefined }}
                </span>
              </template>
            </UFormGroup>

            <UTooltip
              :text="phones.length == 3 ? 'Max number reached' : 'Save number'"
              class="w-full"
              :popper="{ arrow: true }"
              :ui="{
                background: 'dark:bg-custom-800 bg-custom-50',
                arrow: {
                  background: 'dark:before:bg-custom-950 before:bg-custom-300',
                },
              }"
            >
              <UButton
                :disabled="phones.length == 3"
                type="submit"
                :label="save.label.value"
                :loading="save.bool.value"
                :loading-icon="save.icon.value"
                size="sm"
                class="rounded dark:text-white dark:bg-green-500 bg-green-500 hover:bg-green-600 hover:dark:bg-green-600 flex justify-center w-full -mt-5"
              />
            </UTooltip>
          </UForm>

          <div
            class="h-auto w-1 bg-custom-200 dark:bg-custom-700 md:block hidden"
          ></div>

          <section class="w-full flex flex-col gap-5">
            <p class="text-sm text-custom-500 dark:text-custom-300">
              Selected phone numbers will receive an SMS notification.
            </p>

            <div
              v-for="(phone, index) in phones"
              :key="index"
              class="border-b dark:border-b-custom-950 rounded-lg border-b-custom-200 pb-2"
            >
              <div class="px-2 flex justify-between items-center">
                <div class="max-w-[150px] truncate">
                  <UCheckbox
                    :label="phone.number"
                    v-model="phone.selected"
                    color="green"
                    @change="handleCheckboxChange(phone.contact_id)"
                  />
                </div>

                <UTooltip
                  text="Remove"
                  :popper="{ placement: 'left', arrow: true }"
                  :ui="{
                    background: 'dark:bg-custom-800 bg-custom-50',
                    arrow: {
                      background:
                        'dark:before:bg-custom-950 before:bg-custom-300',
                    },
                  }"
                >
                  <UIcon
                    @click="remove(phone)"
                    name="i-lucide-trash-2"
                    class="cursor-pointer hover:text-red-500"
                  />
                </UTooltip>
              </div>
            </div>
          </section>
        </section>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import type { FormError, FormErrorEvent, FormSubmitEvent } from "#ui/types";
import { user, initial, fetchUser } from "~/assets/js/userLogged";
import { name, playSound } from "~/assets/js/sound";
import { formatDate } from "~/assets/js/formatDate";

const isPasswordVisible = ref(false);

// Computed property to show either the masked or full password
const passwordDisplay = computed(() => {
  if (isPasswordVisible.value) {
    return user.password; // Show full password
  }
  // Mask the password: Show the first 3 and last characters, and replace the middle with asterisks
  return user.password
    ? user.password.substring(0, 3) + "***" + user.password.slice(-1)
    : "";
});

// Function to toggle password visibility
const togglePasswordVisibility = () => {
  isPasswordVisible.value = !isPasswordVisible.value;
};

interface Phone {
  contact_id: number;
  number: string;
  selected: boolean;
}

// Reactive phones array
const phones = ref<Phone[]>([
  {
    contact_id: 1,
    number: "+6301938473625",
    selected: true,
  },
  {
    contact_id: 2,
    number: "+631845884734",
    selected: false,
  },
]);

// Function to fetch contacts and update the phones array
async function fetchContact() {
  try {
    const response = await $fetch(`http://127.0.0.1:8000/api/user/contact`, {
      method: "GET",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("_token"), // Use 'Bearer' prefix for token
      },
    });

    if (response) {
      // Map the response to the Phone interface, converting 1/0 to true/false
      phones.value = response.map((item) => ({
        contact_id: item.contact_id,
        number: "+63" + item.contact_number, // Adjust this if the field name is different
        selected: item.is_enabled === 1, // Convert 1 to true, 0 to false
      }));
    }
  } catch (error) {
    console.error("Error fetching contacts:", error);
  }
}

const handleCheckboxChange = async (phone) => {
  try {
    const response = await $fetch(
      `http://127.0.0.1:8000/api/user/contact/${phone}`,
      {
        method: "PUT",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("_token"), // Use 'Bearer' prefix for token
        },
      }
    );

    if (response) {
      console.log(response);
    }
  } catch {
    console.log("error sa pag update sa checkbox");
  }
};

const remove = async (phone: Phone) => {
  console.log(phone);

  name.value = "delete_1";
  if (confirm("Remove this phone number?") === true) {
    try {
      const response = await $fetch(
        `http://127.0.0.1:8000/api/user/contact/${phone.contact_id}`,
        {
          method: "delete",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("_token"), // Use 'Bearer' prefix for token
          },
        }
      );

      if (response) {
        playSound();
        phones.value = phones.value.filter((p) => p.number !== phone.number);
        toast.add({
          title: "Removed Successfully!",
          icon: "i-lucide-trash-2",
          timeout: 2000,
          ui: {
            background: "dark:bg-red-700 bg-red-300",
            progress: { background: "dark:bg-white bg-red-700 rounded-full" },
            ring: "ring-1 ring-red-700 dark:ring-custom-900",
            default: { closeButton: { color: "white" } },
            icon: "text-custom-900",
          },
        });
      }
    } catch {
      console.log("nag error sa pag delete");
    }
  } else {
    console.log("Cancelled.");
  }
};

const state = reactive({
  errors: [] as string[],
  user: {
    contact_number: "",
  },
});

// FE validation
const validate = (state: any): FormError[] => {
  const errors = [];
  if (!state.user.contact_number)
    errors.push({ path: "phone", message: "Required" });
  return errors;
};

const isOpen = ref(false);

const save = {
  bool: ref(false),
  label: ref("Save"),
  icon: ref(""),
};

async function onSubmit(event: FormSubmitEvent<any>) {
  // Do something with data

  state.errors = [];

  name.value = "success_2";
  save.bool.value = true;
  save.icon.value = "i-lucide-loader-circle";
  save.label.value = "";

  const params = {
    contact_number: event.data.user.contact_number,
    is_enabled: 1,
  };

  try {
    const response = await $fetch(`http://127.0.0.1:8000/api/user/contact`, {
      method: "POST",
      body: params,
      headers: {
        Authorization: "Bearer " + localStorage.getItem("_token"), // Use 'Bearer' prefix for token
      },
    });

    if (response) {
      setTimeout(() => {
        phones.value.push({
          contact_id: response.contact_id,
          number: "+63" + state.user.contact_number, // Use the phone number from the form state
          selected: true, // Default selected (you can change this as needed)
        });

        playSound();
        toast.add({
          title: "Phone Added Successfully!",
          icon: "i-iconoir-phone-plus",
          timeout: 2000,
          ui: {
            background: "dark:bg-green-700 bg-green-300",
            progress: {
              background: "dark:bg-white bg-green-700 rounded-full",
            },
            ring: "ring-1 ring-green-700 dark:ring-custom-900",
            default: {
              closeButton: {
                color: "white",
              },
            },
            icon: "text-custom-900",
          },
        });

        state.user.contact_number = "";

        save.label.value = "Save";
        save.bool.value = false;
        isOpen.value = false;
        navigateTo("/client/settings");
      }, 800);
    }
  } catch (error) {
    state.errors = error.response?.data?.errors || [
      { message: "An unexpected error occurred. Please try again." },
    ];
    console.error("Error occurred while adding contact:", error);

    save.label.value = "Save";
    save.bool.value = false;
    isOpen.value = false;
    navigateTo("/client/settings");
  }
}

async function onError(event: FormErrorEvent) {
  const element = document.getElementById(event.errors[0].id);
  element?.focus();
  element?.scrollIntoView({ behavior: "smooth", block: "center" });
}

const toast = useToast();

async function handleLogout() {
  name.value = "logoff_1";
  if (confirm("You would like to log out?") == true) {
    try {
      const response = await $fetch(`http://127.0.0.1:8000/api/user/logout`, {
        method: "POST",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("_token"),
        },
      });

      playSound();

      toast.add({
        title: "Logout Successfully!",
        icon: "i-lucide-log-out",
        timeout: 2000,
        ui: {
          background: "dark:bg-orange-700 bg-orange-300",
          progress: {
            background: "dark:bg-white bg-orange-700 rounded-full",
          },
          ring: "ring-1 ring-orange-700 dark:ring-custom-900",
          default: {
            closeButton: {
              color: "white",
            },
          },
          icon: "text-custom-900",
        },
      });
      localStorage.removeItem("_token");
      navigateTo("/auth");
    } catch {}
  } else {
    console.log("Cancelled.");
  }
}

onMounted(() => {
  fetchUser();

  fetchContact();
});
</script>
