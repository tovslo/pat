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
  background: #07071a;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}
.auth-card {
  width: 100%;
  max-width: 420px;
  padding: 2.5rem 2rem;
  border-radius: 1.25rem;
  background: rgba(255,255,255,.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,.09);
}
.logo-mark { display: inline-flex; align-items: center; gap: .5rem; text-decoration: none; font-weight: 700; font-size: 1.15rem; color: #fff; }
.logo-icon  { width: 1.3rem; height: 1.3rem; vertical-align: middle; }
.logo-text  { color: #fff; }
.auth-title { font-size: 1.6rem; font-weight: 750; letter-spacing: -.03em; color: #fff; margin-bottom: .4rem; }
.auth-sub   { font-size: .9rem; color: rgba(255,255,255,.5); margin-bottom: 1.75rem; }
.link { color: #a78bfa; text-decoration: none; }
.link:hover { text-decoration: underline; }
.auth-form  { display: flex; flex-direction: column; gap: 1.1rem; }
.field      { display: flex; flex-direction: column; gap: .35rem; }
.field-label { font-size: .8rem; font-weight: 600; color: rgba(255,255,255,.6); text-transform: uppercase; letter-spacing: .05em; }
.field-input {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.12);
  border-radius: .65rem;
  padding: .65rem .9rem;
  color: #fff;
  font-size: .95rem;
  outline: none;
  transition: border-color .2s;
}
.field-input::placeholder { color: rgba(255,255,255,.25); }
.field-input:focus { border-color: rgba(139,92,246,.6); }
.field-input.error { border-color: rgba(239,68,68,.6); }
.field-error { font-size: .78rem; color: #f87171; }
.server-error {
  background: rgba(239,68,68,.12);
  border: 1px solid rgba(239,68,68,.25);
  border-radius: .65rem;
  padding: .65rem .9rem;
  font-size: .85rem;
  color: #f87171;
}
.btn-primary {
  padding: .7rem 1.1rem;
  border-radius: .65rem;
  font-size: .95rem;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
  border: 1px solid rgba(139,92,246,.4);
  cursor: pointer;
  transition: filter .2s, transform .15s;
  box-shadow: 0 4px 20px rgba(124,58,237,.35);
}
.btn-primary:hover:not(:disabled) { filter: brightness(1.12); transform: translateY(-1px); }
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
  border-radius: 50%;
  border: 2px dashed rgba(139,92,246,.4);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(139,92,246,.08);
  transition: border-color .2s, background .2s;
}
.avatar-upload-label:hover .avatar-preview {
  border-color: rgba(139,92,246,.8);
  background: rgba(139,92,246,.14);
}
.avatar-img { width: 100%; height: 100%; object-fit: cover; }
.avatar-placeholder { display: flex; flex-direction: column; align-items: center; gap: .2rem; }
.avatar-plus { font-size: 1.5rem; color: rgba(139,92,246,.7); line-height: 1; }
.avatar-hint { font-size: .65rem; color: rgba(255,255,255,.4); text-align: center; }
.avatar-input { display: none; }
</style>
