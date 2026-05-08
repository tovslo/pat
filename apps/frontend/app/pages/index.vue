<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

definePageMeta({ layout: false })

useSeoMeta({
  title: 'MyApp — ИИ-платформа для документов',
  description: 'Self-hosted платформа для анализа, поиска и автоматизации работы с документами на базе FastAPI и Nuxt 3.'
})

const auth = useAuthStore()

const DEFAULT_AVATAR = 'data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 40 40\'%3E%3Ccircle cx=\'20\' cy=\'20\' r=\'20\' fill=\'%236d28d9\'/%3E%3Ccircle cx=\'20\' cy=\'16\' r=\'7\' fill=\'%23fff\' fill-opacity=\'.85\'/%3E%3Cellipse cx=\'20\' cy=\'36\' rx=\'13\' ry=\'9\' fill=\'%23fff\' fill-opacity=\'.85\'/%3E%3C/svg%3E'

async function handleLogout() {
  await auth.logout()
}

const navLinks = [
  { label: 'Возможности', href: '#features' },
  { label: 'Технологии', href: '#tech' },
  { label: 'Тарифы', href: '#pricing' },
  { label: 'Контакты', href: '#contact' }
]

const features = [
  {
    icon: '🧠',
    title: 'ИИ-анализ документов',
    desc: 'Автоматическое извлечение данных, суммаризация и классификация любых документов с помощью языковых моделей.'
  },
  {
    icon: '⚡',
    title: 'Семантический поиск',
    desc: 'Мгновенный поиск по всему архиву документов. Находит смысл, а не только ключевые слова.'
  },
  {
    icon: '🔒',
    title: 'Полная безопасность',
    desc: 'Self-hosted решение — данные остаются на вашем сервере. Шифрование на каждом уровне.'
  },
  {
    icon: '🔄',
    title: 'Автоматизация задач',
    desc: 'Гибкие пайплайны обработки с Celery + RabbitMQ. Уведомления в реальном времени через WebSocket.'
  },
  {
    icon: '📊',
    title: 'Аналитика и отчёты',
    desc: 'Дашборды с метриками, трендами и экспортом. Grafana + Prometheus из коробки.'
  },
  {
    icon: '🌐',
    title: 'API-first подход',
    desc: 'RESTful API с OpenAPI-документацией. Type-safe клиент из схемы для быстрой интеграции.'
  }
]

const techStack = [
  { label: 'Nuxt 3', color: '#00DC82' },
  { label: 'FastAPI', color: '#059669' },
  { label: 'PostgreSQL', color: '#3b82f6' },
  { label: 'Celery', color: '#8b5cf6' },
  { label: 'RabbitMQ', color: '#f59e0b' },
  { label: 'Docker Swarm', color: '#0ea5e9' },
  { label: 'Traefik', color: '#ec4899' },
  { label: 'Prometheus', color: '#ef4444' }
]

const mobileMenuOpen = ref(false)
</script>

