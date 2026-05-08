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
  <div class="min-h-screen bg-black flex items-center justify-center p-4">
    <div class="bg-purple-500 text-black p-8 border-4 border-black shadow-[4px_4px_0px_0px_#000] max-w-md w-full text-center">
      <NuxtLink to="/" class="text-black text-2xl font-black mb-6 block">MYAPP</NuxtLink>

      <div v-if="status === 'loading'" class="space-y-4">
        <div class="text-6xl mb-4 animate-spin">⟳</div>
        <p class="text-lg font-bold">Проверяем токен…</p>
      </div>

      <div v-else-if="status === 'success'" class="space-y-4">
        <div class="text-6xl mb-4 text-green-500">✓</div>
        <h2 class="text-3xl font-black mb-4">Email подтверждён!</h2>
        <p class="text-lg font-bold mb-6">Ваш аккаунт активирован. Можете войти.</p>
        <NuxtLink
          to="/auth/login"
          class="bg-blue-500 text-white px-8 py-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black text-xl hover:bg-blue-600 inline-block"
        >Войти</NuxtLink>
      </div>

      <div v-else class="space-y-4">
        <div class="text-6xl mb-4 text-red-500">✗</div>
        <h2 class="text-3xl font-black mb-4">Ошибка подтверждения</h2>
        <p class="text-lg font-bold mb-6">{{ errorMessage }}</p>
        <NuxtLink
          to="/auth/register"
          class="bg-red-500 text-white px-8 py-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black text-xl hover:bg-red-600 inline-block"
        >Зарегистрироваться снова</NuxtLink>
      </div>
    </div>
  </div>
</template>
