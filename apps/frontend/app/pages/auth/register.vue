<script setup lang="ts">
import { z } from 'zod'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: false, ssr: false })
useSeoMeta({ title: 'Регистрация — MyApp' })

const schema = z.object({
  email: z.string().email('Введите корректный email'),
  password: z.string().min(8, 'Минимум 8 символов'),
  confirm: z.string()
}).refine(d => d.password === d.confirm, {
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

function onAvatarChange(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0] ?? null
  avatarFile.value = file
  if (file) {
    avatarPreview.value = URL.createObjectURL(file)
  } else {
    avatarPreview.value = null
  }
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

const auth = useAuthStore()

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
  <div class="auth-page">
    <div class="auth-card glass-card">
      <NuxtLink
        to="/"
        class="logo-mark mb-6 inline-flex"
      >
        <img class="logo-icon" src="/logo-icon.svg" alt="" aria-hidden="true">
        <span class="logo-text">MyApp</span>
      </NuxtLink>

      <template v-if="success">
        <div class="success-block">
          <div class="success-icon">
            ✉
          </div>
          <h2 class="auth-title">
            Проверьте почту
          </h2>
          <p class="auth-sub">
            Мы отправили письмо с подтверждением на <strong>{{ submittedEmail }}</strong>.<br>
            Перейдите по ссылке в письме, чтобы активировать аккаунт.
          </p>
          <NuxtLink
            to="/auth/login"
            class="btn-primary btn-block mt-6"
          >
            Войти
          </NuxtLink>
        </div>
      </template>

      <template v-else>
        <h2 class="auth-title">
          Создать аккаунт
        </h2>
        <p class="auth-sub">
          Уже есть аккаунт? <NuxtLink
            to="/auth/login"
            class="link"
          >Войти</NuxtLink>
        </p>

        <form
          class="auth-form"
          novalidate
          @submit.prevent="onSubmit"
        >
          <!-- Avatar upload -->
          <div class="field avatar-field">
            <label class="field-label">Аватарка (необязательно)</label>
            <label class="avatar-upload-label">
              <div class="avatar-preview">
                <img
                  v-if="avatarPreview"
                  :src="avatarPreview"
                  class="avatar-img"
                  alt="Предпросмотр аватарки"
                >
                <div
                  v-else
                  class="avatar-placeholder"
                >
                  <span class="avatar-plus">+</span>
                  <span class="avatar-hint">Загрузить фото</span>
                </div>
              </div>
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp,image/gif"
                class="avatar-input"
                @change="onAvatarChange"
              >
            </label>
          </div>

          <div class="field">
            <label
              class="field-label"
              for="reg-email"
            >Email</label>
            <input
              id="reg-email"
              v-model.trim="form.email"
              type="email"
              autocomplete="email"
              placeholder="you@example.com"
              class="field-input"
              :class="{ error: errors.email }"
            >
            <span
              v-if="errors.email"
              class="field-error"
            >{{ errors.email }}</span>
          </div>

          <div class="field">
            <label
              class="field-label"
              for="reg-password"
            >Пароль</label>
            <input
              id="reg-password"
              v-model="form.password"
              type="password"
              autocomplete="new-password"
              placeholder="Минимум 8 символов"
              class="field-input"
              :class="{ error: errors.password }"
            >
            <span
              v-if="errors.password"
              class="field-error"
            >{{ errors.password }}</span>
          </div>

          <div class="field">
            <label
              class="field-label"
              for="reg-confirm"
            >Повторите пароль</label>
            <input
              id="reg-confirm"
              v-model="form.confirm"
              type="password"
              autocomplete="new-password"
              placeholder="Повторите пароль"
              class="field-input"
              :class="{ error: errors.confirm }"
            >
            <span
              v-if="errors.confirm"
              class="field-error"
            >{{ errors.confirm }}</span>
          </div>

          <div
            v-if="serverError"
            class="server-error"
          >
            {{ serverError }}
          </div>

          <button
            type="submit"
            class="btn-primary btn-block"
            :disabled="submitting"
          >
            <span v-if="submitting">Регистрация…</span>
            <span v-else>Создать аккаунт</span>
          </button>
        </form>
      </template>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}
.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem 2rem;
  border-radius: 0;
  background: #ffffff;
  backdrop-filter: none;
  border: 4px solid #000;
  box-shadow: 8px 8px 0 rgba(0,0,0,0.1);
}
.logo-mark { display: inline-flex; align-items: center; gap: .5rem; text-decoration: none; font-weight: 900; font-size: 1.2rem; color: #000; }
.logo-icon  { width: 1.3rem; height: 1.3rem; vertical-align: middle; }
.logo-text  { color: #000; }
.auth-title { font-size: 1.6rem; font-weight: 900; letter-spacing: -.03em; color: #000; margin-bottom: .4rem; }
.auth-sub   { font-size: .9rem; color: #333; margin-bottom: 1.75rem; font-weight: 600; }
.link { color: #000; text-decoration: underline; font-weight: 700; }
.link:hover { color: #666; }
.auth-form  { display: flex; flex-direction: column; gap: 1.1rem; }
.field      { display: flex; flex-direction: column; gap: .35rem; }
.field-label { font-size: .8rem; font-weight: 800; color: #000; text-transform: uppercase; letter-spacing: .05em; }
.field-input {
  background: #ffffff;
  border: 3px solid #000;
  border-radius: 0;
  padding: .65rem .9rem;
  color: #000;
  font-size: .95rem;
  outline: none;
  transition: none;
  font-weight: 600;
}
.field-input::placeholder { color: #999; }
.field-input:focus { border-color: #000; box-shadow: inset 0 0 0 2px #ffffcc; }
.field-input.error { border-color: #ff0000; }
.field-error { font-size: .78rem; color: #ff0000; font-weight: 700; }
.server-error {
  background: #ffcccc;
  border: 3px solid #ff0000;
  border-radius: 0;
  padding: .65rem .9rem;
  font-size: .85rem;
  color: #cc0000;
  font-weight: 700;
}
.btn-primary {
  padding: .7rem 1.1rem;
  border-radius: 0;
  font-size: .95rem;
  font-weight: 800;
  color: #fff;
  background: #000;
  border: 3px solid #000;
  cursor: pointer;
  transition: none;
  box-shadow: 4px 4px 0 #ffffcc;
}
.btn-primary:hover:not(:disabled) { 
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 #ffffcc;
}
.btn-primary:disabled { opacity: .6; cursor: not-allowed; }
.btn-block { width: 100%; text-align: center; text-decoration: none; display: block; }
.success-block { text-align: center; }
.success-icon { font-size: 3rem; margin-bottom: 1rem; }
.mt-6 { margin-top: 1.5rem; }

/* Avatar upload */
.avatar-field { align-items: center; }
.avatar-upload-label { cursor: pointer; }
.avatar-preview {
  width: 88px;
  height: 88px;
  border-radius: 0;
  border: 3px dashed #000;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  transition: none;
}
.avatar-upload-label:hover .avatar-preview {
  border-color: #000;
  background: #ffffcc;
}
.avatar-img { width: 100%; height: 100%; object-fit: cover; }
.avatar-placeholder { display: flex; flex-direction: column; align-items: center; gap: .2rem; }
.avatar-plus { font-size: 1.5rem; color: #000; line-height: 1; font-weight: 800; }
.avatar-hint { font-size: .65rem; color: #333; text-align: center; font-weight: 600; }
.avatar-input { display: none; }
</style>