<template>
  <div class="min-h-screen bg-black text-white font-bold">
    <header class="bg-yellow-400 border-b-4 border-black p-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <NuxtLink to="/" class="text-black text-2xl font-black">MYAPP</NuxtLink>

        <nav class="hidden md:flex space-x-8">
          <a
            v-for="link in navLinks"
            :key="link.href"
            :href="link.href"
            class="text-black font-black text-lg hover:bg-red-500 hover:text-white px-4 py-2 border-4 border-black shadow-[4px_4px_0px_0px_#000]"
          >
            {{ link.label }}
          </a>
        </nav>

        <div class="flex items-center space-x-4">
          <div
            v-if="auth.isLoggedIn"
            class="bg-blue-500 text-white px-4 py-2 border-4 border-black shadow-[4px_4px_0px_0px_#000]"
          >
            {{ auth.user?.email }}
          </div>
          <button
            v-if="auth.isLoggedIn"
            class="bg-red-500 text-white px-4 py-2 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black"
            @click="handleLogout"
          >
            ВЫЙТИ
          </button>
          <NuxtLink
            v-else
            to="/auth/login"
            class="bg-green-500 text-white px-4 py-2 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black"
          >ВОЙТИ</NuxtLink>

          <button
            class="md:hidden bg-black text-white p-2 border-4 border-white"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <span class="block w-6 h-1 bg-white mb-1"></span>
            <span class="block w-6 h-1 bg-white mb-1"></span>
            <span class="block w-6 h-1 bg-white"></span>
          </button>
        </div>
      </div>

      <div v-if="mobileMenuOpen" class="md:hidden bg-red-500 border-t-4 border-black p-4">
        <a
          v-for="link in navLinks"
          :key="link.href"
          :href="link.href"
          class="block text-white font-black text-lg py-2 border-b-2 border-black"
          @click="mobileMenuOpen = false"
        >
          {{ link.label }}
        </a>
        <div class="mt-4">
          <NuxtLink
            v-if="!auth.isLoggedIn"
            to="/auth/login"
            class="bg-green-500 text-white px-4 py-2 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black"
          >ВОЙТИ</NuxtLink>
        </div>
      </div>
    </header>

    <section class="bg-black text-white py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <div class="bg-red-500 text-white px-4 py-2 border-4 border-black shadow-[4px_4px_0px_0px_#000] inline-block mb-8 font-black text-lg">
          ✦ ОТКРЫТЫЙ БЕТА-ДОСТУП
        </div>

        <h1 class="text-6xl md:text-8xl font-black mb-8 leading-tight">
          УМНАЯ ОБРАБОТКА<br>
          <span class="text-yellow-400">ДОКУМЕНТОВ С ИИ</span>
        </h1>

        <p class="text-xl md:text-2xl mb-12 font-bold">
          Загружайте, анализируйте и извлекайте данные из любых документов.<br>
          Self-hosted платформа на FastAPI + Nuxt 3, готовая к продакшну.
        </p>

        <div class="flex flex-col md:flex-row gap-4 justify-center">
          <NuxtLink
            to="/auth/register"
            class="bg-blue-500 text-white px-8 py-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black text-xl hover:bg-blue-600"
          >
            НАЧАТЬ БЕСПЛАТНО →
          </NuxtLink>
          <button class="bg-white text-black px-8 py-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black text-xl hover:bg-gray-200">
            СМОТРЕТЬ ДЕМО
          </button>
        </div>
      </div>
    </section>

    <section id="features" class="bg-white text-black py-20 px-4">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <div class="bg-green-500 text-white px-4 py-2 border-4 border-black shadow-[4px_4px_0px_0px_#000] inline-block mb-4 font-black text-lg">
            ВОЗМОЖНОСТИ
          </div>
          <h2 class="text-5xl font-black mb-4">ВСЁ ДЛЯ РАБОТЫ С ДОКУМЕНТАМИ</h2>
          <p class="text-xl font-bold">
            Платформа объединяет ИИ-анализ, семантический поиск<br>и автоматизацию в едином self-hosted решении
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="f in features"
            :key="f.title"
            class="bg-yellow-400 text-black p-8 border-4 border-black shadow-[4px_4px_0px_0px_#000]"
          >
            <div class="text-6xl mb-4">{{ f.icon }}</div>
            <h3 class="text-2xl font-black mb-4">{{ f.title }}</h3>
            <p class="text-lg font-bold">{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <section id="tech" class="bg-black text-white py-20 px-4">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <div class="bg-purple-500 text-white px-4 py-2 border-4 border-black shadow-[4px_4px_0px_0px_#000] inline-block mb-4 font-black text-lg">
            ТЕХНОЛОГИИ
          </div>
          <h2 class="text-5xl font-black mb-4">ПРОВЕРЕННЫЙ СТЕК</h2>
          <p class="text-xl font-bold">Production-ready технологии без избыточных зависимостей</p>
        </div>

        <div class="flex flex-wrap justify-center gap-4">
          <div
            v-for="t in techStack"
            :key="t.label"
            class="bg-white text-black px-6 py-3 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black text-lg"
          >
            <span class="inline-block w-4 h-4 rounded-full mr-2" :style="{ background: t.color }"></span>
            {{ t.label }}
          </div>
        </div>
      </div>
    </section>

    <section id="contact" class="bg-red-500 text-white py-20 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <div class="bg-black text-white px-4 py-2 border-4 border-white shadow-[4px_4px_0px_0px_#fff] inline-block mb-8 font-black text-lg">
          НАЧНИТЕ СЕГОДНЯ
        </div>
        <h2 class="text-5xl font-black mb-4">ГОТОВЫ К ЗАПУСКУ?</h2>
        <p class="text-xl font-bold mb-12">
          Разверните платформу на своём сервере за 5 минут.<br>
          Полный контроль над данными, без vendor lock-in.
        </p>
        <div class="flex flex-col md:flex-row gap-4 justify-center">
          <NuxtLink
            to="/auth/register"
            class="bg-yellow-400 text-black px-8 py-4 border-4 border-black shadow-[4px_4px_0px_0px_#000] font-black text-xl hover:bg-yellow-500"
          >ПОЛУЧИТЬ ДОСТУП</NuxtLink>
          <button class="bg-black text-white px-8 py-4 border-4 border-white shadow-[4px_4px_0px_0px_#fff] font-black text-xl hover:bg-gray-800">
            ДОКУМЕНТАЦИЯ
          </button>
        </div>
      </div>
    </section>

    <footer class="bg-black text-white py-12 px-4 border-t-4 border-white">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div>
            <div class="text-2xl font-black mb-4">MYAPP</div>
            <p class="font-bold">Современная ИИ-платформа<br>для работы с документами</p>
          </div>

          <div>
            <h4 class="text-xl font-black mb-4">ПРОДУКТ</h4>
            <ul class="space-y-2 font-bold">
              <li><a href="#features" class="hover:text-yellow-400">Возможности</a></li>
              <li><a href="#tech" class="hover:text-yellow-400">Технологии</a></li>
              <li><a href="#pricing" class="hover:text-yellow-400">Тарифы</a></li>
              <li><a href="#" class="hover:text-yellow-400">Документация</a></li>
            </ul>
          </div>

          <div>
            <h4 class="text-xl font-black mb-4">КОМПАНИЯ</h4>
            <ul class="space-y-2 font-bold">
              <li><a href="#" class="hover:text-yellow-400">О нас</a></li>
              <li><a href="#contact" class="hover:text-yellow-400">Контакты</a></li>
              <li><a href="#" class="hover:text-yellow-400">Политика</a></li>
              <li><a href="#" class="hover:text-yellow-400">Условия</a></li>
            </ul>
          </div>

          <div>
            <h4 class="text-xl font-black mb-4">СООБЩЕСТВО</h4>
            <ul class="space-y-2 font-bold">
              <li><a href="#" class="hover:text-yellow-400">GitHub</a></li>
              <li><a href="#" class="hover:text-yellow-400">Telegram</a></li>
              <li><a href="#" class="hover:text-yellow-400">Discord</a></li>
              <li><a href="#" class="hover:text-yellow-400">Changelog</a></li>
            </ul>
          </div>
        </div>

        <div class="border-t-2 border-white pt-8 text-center font-bold">
          <p>© {{ new Date().getFullYear() }} MYAPP. ВСЕ ПРАВА ЗАЩИЩЕНЫ.</p>
          <p>СОЗДАНО НА NUXT 3 + FASTAPI</p>
        </div>
      </div>
    </footer>
  </div>
</template>
