<template>

  <div class="h-auto w-full p-5 gap-5 flex flex-col justify-between">

    <header class="flex justify-between w-full items-center">
      <h1 class="text-lg font-semibold text-custom-800 dark:text-white">Settings</h1>
      <UButton
        class="bg-red-500 dark:bg-red-500 hover:bg-red-600 dark:hover:bg-red-400 text-white dark:text-white rounded"
        label="Logout" icon="i-lucide-log-out" @click="handleLogout" />
    </header>

    <div class="grid grid-cols-2 gap-5 h-auto w-full">

      <div
        class="flex flex-col h-auto max-h-max w-full gap-5 p-10 rounded dark:bg-custom-900 bg-custom-100 border border-custom-300 dark:border-custom-700">

        <div class="flex justify-between items-center">
          <h1 class="font-semibold text-lg">Profile</h1>

          <UButton v-if="user.role === 'client'"
            class="flex cursor-pointer justify-center items-center rounded dark:text-white" label="Edit"
            icon="i-lucide-edit" :to="`/client/settings/${user.username}`" />

          <UButton v-if="user.role === 'admin' || user.role === 'superadmin'"
            class="flex cursor-pointer justify-center items-center rounded dark:text-white" label="Edit"
            icon="i-lucide-edit" :to="`/admin/settings/${user.username}`" />
        </div>

        <hr class="dark:border-custom-700 border-custom-200">

        <div class="flex flex-col gap-10 h-auto w-full">

          <section
            class="w-52 h-52 mx-auto flex flex-col justify-center items-center cursor-default mt-5">

            <img v-if="user.avatar" 
              class="w-full h-full border-4 border-custom-400 dark:border-custom-700 rounded-full" 
              :src="user.avatar">
            <span v-else class="font-black text-[150px] w-full h-full dark:bg-custom-700 bg-custom-400 flex items-center justify-center rounded-full">{{ initial }}</span>
            
            <div class="flex gap-2 mt-2 h-full items-center justify-center">
              <UKbd 
                class="text-center rounded-full" 
                :value="user.status" 
                :class="{
                    'dark:border bg-green-600 dark:border-green-700 text-custom-100 dark:text-green-400 cursor-default px-2 py-1 lowercase': user.status === 'active',
                    'dark:border bg-red-600 dark:border-red-700 text-custom-100 dark:text-red-400 cursor-default px-2 py-1 lowercase': user.status=== 'inactive'
                  }"  />
              <UKbd 
                class="text-center rounded-full px-2 py-1 bg-custom-700 text-custom-100 dark:text-custom-200 dark:bg-custom-900 dark:border dark:border-custom-500"
                :value="user.role" />

            </div>
            
          </section>

          <div class="p-5 dark:bg-custom-800 bg-custom-50 space-y-2">

            <section class="flex justify-between items-center flex-wrap">
              <div class="flex items-center gap-2"> 
                <UIcon name="i-heroicons-user-16-solid" class="h-auto w-7"/>
                <p class="capitalize text-xl font-medium">{{ user.name }}</p>
              </div>

              <div v-if="user.gender === 'female'" class="flex items-center gap-1 rounded-full cursor-default bg-pink-500 dark:bg-pink-500 text-white px-2 py-1"> 
                <UIcon name="i-game-icons-female" class="h-4 w-4"/>
                <p class="capitalize text-xs font-medium">{{ user.gender }}</p>
              </div>

              <div v-else-if="user.gender === 'male'" class="flex items-center gap-1 rounded-full cursor-default bg-blue-500 dark:bg-blue-500 text-white px-2 py-1"> 
                <UIcon name="i-game-icons-male" class="h-4 w-4"/>
                <p class="capitalize text-xs font-medium">{{ user.gender }}</p>
              </div>

              <div v-else>
                Others
              </div>
            </section>

            <section class="flex items-center gap-2"> 
              <UIcon name="i-heroicons-phone-16-solid" class="h-auto w-5"/>
              <p class="capitalize text-base">{{ user.phone_number }}</p>
            </section>

            <section class="flex items-center gap-2"> 
              <UIcon name="i-heroicons-envelope-16-solid" class="h-auto w-5"/>
              <p class="text-base">{{ user.email }}</p>
            </section>

          </div>

          <div 
            v-if="user.role === 'client'"
            class="p-5 dark:bg-custom-800 bg-custom-50 space-y-2 -mt-7">

            <section class="flex items-center gap-2"> 
              <h1 class="font-medium">Username:</h1>
              <p class="text-base">{{ user.username }}</p>
            </section>

            <section class="flex justify-between items-center"> 
              <div class="flex gap-2">
                <h1 class="font-medium">Password:</h1>
                <!-- dli ma display ang password kay naka hashed (for safety) pero kung dli i-hashed kay ma retrieve-->
                <!-- <p class="text-base">{{ passwordDisplay }}</p>  -->
                <p class="text-base">********</p> 
              </div>
              <!-- <button @click="togglePasswordVisibility" class="text-blue-500 underline">
                {{ isPasswordVisible ? 'Hide' : 'Show' }}
              </button> -->
            </section>
          </div>
        </div>

      </div>

      <div class="flex flex-col gap-5 h-auto w-full">

        <section
          v-if="user.role === 'client'"
          class="h-auto w-full dark:bg-custom-900 bg-custom-100 flex flex-col gap-5 p-10 rounded border border-custom-300 dark:border-custom-700">
          <div class="flex justify-between items-center">
            <h1 class="font-semibold text-lg">Phone Associated</h1>
            <span>
              <UButton 
                @click="isOpen = true" 
                icon="i-iconoir-phone-plus" 
                label="Add phone" 
                class="rounded dark:text-white" 
                size="xs"/>
            </span>
          </div>

          <UForm 
            v-show="isOpen" 
            :state="state" 
            @submit="onSubmit" 
            :validate="validate"
            @error="onError" 
            class="space-y-2 flex items-center">

          <div class="flex flex-col gap-2 p-5 dark:bg-custom-800 bg-custom-50 w-full h-auto">
            <UFormGroup
              class="grid gap-2" 
              name="phone" 
              :ui="{ error: 'mt-1' }">

              <template #label>
                <div class="flex items-center justify-start gap-1">
                  <UIcon 
                    name="i-lucide-phone" 
                    class="text-lg" />
                  <p class="text-base">Phone Number <span class="font-bold text-red-700 dark:text-red-400">(max: 3 phone no.)</span></p>
                </div>
              </template>

              <template #default="{ error }">
                <UInput 
                class="w-full"
                v-model="state.phone"
                color="gray" 
                size="xs"
                  :trailing-icon="error ? 'i-heroicons-exclamation-triangle-20-solid' : undefined" 
                  :ui="{
                    rounded: 'rounded',
                    color: error ?
                      { red: { outline: 'bg-red-100 dark:bg-red-50 text-custom-900 dark:text-custom-900 focus:ring-1 focus:ring-red-400 border-2 border-red-400 focus:border-red-400 active:ring-red-400 active:border-red-400' } } : 
                      { gray: { outline: 'dark:bg-custom-100 dark:text-custom-900' } }
                  }" />
              </template>

              <template #error="{ error }">
                <span
                  :class="[error ? 'text-red-500 dark:text-red-400 text-xs font-bold' : 'text-primary-500 dark:text-primary-400']">
                  {{ error ? error : undefined }}
                </span>
              </template>
            </UFormGroup>

            <div class="flex gap-2 items-center w-full">
              <span class="w-full">
                <UButton 
                  type="submit" 
                  :label="save.label.value" 
                  :loading="save.bool.value" 
                  :loading-icon="save.icon.value" 
                  size="xs" 
                  class="rounded dark:text-white dark:bg-green-500 bg-green-500 hover:bg-green-600 hover:dark:bg-green-600 flex justify-center w-full"/>
              </span>

              <span class="w-full">
                <UButton 
                  @click="isOpen = false" 
                  label="Cancel"
                  size="xs"
                  class="rounded dark:bg-red-500 dark:text-white bg-red-500 hover:bg-red-600 dark:hover:bg-red-600 flex justify-center w-full"/>
              </span>
            </div>
          </div>
            
          </UForm>

          <hr class="dark:border-custom-700 border-custom-200">

          <p class="text-sm text-custom-500 dark:text-custom-300 -mt-3">Selected phone numbers will receive an SMS notification.</p>
          
          <div v-for="(phone, index) in phones" :key="index" class="border-b dark:border-b-custom-950 rounded-lg border-b-custom-200 pb-2">
            <div class="px-2 flex justify-between items-center">
              <UCheckbox 
                :label="phone.number" 
                v-model="phone.selected" 
                color="green"/>
                <UTooltip 
                text="Remove" 
                :popper="{ placement: 'left-start', arrow: true }">

                <UIcon 
                  @click="remove(phone)"
                  name="i-lucide-trash-2" 
                  class="cursor-pointer hover:text-red-500"/>
              </UTooltip>
            </div>

            
          </div>

        </section>
        
        <section
          v-if="user.role === 'admin' || user.role === 'superadmin'"
          class="h-auto w-full dark:bg-custom-900 bg-custom-100 flex flex-col gap-5 p-10 rounded border border-custom-300 dark:border-custom-700">
          <h1 class="font-semibold text-lg">Login Credentials</h1>
          <hr class="dark:border-custom-700 border-custom-200">
          <div class="space-y-2">
            <section class="flex gap-2">
              <h1 class="font-medium">username:</h1>
              <p>{{ user.username }}</p>
            </section>
            <section class="flex justify-between items-center"> 
              <div class="flex gap-2">
                <h1 class="font-medium">Password:</h1>
                <!-- dli ma display ang password kay naka hashed (for safety) pero kung dli i-hashed kay ma retrieve-->
                <!-- <p class="text-base">{{ passwordDisplay }}</p>  -->
                <p class="text-base">********</p> 
              </div>
              <!-- <button @click="togglePasswordVisibility" class="text-blue-500 underline">
                {{ isPasswordVisible ? 'Hide' : 'Show' }}
              </button> -->
            </section>
          </div>
        </section>

        <section
          class="h-auto w-full dark:bg-custom-900 bg-custom-100 flex flex-col gap-5 p-10 rounded border border-custom-300 dark:border-custom-700">
          <h1 class="font-semibold text-lg">Timestamps (date & time)</h1>
          <hr class="dark:border-custom-700 border-custom-200">
          <div class="space-y-2">
            <section class="flex gap-2">
              <h1 class="font-medium">Account created:</h1>
              <p>{{ formatDate(user.created_at) }}</p>
            </section>
            <section class="flex gap-2">
              <h1 class="font-medium">Account updated:</h1>
              <p>{{ formatDate(user.updated_at) }}</p>
            </section>
          </div>
        </section>

      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">

