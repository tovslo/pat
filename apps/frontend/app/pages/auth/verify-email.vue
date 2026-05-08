<script setup lang="ts">
definePageMeta({ layout: false, ssr: false })
useSeoMeta({ title: 'Подтверждение email — MyApp' })

const route = useRoute()

const status = ref<'loading' | 'success' | 'error'>('loading')
const errorMessage = ref('')

onMounted(async () => {
  const token = route.query.token as string | undefined
  if (!token) {
    status.value = 'error'
    errorMessage.value = 'Токен подтверждения отсутствует.'
    return
  }
  try {
    await $fetch('/api/v1/auth/verify-email', {
      method: 'POST',
      body: { token }
    })
    status.value = 'success'
  } catch (e: unknown) {
    const err = e as { data?: { detail?: string } }
    status.value = 'error'
    errorMessage.value = err?.data?.detail ?? 'Недействительная или устаревшая ссылка.'
  }
})
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

      <!-- Loading -->
      <div
        v-if="status === 'loading'"
        class="state-block"
      >
        <div class="spinner" />
        <p class="state-text">
          Проверяем токен…
        </p>
      </div>

      <!-- Success -->
      <div
        v-else-if="status === 'success'"
        class="state-block"
      >
        <div class="state-icon success">
          ✓
        </div>
        <h2 class="auth-title">
          Email подтверждён!
        </h2>
        <p class="auth-sub">
          Ваш аккаунт активирован. Можете войти.
        </p>
        <NuxtLink
          to="/auth/login"
          class="btn-primary btn-block mt-6"
        >
          Войти
        </NuxtLink>
      </div>

      <!-- Error -->
      <div
        v-else
        class="state-block"
      >
        <div class="state-icon error">
          ✗
        </div>
        <h2 class="auth-title">
          Ошибка подтверждения
        </h2>
        <p class="auth-sub">
          {{ errorMessage }}
        </p>
        <NuxtLink
          to="/auth/register"
          class="btn-primary btn-block mt-6"
        >
          Зарегистрироваться снова
        </NuxtLink>
      </div>
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
.state-block { text-align: center; }
.state-icon  { font-size: 3rem; margin-bottom: 1rem; width: 4rem; height: 4rem; border-radius: 0; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; }
.state-icon.success { background: #ccffcc; color: #009900; border: 3px solid #009900; }
.state-icon.error   { background: #ffcccc; color: #cc0000; border: 3px solid #ff0000; }
.auth-title { font-size: 1.6rem; font-weight: 900; letter-spacing: -.03em; color: #000; margin-bottom: .4rem; }
.auth-sub   { font-size: .9rem; color: #333; font-weight: 600; }
.spinner {
  width: 40px; height: 40px;
  border: 4px solid #000;
  border-top-color: #ffffcc;
  border-radius: 0;
  animation: spin .8s linear infinite;
  margin: 0 auto 1rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
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
.btn-primary:hover { 
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 #ffffcc;
}
.btn-block { width: 100%; text-align: center; text-decoration: none; display: block; }
.mt-6 { margin-top: 1.5rem; }
</style>
