<script setup lang="ts">
import { z } from 'zod'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: false, ssr: false })
useSeoMeta({ title: 'Регистрация — MyApp' })

const auth = useAuthStore()

const schema = z.object({
  email: z.string().email('Введите корректный email'),
  password: z.string().min(8, 'Минимум 8 символов'),
  confirm: z.string()
}).refine(data => data.password === data.confirm, {
  message: 'Пароли не совпадают',
  path: ['confirm']
})

const form = reactive({ email: '', password: '', confirm: '' })
const errors = reactive({ email: '', password: '', confirm: '' })
const submitting = ref(false)
const serverError = ref('')
const success = ref(false)
const submittedEmail = ref('')
const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string | null>(null)

function onAvatarChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0] ?? null
  avatarFile.value = file
  avatarPreview.value = file ? URL.createObjectURL(file) : null
}

function validate(): boolean {
  errors.email = ''
  errors.password = ''
  errors.confirm = ''
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
  try {
    await auth.register(form.email, form.password, avatarFile.value)
    submittedEmail.value = form.email
    success.value = true
  } catch (e: unknown) {
    const err = e as { data?: { detail?: string } }
    serverError.value = err?.data?.detail ?? 'Ошибка регистрации. Попробуйте позже.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-black flex items-center justify-center p-4">
    <div class="bg-green-400 text-black p-8 border-4 border-black shadow-[4px_4px_0px_0px_#000] max-w-md w-full">
      <NuxtLink to="/" class="text-black text-2xl font-black mb-6 block text-center">MYAPP</NuxtLink>

      <template v-if="success">
        <div class="text-center">
          <div class="text-6xl mb-4">✉</div>
          <h2 class="text-3xl font-black mb-4">Проверьте почту</h2>
          <p class="text-lg font-bold mb-6">
            Мы отправили письмо на <strong>{{ submittedEmail }}</strong>.<br />Перейдите по ссылке в письме, чтобы активировать аккаунт.
          </p>
          <NuxtLink
            to="/auth/login"
            class="bg-blue-500 text-white px-8 py-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black text-xl hover:bg-blue-600 inline-block"
          >Войти</NuxtLink>
        </div>
      </template>

      <template v-else>
        <h2 class="text-3xl font-black mb-2 text-center">Создать аккаунт</h2>
        <p class="text-lg font-bold mb-6 text-center">
          Уже есть аккаунт? <NuxtLink to="/auth/login" class="text-red-500 font-black">Войти</NuxtLink>
        </p>

        <form class="space-y-6" novalidate @submit.prevent="onSubmit">
          <div>
            <label class="block text-lg font-black mb-2">Аватарка (необязательно)</label>
            <label class="block cursor-pointer">
              <div class="bg-white text-black border-4 border-black p-4 shadow-[4px_4px_0px_0px_#000] text-center">
                <img
                  v-if="avatarPreview"
                  :src="avatarPreview"
                  alt="Предпросмотр аватарки"
                  class="w-16 h-16 rounded-full mx-auto mb-2 border-2 border-black"
                />
                <div v-else class="text-4xl mb-2">+</div>
                <div class="font-black">Загрузить фото</div>
              </div>
              <input type="file" accept="image/jpeg,image/png,image/webp,image/gif" class="hidden" @change="onAvatarChange" />
            </label>
          </div>

          <div>
            <label class="block text-lg font-black mb-2" for="register-email">EMAIL</label>
            <input
              id="register-email"
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
            <label class="block text-lg font-black mb-2" for="register-password">ПАРОЛЬ</label>
            <input
              id="register-password"
              v-model="form.password"
              type="password"
              autocomplete="new-password"
              placeholder="Минимум 8 символов"
              class="w-full bg-white text-black border-4 border-black p-4 text-lg font-bold shadow-[4px_4px_0px_0px_#000] focus:bg-gray-100"
              :class="{ 'border-red-500': errors.password }"
            />
            <span v-if="errors.password" class="block text-red-500 font-black mt-2">{{ errors.password }}</span>
          </div>

          <div>
            <label class="block text-lg font-black mb-2" for="register-confirm">ПОДТВЕРДИТЬ ПАРОЛЬ</label>
            <input
              id="register-confirm"
              v-model="form.confirm"
              type="password"
              autocomplete="new-password"
              placeholder="Повторите пароль"
              class="w-full bg-white text-black border-4 border-black p-4 text-lg font-bold shadow-[4px_4px_0px_0px_#000] focus:bg-gray-100"
              :class="{ 'border-red-500': errors.confirm }"
            />
            <span v-if="errors.confirm" class="block text-red-500 font-black mt-2">{{ errors.confirm }}</span>
          </div>

          <div v-if="serverError" class="bg-red-500 text-white p-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-bold">{{ serverError }}</div>

          <button
            type="submit"
            class="w-full bg-purple-500 text-white p-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black text-xl hover:bg-purple-600 disabled:opacity-60"
            :disabled="submitting"
          >
            <span v-if="submitting">Создание…</span>
            <span v-else>Создать аккаунт</span>
          </button>
        </form>
      </template>
    </div>
  </div>
</template>