definePageMeta({
  layout: 'sidebar'
})

import type { FormError, FormErrorEvent, FormSubmitEvent } from '#ui/types'
import { user, initial } from '~/assets/js/userLogged';
import { name, playSound } from '~/assets/js/sound'
import { formatDate } from '~/assets/js/formatDate';

// const isPasswordVisible = ref(false);

// // Computed property to show either the masked or full password
// const passwordDisplay = computed(() => {
//   if (isPasswordVisible.value) {
//     return user.password; // Show full password
//   }
//   // Mask the password: Show the first 3 and last characters, and replace the middle with asterisks
//   return user.password ? user.password.substring(0, 3) + '****' + user.password.slice(-1) : '';
// });

// // Function to toggle password visibility
// const togglePasswordVisibility = () => {
//   isPasswordVisible.value = !isPasswordVisible.value;
// };

interface Phone {
  number: string;
  selected: boolean;
}

const phones = ref<Phone[]>([
  {
    number: '+631276217636',
    selected: true,
  },
  {
    number: '+631845884734',
    selected: false,
  },
]);

const remove = (phone: Phone) => {
  if (confirm('Remove this phone number?') === true) {

    phones.value = phones.value.filter(p => p.number !== phone.number);

    name.value = 'delete_1';
    toast.add({
      title: 'Removed Successfully!',
      icon: 'i-lucide-trash-2',
      timeout: 2000,
      ui: {
        background: 'dark:bg-red-700 bg-red-300',
        progress: { background: 'dark:bg-white bg-red-700 rounded-full' },
        ring: 'ring-1 ring-red-700 dark:ring-custom-900',
        default: { closeButton: { color: 'white' } },
        icon: 'text-custom-900',
      },
    });
    playSound();
  } else {
    console.log('Cancelled.')
  }
};

