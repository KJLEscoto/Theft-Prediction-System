<template>
  <UseHead :title="`Edit - ${state.user.username} - Users - Admin`" />

  <div class="h-auto w-full flex flex-col p-5 gap-10">
    <section class="">
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
    <section class="h-4/5 w-full flex justify-center items-center">
      <div
        class="sm:w-3/4 w-full h-auto border p-10 rounded border-custom-300 bg-custom-100 dark:bg-custom-900 dark:border-custom-700"
      >
        <UForm
          class="h-auto w-full flex flex-col gap-3"
          :state="state"
          @submit="onSubmit"
          :validate="validate"
          @error="onError"
        >
          <header class="flex justify-between items-center">
            <div
              class="font-semibold cursor-default flex items-center gap-1 w-1/2"
            >
              <UIcon name="i-lucide-user-round-plus" class="text-xl" />
              <h1 class="font-bold text-xl">New User</h1>
            </div>
          </header>

          <div class="flex justify-between items-center">
            <h1 class="text-lg w-auto">Avatar</h1>

            <div class="flex justify-end w-1/2 gap-x-2">
              <section class="w-auto">
                <UButton
                  :label="load.label.value"
                  :loading-icon="load.icon.value"
                  :loading="load.bool.value"
                  icon="i-lucide-save"
                  class="flex justify-center w-full items-center rounded dark:text-white bg-green-600 hover:bg-green-700 dark:bg-green-700 hover:dark:bg-green-800"
                  type="submit"
                />
              </section>

              <section class="w-auto">
                <UButton
                  label="Cancel"
                  icon="i-lucide-x"
                  class="flex justify-center w-full items-center rounded dark:bg-red-600 dark:hover:bg-red-500 bg-red-700 hover:bg-red-600 dark:text-custom-100"
                  :to="`/admin/users/${state.user.username}`"
                />
              </section>
            </div>
          </div>

          <hr class="border-custom-300 dark:border-custom-500 w-full" />

          <section class="flex justify-center w-full gap-5 px-5 flex-wrap">
            <div class="m-auto grid gap-2">
              <div class="flex justify-between">
                <p>Preview:</p>
                <p @click="resetAvatar" class="hover:opacity-50 cursor-pointer">
                  Reset
                </p>
              </div>
              <div class="flex justify-start gap-3 items-end">
                <img
                  v-if="previewAvatar || state.user.avatar"
                  class="w-40 h-40 border-4 border-custom-400 dark:border-custom-300"
                  :src="previewAvatar || state.user.avatar"
                />
                <span
                  v-else
                  class="font-black text-[150px] w-40 h-40 border-4 border-custom-400 dark:border-custom-300 flex items-center justify-center"
                  >{{ state.user.initial }}</span
                >
                <img
                  v-if="previewAvatar || state.user.avatar"
                  class="w-24 h-24 border-4 border-custom-400 dark:border-custom-300"
                  :src="previewAvatar || state.user.avatar"
                />
                <span
                  v-else
                  class="font-black text-[50px] w-24 h-24 border-4 border-custom-400 dark:border-custom-300 flex items-center justify-center"
                  >{{ state.user.initial }}</span
                >
                <img
                  v-if="previewAvatar || state.user.avatar"
                  class="w-14 h-14 border-2 border-custom-400 dark:border-custom-300"
                  :src="previewAvatar || state.user.avatar"
                />
                <span
                  v-else
                  class="font-black text-[20px] w-14 h-14 border-4 border-custom-400 dark:border-custom-300 flex items-center justify-center"
                  >{{ state.user.initial }}</span
                >
              </div>
            </div>

            <div
              class="grid grid-cols-5 gap-2 p-3 bg-white dark:bg-custom-800 rounded m-auto max-h-[300px] overflow-y-scroll"
            >
              <section v-for="avatar in avatars">
                <img
                  :class="[
                    'w-14 h-14 cursor-pointer',
                    previewAvatar === avatar ||
                    (!previewAvatar && state.user.avatar === avatar)
                      ? 'border-4'
                      : 'border',
                    'border-red-600 dark:border-red-800',
                  ]"
                  :src="avatar"
                  @click="setPreviewAvatar(avatar)"
                />
              </section>
            </div>
          </section>

          <h1 class="text-lg w-auto">Information</h1>
          <hr class="border-custom-300 dark:border-custom-500 w-full" />

          <!-- display other errors here -->
          <div v-if="state.errors.length">
            <ul>
              <li
                v-for="(error, index) in state.errors"
                :key="index"
                class="text-red-500 dark:text-red-400 text-lg font-bold text-center truncate"
              >
                {{ error }}
              </li>
            </ul>
          </div>

          <section class="flex w-full gap-x-2">
            <!-- first name -->
            <UFormGroup class="w-1/2" name="first_name" :ui="{ error: 'mt-1' }">
              <template #label>
                <p class="text-sm mb-2">First name</p>
              </template>

              <template #default="{ error }">
                <UInput
                  type="text"
                  color="gray"
                  v-model="state.user.first_name"
                  size="md"
                  :ui="{
                    rounded: 'rounded',
                    color: error
                      ? {
                          red: {
                            outline:
                              'dark:bg-red-50 bg-red-100 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400',
                          },
                        }
                      : {
                          gray: {
                            outline:
                              'dark:bg-custom-100 dark:text-custom-900 border-none',
                          },
                        },
                  }"
                />
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

            <!-- last name -->
            <UFormGroup class="w-1/2" name="last_name" :ui="{ error: 'mt-1' }">
              <template #label>
                <p class="text-sm mb-2">Last name</p>
              </template>

              <template #default="{ error }">
                <UInput
                  type="text"
                  color="gray"
                  v-model="state.user.last_name"
                  size="md"
                  :ui="{
                    rounded: 'rounded',
                    color: error
                      ? {
                          red: {
                            outline:
                              'dark:bg-red-50 bg-red-100 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400',
                          },
                        }
                      : {
                          gray: {
                            outline:
                              'dark:bg-custom-100 dark:text-custom-900 border-none',
                          },
                        },
                  }"
                />
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

            <!-- middle initial -->
            <UFormGroup class="w-1/4" name="m_i">
              <template #label>
                <p class="text-sm mb-2">M. I.</p>
              </template>

              <template #default="{ error }">
                <UInput
                  type="text"
                  color="gray"
                  size="md"
                  v-model="state.user.middle_initial"
                  :ui="{
                    rounded: 'rounded',
                    color: error
                      ? {
                          red: {
                            outline:
                              'dark:bg-red-50 bg-red-100 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400',
                          },
                        }
                      : {
                          gray: {
                            outline:
                              'dark:bg-custom-100 dark:text-custom-900 border-none',
                          },
                        },
                  }"
                />
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
          </section>

          <section class="flex w-full gap-x-2">
            <!-- gender -->
            <UFormGroup class="w-2/3" label="Gender" name="gender">
              <template #label>
                <p class="text-sm mb-2">Gender</p>
              </template>

              <URadioGroup
                v-model="state.user.gender"
                :options="genderOptions"
                class="ml-2"
              />
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

            <!-- phone -->
            <UFormGroup class="w-1/2" name="phone_number">
              <template #label>
                <p class="text-sm mb-2">Phone number</p>
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
                    v-model="state.user.phone_number"
                    color="gray"
                    size="md"
                    :ui="{
                      rounded: 'rounded',
                      color: error
                        ? {
                            red: {
                              outline:
                                'dark:bg-red-50 bg-red-100 pl-16 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400',
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

            <!-- email -->
            <UFormGroup class="w-1/2" name="email">
              <template #label>
                <p class="text-sm mb-2">Email</p>
              </template>

              <template #default="{ error }">
                <UInput
                  type="email"
                  color="gray"
                  size="md"
                  v-model="state.user.email"
                  :ui="{
                    rounded: 'rounded',
                    color: error
                      ? {
                          red: {
                            outline:
                              'dark:bg-red-50 bg-red-100 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400',
                          },
                        }
                      : {
                          gray: {
                            outline:
                              'dark:bg-custom-100 dark:text-custom-900 border-none',
                          },
                        },
                  }"
                />
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
          </section>

          <section class="flex w-full gap-x-2">
            <!-- status -->
            <UFormGroup class="w-2/3" name="status">
              <template #label>
                <p class="text-sm mb-2">Status</p>
              </template>
              <URadioGroup
                v-model="state.user.status"
                :options="statusOptions"
                class="ml-2"
                :uiRadio="{
                  color:
                    state.user.status === statusOptions[0].value
                      ? 'text-green-500'
                      : 'text-red-500',
                }"
              />
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

            <!-- role -->
            <UFormGroup class="w-full" name="role">
              <template #label>
                <p class="text-sm mb-2">Role</p>
              </template>

              <template #default="{ error }">
                <UTooltip
                  class="w-full"
                  text="Role cannot be change."
                  :popper="{ arrow: true }"
                  :ui="{
                    background: 'dark:bg-custom-800 bg-custom-50',
                    arrow: {
                      background:
                        'dark:before:bg-custom-950 before:bg-custom-300',
                    },
                  }"
                >
                  <USelectMenu
                    disabled
                    color="gray"
                    class="w-full capitalize"
                    selected-icon="i-heroicons-hand-thumb-up-solid"
                    size="md"
                    :ui="{
                      rounded: 'rounded',
                      placeholder: 'capitalize',
                      color: error
                        ? {
                            red: {
                              outline:
                                'dark:bg-red-50 bg-red-100 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400',
                            },
                          }
                        : {
                            gray: {
                              outline:
                                'dark:bg-custom-100 dark:text-custom-900 border-none',
                            },
                          },
                    }"
                    :uiMenu="{
                      background: 'dark:bg-custom-400',
                      option: {
                        color: 'dark:text-white',
                        active: 'dark:bg-custom-600',
                        empty: 'dark:text-white',
                      },
                      empty: 'dark:text-white',
                    }"
                    placeholder="Select a role"
                  >
                    <template #label>
                      <span
                        v-if="state.user.role"
                        class="truncate capitalize"
                        >{{ state.user.role }}</span
                      >
                      <span v-else>---</span>
                    </template>

                    <template #empty> No role. </template>
                  </USelectMenu>
                </UTooltip>
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
          </section>

          <h1 class="text-lg w-auto text-start mt-3 -mb-2">
            Login Credentials
          </h1>
          <hr class="border-custom-300 dark:border-custom-500 w-full" />

          <section class="flex w-full gap-x-2">
            <UFormGroup class="w-1/2" name="username">
              <template #label>
                <p class="text-sm mb-2">Username</p>
              </template>
              <template #default="{ error }">
                <UInput
                  type="text"
                  color="gray"
                  size="md"
                  v-model="state.user.username"
                  :ui="{
                    rounded: 'rounded',
                    color: error
                      ? {
                          red: {
                            outline:
                              'dark:bg-red-50 bg-red-100 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400',
                          },
                        }
                      : {
                          gray: {
                            outline:
                              'dark:bg-custom-100 dark:text-custom-900 border-none',
                          },
                        },
                  }"
                />
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

            <UFormGroup class="w-1/2" name="password">
              <template #label>
                <p class="text-sm mb-2">Password</p>
              </template>

              <template #default="{ error }">
                <div class="relative w-full">
                  <!-- Show/Hide Icon -->
                  <div
                    class="flex gap-1 items-center absolute z-10 right-2 top-[10px] pr-1 cursor-pointer dark:text-black"
                    @click="togglePassword"
                  >
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
                      <UIcon
                        :name="
                          isPasswordVisible
                            ? 'i-fluent-eye-off-24-filled'
                            : 'i-fluent-eye-12-filled'
                        "
                      />
                    </UTooltip>
                  </div>

                  <UInput
                    v-model="state.user.password"
                    :type="isPasswordVisible ? 'text' : 'password'"
                    color="gray"
                    size="md"
                    :ui="{
                      rounded: 'rounded',
                      color: error
                        ? {
                            red: {
                              outline:
                                'dark:bg-red-50 bg-red-100 pr-10 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400',
                            },
                          }
                        : {
                            gray: {
                              outline:
                                'dark:bg-custom-100 dark:text-custom-900 pr-10 border-none',
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
          </section>
        </UForm>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "sidebar",
});

