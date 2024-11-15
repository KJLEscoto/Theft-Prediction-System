<template>
  <UseHead title="Email - Auth" description="Email verification." />

  <div class="flex justify-center items-center h-screen w-auto">
    <ToggleDarkMode
      class="fixed sm:top-20 z-50 top-3 left-3 sm:left-20 duration-200"
    />

    <UForm
      :state="state"
      @submit="onSubmit"
      :validate="validate"
      @error="onError"
      class="h-auto w-[500px] flex flex-col gap-4 rounded p-8 bg-custom-50 dark:bg-custom-900 shadow-lg border dark:border-custom-700 border-custom-300"
    >
      <header>
        <div class="flex items-center justify-end">
          <UButton
            icon="i-lucide-x"
            to="/auth/otp"
            class="flex justify-center items-center text-sm rounded-full dark:bg-red-600 dark:hover:bg-red-600/75 bg-red-600 hover:bg-red-600/75 dark:text-custom-100"
            size="2xs"
          />
        </div>
        <div class="flex justify-center items-center gap-1">
          <UIcon name="i-lucide-mail" class="text-3xl" />
          <h1 class="text-2xl font-bold cursor-default">Email Verification</h1>
        </div>
      </header>

      <hr class="border-custom-300 dark:border-custom-500" />

      <!-- display other errors here -->
      <div v-if="state.errors.length">
        <ul>
          <li
            v-for="(error, index) in state.errors"
            :key="index"
            class="text-red-500 dark:text-red-400 text-lg font-bold text-center truncate"
          >
          <UTooltip class="truncate" :text="error" :popper="{ arrow: true, placement: 'right' }" :ui="{ base: 'text-ellipsis text-wrap text-start h-auto'  }">
            <span>{{ error }}</span>
          </UTooltip>
          </li>
        </ul>
      </div>

      <!-- otp -->
      <UFormGroup
        class="flex flex-col gap-1"
        name="otp"
        :ui="{ error: 'mt-1', label: '' }"
      >
        <template #label>
          <div class="flex flex-col justify-center mb-2 items-center w-full">
            <p class="font-normal">
              Enter the code from the <strong>Email</strong> we sent to
            </p>
            <span
              v-if="
                !user.role ||
                !['client', 'admin', 'superadmin'].includes(user.role) ||
                !user.email
              "
            >
              <UIcon
                class="animate-spin text-center"
                name="i-heroicons-arrow-path-solid"
              />
            </span>
            <p
              v-else
              class="font-medium text-base italic text-blue-700 dark:text-blue-500"
            >
              {{ user.email }}
            </p>
          </div>
        </template>

        <template #default="{ error }">
          <UInput
            v-model="state.otp"
            placeholder="6-digit code"
            type="text"
            color="gray"
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
            {{ error ? error : "" }}
          </span>
        </template>
      </UFormGroup>

      <UButton
        type="submit"
        :label="submit.label.value"
        :loading-icon="submit.icon.value"
        :loading="submit.bool.value"
        class="flex justify-center items-center gap-1 py-2 rounded dark:text-custom-50 dark:bg-custom-500 hover:dark:bg-custom-500/75"
      />
    </UForm>
  </div>
</template>

<script setup lang="ts">
import type { FormError, FormErrorEvent, FormSubmitEvent } from "#ui/types";
import { name, playSound } from "~/assets/js/sound";
import { user, fetchUser } from "~/assets/js/userLogged";

let securedOtp = "";

const submit = {
  bool: ref(false),
  label: ref("Submit"),
  icon: ref(""),
};

const state = reactive({
  errors: [] as string[],
  otp: "",
  email: "",
});

const validate = (state: any): FormError[] => {
  const errors = [];
  if (!state.otp) errors.push({ path: "otp", message: "Required" });
  return errors;
};

const loadUser = async () => {
  await fetchUser();
  state.email = user.email;
  console.log(user);

  sendOTP();
};

const sendOTP = async () => {
  console.log("Sending OTP...");

  const params = {
    email: state.email,
  };

  interface Response {
    status: string;
    otp: string;
  }

  try {
    const response = await $fetch<Response>(
      `http://127.0.0.1:8000/api/otp-email`,
      {
        method: "POST",
        body: params,
      }
    );

    if (response && response.status === "success") {
      // console.log(response)
      // console.log(params);

      securedOtp = response.otp; // Store the OTP in the state
      console.log("OTP:", securedOtp);
    } else {
      console.log("Error sending OTP. Please try again.");
    }
  } catch (error: any) {
    submit.label.value = "Login";
    submit.bool.value = false;

    if (error.response && error.response._data) {
      const backendErrors = error.response._data.message; // Assuming it's a string
      state.errors.push(backendErrors);
    } else {
      state.errors.push("Server Error.");
    }
    console.log("An error occurred:", state.errors);
  }
};

async function onSubmit(event: FormSubmitEvent<any>) {
  state.errors = [];

  if (securedOtp == state.otp) {
    submit.bool.value = true;
    submit.icon.value = "i-lucide-loader-circle";
    submit.label.value = "";

    const toast = useToast();
    name.value = "login_1";

    const showToast = () => {
      playSound();

      toast.add({
        title: "Login Successfully!",
        icon: "i-lucide-log-in",
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
    };

    setTimeout(() => {
      if (user.role === "client") {
        showToast();
        navigateTo("/client/monitor");
      } else if (user.role === "admin" || user.role === "superadmin") {
        showToast();
        navigateTo("/admin/dashboard");
      } else {
        alert("This account has no role. Please contact support.");
      }

      submit.label.value = "Submit";
      submit.bool.value = false;
    }, 800);
  } else {
    state.errors.push("Invalid OTP");
  }
}

async function onError(event: FormErrorEvent) {
  const element = document.getElementById(event.errors[0].id);
  element?.focus();
  element?.scrollIntoView({ behavior: "smooth", block: "center" });
}

onMounted(() => {
  loadUser();
});
</script>