const state = reactive({
  phone: ''
})

const validate = (state: any): FormError[] => {
  const errors = []
  if (!state.phone) errors.push({ path: 'phone', message: 'Required' })
  return errors
}

const isOpen = ref(false);

const save = {
  bool: ref(false),
  label: ref('Save'),
  icon: ref('')
}

async function onSubmit(event: FormSubmitEvent<any>) {
  // Do something with data
  console.log(event.data)
  name.value = 'success_2'
  save.bool.value = true;
  save.icon.value = 'i-lucide-loader-circle';
  save.label.value = '';

  setTimeout(() => {

    phones.value.push({
      number: state.phone,   // Use the phone number from the form state
      selected: true,       // Default selected (you can change this as needed)
    });

    toast.add({
      title: 'Phone Added Successfully!',
      icon: 'i-iconoir-phone-plus',
      timeout: 2000,
      ui: {
        background : 'dark:bg-green-700 bg-green-300', 
        progress: {
          background: 'dark:bg-white bg-green-700 rounded-full'
        }, 
        ring: 'ring-1 ring-green-700 dark:ring-custom-900',
        default: {
          closeButton: { 
            color: 'white',
          }
        },
        icon: 'text-custom-900'
      },
    })

    state.phone = ''

    playSound()
    save.label.value = 'Save';
    save.bool.value = false;
    isOpen.value = false;
    navigateTo('/client/settings/test')
  }, 800)
}

async function onError(event: FormErrorEvent) {
  const element = document.getElementById(event.errors[0].id)
  element?.focus()
  element?.scrollIntoView({ behavior: 'smooth', block: 'center' })
}

const toast = useToast()
name.value = 'logoff_1'

const handleLogout = () => {
  if (confirm("You would like to log out?") == true) {

    playSound()

    toast.add({
      title: 'Logout Successfully!',
      icon: 'i-lucide-log-out',
      timeout: 2000,
      ui: {
        background: 'dark:bg-orange-700 bg-orange-300',
        progress: {
          background: 'dark:bg-white bg-orange-700 rounded-full'
        },
        ring: 'ring-1 ring-orange-700 dark:ring-custom-900',
        default: {
          closeButton: {
            color: 'white',
          }
        },
        icon: 'text-custom-900'
      },
    })

    navigateTo('/auth')
  } else {
    console.log('Cancelled.')
  }
}
</script>