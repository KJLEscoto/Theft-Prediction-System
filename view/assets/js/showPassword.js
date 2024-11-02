export const isPasswordVisible = ref(false)

export function togglePassword() {
    isPasswordVisible.value = !isPasswordVisible.value;
}