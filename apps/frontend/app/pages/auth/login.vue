<script setup lang="ts">
import { z } from 'zod'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: false, ssr: false })
useSeoMeta({ title: 'Вход — MyApp' })

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

const auth = useAuthStore()

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
  <div class="auth-page">
    <div class="auth-card glass-card">
      <NuxtLink
        to="/"
        class="logo-mark mb-6 inline-flex"
      >
        <img class="logo-icon" src="/logo-icon.svg" alt="" aria-hidden="true">
        <span class="logo-text">MyApp</span>
      </NuxtLink>

      <h2 class="auth-title">
        Войти в аккаунт
      </h2>
      <p class="auth-sub">
        Нет аккаунта? <NuxtLink
          to="/auth/register"
          class="link"
        >Зарегистрироваться</NuxtLink>
      </p>

      <div
        v-if="showUnverifiedWarning"
        class="warning-block"
      >
        <span class="warning-icon">⚠</span>
        <div>
          <strong>Email не подтверждён.</strong><br>
          Проверьте почту и перейдите по ссылке из письма, чтобы активировать аккаунт.
        </div>
      </div>

      <form
        class="auth-form"
        novalidate
        @submit.prevent="onSubmit"
      >
        <div class="field">
          <label
            class="field-label"
            for="login-email"
          >Email</label>
          <input
            id="login-email"
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
            for="login-password"
          >Пароль</label>
          <input
            id="login-password"
            v-model="form.password"
            type="password"
            autocomplete="current-password"
            placeholder="Ваш пароль"
            class="field-input"
            :class="{ error: errors.password }"
          >
          <span
            v-if="errors.password"
            class="field-error"
          >{{ errors.password }}</span>
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
          <span v-if="submitting">Вход…</span>
          <span v-else>Войти</span>
        </button>
      </form>
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
.warning-block {
  display: flex;
  gap: .75rem;
  align-items: flex-start;
  background: #ffffcc;
  border: 3px solid #ff9900;
  border-radius: 0;
  padding: .85rem 1rem;
  font-size: .88rem;
  color: #cc6600;
  margin-bottom: 1.25rem;
  line-height: 1.5;
  font-weight: 700;
}
.warning-icon { font-size: 1.2rem; flex-shrink: 0; }
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
</style>

