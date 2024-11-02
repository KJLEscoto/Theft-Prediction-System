<template>

  <UseHead title="Client - Auth" description="Login authentication for client users." />

  <div class="flex justify-center items-center h-screen w-auto">

    <ToggleDarkMode class="fixed sm:top-20 z-50 top-3 left-3 sm:left-20 duration-200" />

    <UForm 
      :state="state" 
      @submit="onSubmit" 
      :validate="validate" 
      @error="onError"
      class="h-auto w-[500px] flex flex-col gap-5 rounded p-8 bg-custom-50 dark:bg-custom-900 shadow-lg border dark:border-custom-700 border-custom-300">

      <header class="flex items-center justify-center gap-1">
        <UIcon 
          name="i-lucide-shield-check" 
          class="text-3xl" />
        <h1 class="text-2xl font-bold cursor-default">Authentication</h1>
      </header>

      <hr class="border-custom-300 dark:border-custom-500">

      <!-- display other errors here -->
      <div v-if="state.errors.length">
        <ul>
          <li v-for="(error, index) in state.errors" :key="index" class="text-red-500 dark:text-red-400 text-lg font-bold text-center truncate">
            {{ error }}
          </li>
        </ul>
      </div>

      <!-- username -->
      <UFormGroup 
        class="grid gap-1" 
        name="username" 
        :ui="{ error: 'mt-1' }">

        <template #label>
          <div class="flex items-center justify-start gap-1 mb-1">
            <UIcon 
              name="i-lucide-user-round" 
              class="text-lg" />
            <p class="text-base">Username</p>
          </div>
        </template>

        <template #default="{ error }">
          <UInput 
            v-model="state.user.username" 
            placeholder="Username"
            type="text" 
            color="gray" 
            size="md"
            :ui="{
              rounded: 'rounded',
              color: error ?
                { red: { outline: 'dark:bg-red-50 bg-red-100 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400' } } : 
                { gray: { outline: 'dark:bg-custom-100 dark:text-custom-900 border-none' } }
            }" />
        </template>

        <template #error="{ error }">
          <span
            :class="[error ? 'text-red-500 dark:text-red-400 text-xs font-bold' : 'text-primary-500 dark:text-primary-400']">
            {{ error ? error : undefined }}
          </span>
        </template>
      </UFormGroup>

      <!-- password -->
      <UFormGroup 
        class="grid gap-1" 
        name="password" 
        :ui="{ error: 'mt-1' }">

        <template #label>
          <div class="flex items-center justify-start gap-1 mb-1">
            <UIcon 
              name="i-lucide-key-round" 
              class="text-lg" />
            <p class="text-base">Password</p>
          </div>
        </template>

        <template #default="{ error }">
          <div class="relative w-full">

            <!-- Show/Hide Icon -->
            <div 
              class="flex gap-1 items-center absolute z-10 right-2 top-[10px] pr-1 cursor-pointer dark:text-black" 
              @click="togglePassword">
              <UTooltip :text="isPasswordVisible ? 'Hide Password' : 'Show Password'" 
              :popper="{ arrow: true }" 
              :ui="{ background: 'dark:bg-custom-800 bg-custom-50', arrow: { background: 'dark:before:bg-custom-950 before:bg-custom-300'}}" >
                <UIcon :name="isPasswordVisible ? 'i-fluent-eye-off-24-filled' : 'i-fluent-eye-12-filled'" />
              </UTooltip>
            </div>

            <UInput 
              v-model="state.user.password" 
              :type="isPasswordVisible ? 'text' : 'password'" 
              color="gray" 
              placeholder="Password"
              size="md"
              :ui="{
                rounded: 'rounded',
                color: error ?
                  { red: { outline: 'dark:bg-red-50 bg-red-100 pr-10 dark:text-custom-900 focus:ring-2 ring-1 ring-red-400 focus:ring-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400' } } : 
                  { gray: { outline: 'dark:bg-custom-100 dark:text-custom-900 pr-10 border-none' } }
              }" />
            </div>
          </template>

        <template #error="{ error }">
          <span
            :class="[error ? 'text-red-500 dark:text-red-400 text-xs font-bold' : 'text-primary-500 dark:text-primary-400']">
            {{ error ? error : undefined }}
          </span>
        </template>
      </UFormGroup>

      <UButton 
        type="submit" 
        :label="load.label.value" 
        :loading-icon="load.icon.value" 
        :loading="load.bool.value"
        class="flex justify-center items-center gap-1 py-2 rounded dark:text-custom-50 dark:bg-custom-500 hover:dark:bg-custom-500/75" />

      <Divider />

      <UButton 
        to="/auth/admin" 
        label="Continue as Admin" 
        icon="i-lucide-circle-user-round"
        class="flex justify-center items-center gap-1 py-3 rounded bg-custom-700 hover:bg-custom-800 dark:bg-custom-700 hover:dark:bg-custom-700/75 dark:text-custom-50" />

    </UForm>
  </div>
</template>

<script setup lang="ts">
import type { FormError, FormErrorEvent, FormSubmitEvent } from '#ui/types';
import { isPasswordVisible, togglePassword } from '~/assets/js/showPassword';

const state = reactive({
  errors: [] as string[],
  user: {
    username: '',
    password: ''
  }
})

const load = {
  bool: ref(false),
  label: ref('Login'),
  icon: ref('')
}

const validate = (state: any): FormError[] => {
  const errors = []
  if (!state.user.username) errors.push({ path: 'username', message: 'Required' })
  if (!state.user.password) errors.push({ path: 'password', message: 'Required' })
  return errors
}

async function onError(event: FormErrorEvent) {
  const element = document.getElementById(event.errors[0].id)
  element?.focus()
  element?.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

async function onSubmit(event: FormSubmitEvent<any>) {
  // Clear previous errors
  state.errors = []; 

  load.bool.value = true;
  load.icon.value = 'i-lucide-loader-circle';
  load.label.value = '';

  const params = {
    username: state.user.username,
    password: state.user.password
  }

  interface Response {
    data: {
      token: string;
    }
  }

  try {
    const response = await $fetch<Response>(`http://127.0.0.1:8000/api/auth/login`, {
      method: 'POST',
      body: params
    })

    if (response) {
      localStorage.setItem('_token', response.data.token)

      // console.log(response)
      // console.log(params);

      setTimeout(() => {
        load.label.value = 'Login';
        load.bool.value = false;
        navigateTo('/auth/otp')
      }, 500)
    }
  } catch (error: any) {    
    load.label.value = 'Login';
    load.bool.value = false;

    if (error.response && error.response._data) {
      const backendErrors = error.response._data.message; // Assuming it's a string
      state.errors.push(backendErrors);
    } else {      
      state.errors.push('Server Error.');
    }
    console.log("An error occurred:", state.errors);
  }
}


</script>
