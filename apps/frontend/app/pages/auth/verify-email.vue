<script setup lang="ts">
definePageMeta({ layout: false, ssr: false })
useSeoMeta({ title: 'Подтверждение email — MyApp' })

const route = useRoute()
const router = useRouter()

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
      body: { token },
    })
    status.value = 'success'
  }
  catch (e: unknown) {
    const err = e as { data?: { detail?: string } }
    status.value = 'error'
    errorMessage.value = err?.data?.detail ?? 'Недействительная или устаревшая ссылка.'
  }
})
</script>

<template>
  <div class="auth-page">
    <div class="auth-card glass-card">
      <NuxtLink to="/" class="logo-mark mb-6 inline-flex">
        <span class="logo-icon">◈</span>
        <span class="logo-text">MyApp</span>
      </NuxtLink>

      <!-- Loading -->
      <div v-if="status === 'loading'" class="state-block">
        <div class="spinner" />
        <p class="state-text">Проверяем токен…</p>
      </div>

      <!-- Success -->
      <div v-else-if="status === 'success'" class="state-block">
        <div class="state-icon success">✓</div>
        <h2 class="auth-title">Email подтверждён!</h2>
        <p class="auth-sub">Ваш аккаунт активирован. Можете войти.</p>
        <NuxtLink to="/auth/login" class="btn-primary btn-block mt-6">
          Войти
        </NuxtLink>
      </div>

      <!-- Error -->
      <div v-else class="state-block">
        <div class="state-icon error">✗</div>
        <h2 class="auth-title">Ошибка подтверждения</h2>
        <p class="auth-sub">{{ errorMessage }}</p>
        <NuxtLink to="/auth/register" class="btn-primary btn-block mt-6">
          Зарегистрироваться снова
        </NuxtLink>
      </div>
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
.state-block { text-align: center; }
.state-icon  { font-size: 3rem; margin-bottom: 1rem; width: 4rem; height: 4rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; }
.state-icon.success { background: rgba(34,197,94,.15); color: #4ade80; border: 1px solid rgba(34,197,94,.3); }
.state-icon.error   { background: rgba(239,68,68,.15); color: #f87171; border: 1px solid rgba(239,68,68,.3); }
.auth-title { font-size: 1.6rem; font-weight: 750; letter-spacing: -.03em; color: #fff; margin-bottom: .4rem; }
.auth-sub   { font-size: .9rem; color: rgba(255,255,255,.5); }
.spinner {
  width: 40px; height: 40px;
  border: 3px solid rgba(139,92,246,.2);
  border-top-color: #8b5cf6;
  border-radius: 50%;
  animation: spin .8s linear infinite;
  margin: 0 auto 1rem;
}
@keyframes spin { to { transform: rotate(360deg); } }
.btn-primary {
  padding: .7rem 1.1rem;
  border-radius: .65rem;
  font-size: .95rem;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
  border: 1px solid rgba(139,92,246,.4);
  cursor: pointer;
  transition: filter .2s;
  box-shadow: 0 4px 20px rgba(124,58,237,.35);
}
.btn-primary:hover { filter: brightness(1.12); }
.btn-block { width: 100%; text-align: center; text-decoration: none; display: block; }
.mt-6 { margin-top: 1.5rem; }
</style>