import type { FormError, FormErrorEvent, FormSubmitEvent } from "#ui/types";
import {
  user,
  previewAvatar,
  fetchSpecificAvatar,
  setPreviewAvatar,
} from "~/assets/js/userLogged";
import { name, playSound } from "~/assets/js/sound";
import { avatars } from "~/assets/js/avatar";
import { isPasswordVisible, togglePassword } from "~/assets/js/showPassword";

const load = {
  bool: ref(false),
  label: ref("Update"),
  icon: ref(""),
};

const statusOptions = [
  {
    value: "active",
    label: "Active",
  },
  {
    value: "inactive",
    label: "Inactive",
  },
];

const genderOptions = [
  {
    value: "male",
    label: "Male",
  },
  {
    value: "female",
    label: "Female",
  },
];

const state = reactive({
  errors: [] as string[],
  user: {
    first_name: "",
    last_name: "",
    middle_initial: "",
    gender: "",
    status: "",
    phone_number: "",
    role: "",
    username: "",
    password: "",
    email: "",
    avatar: null,
    initial: "",
  },
});

const validate = (state: any): FormError[] => {
  const errors = [];
  if (!state.user.first_name)
    errors.push({ path: "first_name", message: "Required" });
  if (!state.user.last_name)
    errors.push({ path: "last_name", message: "Required" });
  if (!state.user.gender) errors.push({ path: "gender", message: "Required" });
  if (!state.user.phone_number)
    errors.push({ path: "phone_number", message: "Required" });
  if (!state.user.email) errors.push({ path: "email", message: "Required" });
  if (!state.user.status) errors.push({ path: "status", message: "Required" });
  if (!state.user.role) errors.push({ path: "role", message: "Required" });
  if (!state.user.username)
    errors.push({ path: "username", message: "Required" });
  if (!state.user.password)
    errors.push({ path: "password", message: "Required" });
  return errors;
};

