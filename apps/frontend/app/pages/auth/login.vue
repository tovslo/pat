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
    await navigateTo('/dashboard')
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
        <span class="logo-icon">◈</span>
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
.logo-icon  { color: #8b5cf6; font-size: 1.3rem; }
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
.warning-block {
  display: flex;
  gap: .75rem;
  align-items: flex-start;
  background: rgba(245,158,11,.1);
  border: 1px solid rgba(245,158,11,.3);
  border-radius: .75rem;
  padding: .85rem 1rem;
  font-size: .88rem;
  color: #fcd34d;
  margin-bottom: 1.25rem;
  line-height: 1.5;
}
.warning-icon { font-size: 1.2rem; flex-shrink: 0; }
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
</style>
