<script setup lang="ts">
import { z } from 'zod'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: false, ssr: false })
useSeoMeta({ title: 'Вход — MyApp' })

const auth = useAuthStore()

const schema = z.object({
  email: z.string().email('Введите корректный email'),
  password: z.string().min(1, 'Введите пароль')
})

const form = reactive({ email: '', password: '' })
const errors = reactive({ email: '', password: '' })
const submitting = ref(false)
const serverError = ref('')
const showUnverifiedWarning = ref(false)

function validate(): boolean {
  errors.email = ''
  errors.password = ''
  const result = schema.safeParse(form)
  if (!result.success) {
    for (const issue of result.error.issues) {
      const field = issue.path[0] as keyof typeof errors
      if (field in errors && !errors[field]) errors[field] = issue.message
    }
    return false
  }
  return true
}

async function onSubmit() {
  if (!validate()) return
  submitting.value = true
  serverError.value = ''
  showUnverifiedWarning.value = false
  try {
    await auth.login(form.email, form.password)
    await navigateTo('/')
  } catch (e: unknown) {
    const err = e as { data?: { detail?: string }, status?: number }
    if (err?.status === 403) {
      showUnverifiedWarning.value = true
    } else if (err?.status === 401) {
      serverError.value = 'Неверный email или пароль.'
    } else {
      serverError.value = err?.data?.detail ?? 'Ошибка входа. Попробуйте позже.'
    }
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-black flex items-center justify-center p-4">
    <div class="bg-yellow-400 text-black p-8 border-4 border-black shadow-[4px_4px_0px_0px_#000] max-w-md w-full">
      <NuxtLink
        to="/"
        class="text-black text-2xl font-black mb-6 block text-center"
      >
        MYAPP
      </NuxtLink>

      <h2 class="text-3xl font-black mb-2 text-center">
        ВОЙТИ В АККАУНТ
      </h2>
      <p class="text-lg font-bold mb-6 text-center">
        Нет аккаунта? <NuxtLink
          to="/auth/register"
          class="text-red-500 font-black"
        >Зарегистрироваться</NuxtLink>
      </p>

      <div
        v-if="showUnverifiedWarning"
        class="bg-red-500 text-white p-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] mb-6 font-bold"
      >
        ⚠ Email не подтверждён. Проверьте почту и перейдите по ссылке из письма.
      </div>

      <form
        class="space-y-6"
        novalidate
        @submit.prevent="onSubmit"
      >
        <div>
          <label class="block text-lg font-black mb-2" for="login-email">EMAIL</label>
          <input
            id="login-email"
            v-model.trim="form.email"
            type="email"
            autocomplete="email"
            placeholder="you@example.com"
            class="w-full bg-white text-black border-4 border-black p-4 text-lg font-bold shadow-[4px_4px_0px_0px_#000] focus:bg-gray-100"
            :class="{ 'border-red-500': errors.email }"
          />
          <span v-if="errors.email" class="block text-red-500 font-black mt-2">{{ errors.email }}</span>
        </div>

        <div>
          <label class="block text-lg font-black mb-2" for="login-password">ПАРОЛЬ</label>
          <input
            id="login-password"
            v-model="form.password"
            type="password"
            autocomplete="current-password"
            placeholder="Ваш пароль"
            class="w-full bg-white text-black border-4 border-black p-4 text-lg font-bold shadow-[4px_4px_0px_0px_#000] focus:bg-gray-100"
            :class="{ 'border-red-500': errors.password }"
          />
          <span v-if="errors.password" class="block text-red-500 font-black mt-2">{{ errors.password }}</span>
        </div>

        <div v-if="serverError" class="bg-red-500 text-white p-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-bold">{{ serverError }}</div>

        <button
          type="submit"
          class="w-full bg-blue-500 text-white p-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black text-xl hover:bg-blue-600 disabled:opacity-60"
          :disabled="submitting"
        >
          <span v-if="submitting">Вход…</span>
          <span v-else>Войти</span>
        </button>
      </form>
    </div>
  </div>
</template>