async function onError(event: FormErrorEvent) {
  const element = document.getElementById(event.errors[0].id);
  element?.focus();
  element?.scrollIntoView({ behavior: "smooth", block: "center" });
}

const { username } = useRoute().params;
onMounted(() => {
  getUser(username);
});

async function getUser(username) {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/users/${username}`,
      {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("_token")}`,
        },
      }
    );

    if (response.ok) {
      const data = await response.json();

      state.user.first_name = data.user.first_name;
      state.user.last_name = data.user.last_name;
      state.user.middle_initial = data.user.middle_initial;
      state.user.gender = data.user.gender;
      state.user.status = data.user.status;
      state.user.phone_number = data.user.phone_number;
      state.user.role = data.user.role;
      state.user.username = data.user.username;
      state.user.password = data.user.password;
      state.user.email = data.user.email;
      state.user.avatar = fetchSpecificAvatar(data.user.avatar);
      state.user.initial = data.user.first_name.charAt(0);
    } else {
      console.error("Error fetching userrrr:", await response.json());
    }
  } catch (error) {
    console.error("Error fetchinggg user:", error);
  }
}

async function onSubmit() {
  const { user } = state; // Destructure to make code cleaner
  let number = "";

  if ((previewAvatar && previewAvatar._rawValue) || state.user.avatar) {
    const url = previewAvatar._rawValue || state.user.avatar;
    const match = url.match(/\/(\d+)\.png/);
    number = match ? (parseInt(match[1], 10) - 1).toString() : "0";
  }

  state.errors = [];
  const toast = useToast();

  const params = {
    first_name: state.user.first_name,
    last_name: state.user.last_name,
    middle_initial: state.user.middle_initial,
    gender: state.user.gender,
    phone_number: state.user.phone_number,
    status: state.user.status,
    role: state.user.role,
    password: state.user.password,
    avatar: number,
  };

  console.log(params.status);

  try {
    const response = await $fetch(
      `http://127.0.0.1:8000/api/users/${user.username}`,
      {
        method: "PUT",
        body: params,
        headers: {
          Authorization: `Bearer ${localStorage.getItem("_token")}`, // Use template literals for better readability
        },
      }
    );

    if (response) {
      console.log("Updated successfully:", response);

      load.bool.value = true;
      load.icon.value = "i-lucide-loader-circle";
      load.label.value = "";
      name.value = "success_2";

      setTimeout(() => {
        playSound();
        toast.add({
          title: "Updated Successfully!",
          icon: "i-lucide-circle-check-big",
          timeout: 2500,
          ui: {
            background: "dark:bg-blue-700 bg-blue-300",
            progress: {
              background: "dark:bg-white bg-blue-700 rounded-full",
            },
            ring: "ring-1 ring-blue-700 dark:ring-custom-900",
            default: {
              closeButton: {
                color: "white",
              },
            },
            icon: "text-custom-900",
          },
        });
        load.label.value = "Update";
        load.bool.value = false;
        navigateTo(`/admin/users/${user.username}`);
      }, 800);
    }
  } catch (error: any) {
    load.label.value = "Update";
    load.bool.value = false;

    if (error.response && error.response._data) {
      const backendErrors = error.response._data.message; // Assuming it's a string
      state.errors.push(backendErrors);
    } else {
      state.errors.push("Server Error.");
    }
    console.log("An error occurred:", state.errors);
  }
}

const links = reactive([
  { label: "Users", to: "/admin/users" },
  { label: "Details", to: `/admin/users/${state.user.username}` },
  { label: "Update" },
]);

function resetAvatar() {
  setPreviewAvatar(null);
}

watch(
  () => state.user.username,
  (newUsername) => {
    links[1].to = `/admin/users/${newUsername}`;
  }
);
</script>
