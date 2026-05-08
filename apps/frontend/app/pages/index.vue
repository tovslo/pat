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

const cursorX = ref(-9999)
const cursorY = ref(-9999)

function onMouseMove(e: MouseEvent) {
  cursorX.value = e.clientX
  cursorY.value = e.clientY
}

onMounted(() => window.addEventListener('mousemove', onMouseMove))
onUnmounted(() => window.removeEventListener('mousemove', onMouseMove))
</script>

<template>
  <div class="landing">
    <!-- ── Cursor glow ── -->
    <div
      class="cursor-glow"
      aria-hidden="true"
      :style="{ transform: `translate(${cursorX}px, ${cursorY}px)` }"
    />

    <!-- ── Animated background ── -->
    <div
      class="bg-stage"
      aria-hidden="true"
    >
      <div class="orb orb-1" />
      <div class="orb orb-2" />
      <div class="orb orb-3" />
      <div class="orb orb-4" />
      <div class="grid-overlay" />
    </div>

    <!-- ══════════════ HEADER ══════════════ -->
    <header class="site-header">
      <div class="wrap flex items-center justify-between h-16">
        <!-- Logo -->
        <NuxtLink
          to="/"
          class="logo-mark"
        >
          <img class="logo-icon" src="/logo-icon.svg" alt="" aria-hidden="true">
          <span class="logo-text">MyApp</span>
        </NuxtLink>

        <!-- Desktop nav -->
        <nav class="desktop-nav">
          <a
            v-for="link in navLinks"
            :key="link.href"
            :href="link.href"
            class="nav-item"
          >
            {{ link.label }}
          </a>
        </nav>

        <!-- Actions -->
        <div class="header-actions">
          <div
            v-if="auth.isLoggedIn"
            class="user-pill"
          >
            <img
              :src="auth.user?.avatarUrl || DEFAULT_AVATAR"
              class="user-avatar"
              alt="Аватарка"
            >
            <span class="user-email">{{ auth.user?.email }}</span>
          </div>
          <button
            v-if="auth.isLoggedIn"
            class="btn-danger"
            @click="handleLogout"
          >
            Выйти
          </button>
          <NuxtLink
            v-else
            to="/auth/login"
            class="btn-ghost"
          >Войти</NuxtLink>

          <!-- Burger (mobile) -->
          <button
            class="burger"
            :aria-expanded="mobileMenuOpen"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <span
              class="burger-line"
              :class="{ open: mobileMenuOpen }"
            />
            <span
              class="burger-line"
              :class="{ open: mobileMenuOpen }"
            />
            <span
              class="burger-line"
              :class="{ open: mobileMenuOpen }"
            />
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <Transition name="slide-down">
        <nav
          v-if="mobileMenuOpen"
          class="mobile-nav"
        >
          <a
            v-for="link in navLinks"
            :key="link.href"
            :href="link.href"
            class="mobile-nav-item"
            @click="mobileMenuOpen = false"
          >
            {{ link.label }}
          </a>
          <div class="flex gap-3 mt-4 items-center">
            <template v-if="auth.isLoggedIn">
              <div class="mobile-user-info flex-1">
                <img
                  :src="auth.user?.avatarUrl || DEFAULT_AVATAR"
                  class="user-avatar"
                  alt="Аватарка"
                >
                <span class="mobile-user-email">{{ auth.user?.email }}</span>
              </div>
              <button
                class="btn-danger"
                @click="handleLogout; mobileMenuOpen = false"
              >
                Выйти
              </button>
            </template>
            <template v-else>
              <NuxtLink
                to="/auth/login"
                class="btn-ghost flex-1 text-center"
              >Войти</NuxtLink>
            </template>
          </div>
        </nav>
      </Transition>
    </header>

    <!-- ══════════════ HERO ══════════════ -->
    <section class="hero">
      <div class="wrap-narrow text-center">
        <div
          class="badge animate-fade-up"
          style="animation-delay: 0.1s"
        >
          ✦ Открытый бета-доступ
        </div>

        <h1
          class="hero-title animate-fade-up"
          style="animation-delay: 0.2s"
        >
          Умная обработка<br>
          <span class="gradient-text">документов с ИИ</span>
        </h1>

        <p
          class="hero-desc animate-fade-up"
          style="animation-delay: 0.3s"
        >
          Загружайте, анализируйте и извлекайте данные из любых документов.<br>
          Self-hosted платформа на FastAPI + Nuxt 3, готовая к продакшну.
        </p>

        <div
          class="hero-cta animate-fade-up"
          style="animation-delay: 0.4s"
        >
          <NuxtLink
            to="/auth/register"
            class="btn-primary btn-lg"
          >
            Начать бесплатно
            <span class="ml-1.5">→</span>
          </NuxtLink>
          <button class="btn-outline btn-lg">
            Смотреть демо
          </button>
        </div>

        <!-- Mock UI card -->
        <div
          class="glass-card mock-card animate-fade-up"
          style="animation-delay: 0.5s"
        >
          <div class="mock-bar">
            <span
              class="mock-dot"
              style="background:#ef4444"
            />
            <span
              class="mock-dot"
              style="background:#f59e0b"
            />
            <span
              class="mock-dot"
              style="background:#22c55e"
            />
            <span class="mock-url">myapp.ru/dashboard</span>
          </div>
          <div class="mock-body">
            <div class="mock-sidebar">
              <div class="mock-item w-full h-3 rounded" />
              <div class="mock-item w-4/5 h-3 rounded" />
              <div class="mock-item w-3/5 h-3 rounded" />
              <div class="mock-item w-full h-3 rounded mt-4" />
              <div class="mock-item w-2/3 h-3 rounded" />
            </div>
            <div class="mock-main">
              <div class="flex gap-3 mb-4">
                <div class="glass-card flex-1 h-16 p-3">
                  <div class="mock-item w-1/2 h-2 rounded mb-2" />
                  <div class="mock-item w-1/3 h-4 rounded" />
                </div>
                <div class="glass-card flex-1 h-16 p-3">
                  <div class="mock-item w-1/2 h-2 rounded mb-2" />
                  <div class="mock-item w-2/5 h-4 rounded" />
                </div>
                <div class="glass-card flex-1 h-16 p-3">
                  <div class="mock-item w-1/2 h-2 rounded mb-2" />
                  <div class="mock-item w-1/4 h-4 rounded" />
                </div>
              </div>
              <div class="glass-card h-24 p-3">
                <div class="mock-item w-2/5 h-2 rounded mb-3" />
                <div class="flex gap-1 items-end h-12">
                  <div
                    v-for="h in [30, 55, 40, 70, 50, 80, 60]"
                    :key="h"
                    class="mock-bar-item flex-1 rounded-t"
                    :style="{ height: h + '%' }"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════ FEATURES ══════════════ -->
    <section
      id="features"
      class="section"
    >
      <div class="wrap">
        <div class="section-head">
          <div class="badge">
            Возможности
          </div>
          <h2 class="section-title">
            Всё для работы с документами
          </h2>
          <p class="section-desc">
            Платформа объединяет ИИ-анализ, семантический поиск<br>и автоматизацию в едином self-hosted решении
          </p>
        </div>

        <div class="features-grid">
          <div
            v-for="f in features"
            :key="f.title"
            class="glass-card feature-card"
          >
            <div class="feature-icon">
              {{ f.icon }}
            </div>
            <h3 class="feature-title">
              {{ f.title }}
            </h3>
            <p class="feature-desc">
              {{ f.desc }}
            </p>
            <div class="card-glow" />
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════ TECH STACK ══════════════ -->
    <section
      id="tech"
      class="section"
    >
      <div class="wrap">
        <div class="section-head">
          <div class="badge">
            Технологии
          </div>
          <h2 class="section-title">
            Проверенный стек
          </h2>
          <p class="section-desc">
            Production-ready технологии без избыточных зависимостей
          </p>
        </div>

        <div class="tech-grid">
          <div
            v-for="t in techStack"
            :key="t.label"
            class="glass-card tech-chip"
          >
            <span
              class="tech-dot"
              :style="{ background: t.color }"
            />
            {{ t.label }}
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════ CTA ══════════════ -->
    <section
      id="contact"
      class="section"
    >
      <div class="wrap-narrow">
        <div class="glass-card cta-card">
          <div class="cta-glow" />
          <div class="badge mx-auto w-fit">
            Начните сегодня
          </div>
          <h2 class="cta-title">
            Готовы к запуску?
          </h2>
          <p class="cta-desc">
            Разверните платформу на своём сервере за 5 минут.<br>
            Полный контроль над данными, без vendor lock-in.
          </p>
          <div class="hero-cta">
            <NuxtLink
              to="/auth/register"
              class="btn-primary btn-lg"
            >Получить доступ</NuxtLink>
            <button class="btn-outline btn-lg">
              Документация
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════ FOOTER ══════════════ -->
    <footer class="site-footer">
      <div class="wrap">
        <div class="footer-grid">
          <div class="footer-brand">
            <div class="logo-mark mb-3">
              <img class="logo-icon" src="/logo-icon.svg" alt="" aria-hidden="true">
              <span class="logo-text">MyApp</span>
            </div>
            <p class="footer-tagline">
              Современная ИИ-платформа<br>для работы с документами
            </p>
          </div>

          <div>
            <h4 class="footer-col-title">
              Продукт
            </h4>
            <ul class="footer-links">
              <li><a href="#features">Возможности</a></li>
              <li><a href="#tech">Технологии</a></li>
              <li><a href="#pricing">Тарифы</a></li>
              <li><a href="#">Документация</a></li>
            </ul>
          </div>

          <div>
            <h4 class="footer-col-title">
              Компания
            </h4>
            <ul class="footer-links">
              <li><a href="#">О нас</a></li>
              <li><a href="#contact">Контакты</a></li>
              <li><a href="#">Политика</a></li>
              <li><a href="#">Условия</a></li>
            </ul>
          </div>

          <div>
            <h4 class="footer-col-title">
              Сообщество
            </h4>
            <ul class="footer-links">
              <li><a href="#">GitHub</a></li>
              <li><a href="#">Telegram</a></li>
              <li><a href="#">Discord</a></li>
              <li><a href="#">Changelog</a></li>
            </ul>
          </div>
        </div>

        <div class="footer-bottom">
          <p>© {{ new Date().getFullYear() }} MyApp. Все права защищены.</p>
          <p>Создано на Nuxt 3 + FastAPI</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* ── Cursor glow ── */
.cursor-glow {
  display: none;
}

/* ── Root ── */
.landing {
  min-height: 100vh;
  background: #ffffff;
  color: #000;
  overflow-x: hidden;
  font-family: var(--font-sans, 'Public Sans', sans-serif);
}

/* ── Layout helpers ── */
.wrap        { max-width: 1200px; margin: 0 auto; padding: 0 1.5rem; }
.wrap-narrow { max-width: 860px;  margin: 0 auto; padding: 0 1.5rem; }

/* ── Animated background ── */
.bg-stage {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
  background: #ffffff;
}

.orb {
  display: none;
}
.orb-1 { display: none; }
.orb-2 { display: none; }
.orb-3 { display: none; }
.orb-4 { display: none; }

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(#000 2px, transparent 2px),
    linear-gradient(90deg, #000 2px, transparent 2px);
  background-size: 80px 80px;
  opacity: 0.08;
  mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
}

/* ── Glass card ── */
.glass-card {
  background: #ffffff;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  border: 3px solid #000;
  border-radius: 0;
  box-shadow: 6px 6px 0 rgba(0,0,0,0.15);
  transition: all 0.1s ease;
  position: relative;
  overflow: hidden;
}
.glass-card:hover {
  background: #f5f5f5;
  border-color: #000;
  transform: translate(2px, 2px);
  box-shadow: 4px 4px 0 rgba(0,0,0,0.15);
}

/* ── Header ── */
.site-header {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  background: #ffffff;
  border-bottom: 4px solid #000;
  padding: 0 1.5rem;
  transition: none;
}

.logo-mark {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  font-weight: 900;
  font-size: 1.3rem;
  letter-spacing: -0.02em;
  color: #000;
  transition: none;
}
.logo-mark:hover { opacity: 1; transform: scale(1.05); }
.logo-icon { width: 1.3rem; height: 1.3rem; vertical-align: middle; }

.desktop-nav {
  display: none;
  gap: 0.25rem;
}
@media (min-width: 768px) {
  .desktop-nav { display: flex; }
}

.nav-item {
  padding: 0.5rem 1rem;
  border-radius: 0;
  font-size: 0.875rem;
  color: #000;
  text-decoration: none;
  transition: none;
  position: relative;
  font-weight: 700;
  border: 2px solid transparent;
}
.nav-item::after {
  display: none;
}
.nav-item:hover { color: #000; background: #ffffcc; border-bottom: 3px solid #000; }

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

/* ── Buttons ── */
.btn-ghost {
  padding: 0.5rem 1rem;
  border-radius: 0;
  font-size: 0.875rem;
  font-weight: 700;
  color: #000;
  background: #ffffff;
  border: 3px solid #000;
  cursor: pointer;
  transition: none;
}
.btn-ghost:hover {
  color: #fff;
  background: #000;
  border-color: #000;
  transform: none;
}

.btn-primary {
  padding: 0.6rem 1.4rem;
  border-radius: 0;
  font-size: 0.875rem;
  font-weight: 800;
  color: #fff;
  background: #000;
  border: 3px solid #000;
  cursor: pointer;
  transition: none;
  box-shadow: 4px 4px 0 #ffffcc;
}
.btn-primary:hover {
  filter: none;
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 #ffffcc;
}
.btn-primary:active { transform: translate(0, 0); }

.btn-danger {
  padding: 0.5rem 1rem;
  border-radius: 0;
  font-size: 0.875rem;
  font-weight: 700;
  color: #fff;
  background: #ff0000;
  border: 3px solid #000;
  cursor: pointer;
  transition: none;
}
.btn-danger:hover {
  color: #fff;
  background: #cc0000;
  border-color: #000;
  transform: translate(2px, 2px);
}

.btn-outline {
  padding: 0.5rem 1.2rem;
  border-radius: 0;
  font-size: 0.875rem;
  font-weight: 700;
  color: #000;
  background: transparent;
  border: 3px solid #000;
  cursor: pointer;
  backdrop-filter: none;
  transition: none;
}
.btn-outline:hover {
  color: #fff;
  background: #000;
  border-color: #000;
  transform: none;
}

.btn-lg { padding: 0.8rem 2rem; font-size: 1rem; border-radius: 0; }

/* ── User pill (header) ── */
.user-pill {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem 0.25rem 0.25rem;
  border-radius: 0;
  background: #f5f5f5;
  border: 2px solid #000;
}
.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 0;
  object-fit: cover;
  flex-shrink: 0;
  border: 2px solid #000;
}
.user-email {
  font-size: 0.8rem;
  color: #000;
  max-width: 140px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 600;
}

/* ── Mobile user info ── */
.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.mobile-user-email {
  font-size: 0.85rem;
  color: #000;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-weight: 600;
}

/* ── Burger ── */
.burger {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 0.4rem;
  background: none;
  border: none;
  cursor: pointer;
}
@media (min-width: 768px) { .burger { display: none; } }

.burger-line {
  display: block;
  width: 22px;
  height: 3px;
  background: #000;
  border-radius: 0;
  transition: none;
}
.burger-line.open:nth-child(1) { transform: translateY(8px) rotate(45deg); }
.burger-line.open:nth-child(2) { opacity: 0; }
.burger-line.open:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }

.mobile-nav {
  padding: 1rem 0 1.25rem;
  border-top: 3px solid #000;
  background: #ffffff;
}
.mobile-nav-item {
  display: block;
  padding: 0.65rem 0;
  color: #000;
  text-decoration: none;
  font-size: 0.95rem;
  transition: none;
  font-weight: 700;
}
.mobile-nav-item:hover { color: #000; background: #ffffcc; }

/* ── Slide-down transition ── */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ── Hero ── */
.hero {
  position: relative;
  z-index: 10;
  padding: 10rem 0 5rem;
  text-align: center;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border-radius: 0;
  font-size: 0.8rem;
  font-weight: 800;
  color: #fff;
  background: #000;
  border: 3px solid #000;
  margin-bottom: 1.5rem;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.hero-title {
  font-size: clamp(2.4rem, 6vw, 4rem);
  font-weight: 900;
  line-height: 1.1;
  letter-spacing: -0.04em;
  margin-bottom: 1.4rem;
  color: #000;
}

.gradient-text {
  background: none;
  -webkit-background-clip: unset;
  -webkit-text-fill-color: unset;
  background-clip: unset;
  color: #000;
  border-bottom: 6px solid #ffffcc;
  display: inline-block;
  padding-bottom: 4px;
}

.hero-desc {
  font-size: 1.1rem;
  color: #333;
  line-height: 1.7;
  margin-bottom: 2.25rem;
  font-weight: 600;
}

.hero-cta {
  display: flex;
  gap: 0.85rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}

/* ── Mock UI card ── */
.mock-card {
  margin-top: 1rem;
  text-align: left;
  padding: 0;
  overflow: hidden;
  background: #f5f5f5;
}

.mock-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: #000;
  border-bottom: 3px solid #000;
}
.mock-dot {
  width: 10px; height: 10px;
  border-radius: 0;
  flex-shrink: 0;
}
.mock-url {
  flex: 1;
  font-size: 0.75rem;
  color: #999;
  text-align: center;
  font-family: monospace;
}

.mock-body {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  min-height: 160px;
}
.mock-sidebar {
  width: 140px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  padding-top: 0.25rem;
}
.mock-main { flex: 1; }

.mock-item {
  background: #ddd;
  border-radius: 0;
  animation: none;
  border: 2px solid #000;
}

.mock-bar-item {
  background: #000;
  border-radius: 0;
  min-height: 4px;
  animation: none;
  border: 1px solid #000;
}

/* ── Sections ── */
.section {
  position: relative;
  z-index: 10;
  padding: 6rem 0;
  border-top: 4px solid #000;
}

.section-head {
  text-align: center;
  margin-bottom: 3.5rem;
}
.section-title {
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  font-weight: 900;
  letter-spacing: -0.04em;
  margin: 0.75rem 0 0.9rem;
  color: #000;
}
.section-desc {
  color: #333;
  font-size: 1rem;
  line-height: 1.7;
  font-weight: 600;
}

/* ── Features grid ── */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
}

.feature-card {
  padding: 1.75rem;
  cursor: default;
  position: relative;
}
.feature-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  display: block;
}
.feature-title {
  font-size: 1.05rem;
  font-weight: 800;
  margin-bottom: 0.6rem;
  letter-spacing: -0.02em;
  color: #000;
}
.feature-desc {
  font-size: 0.875rem;
  color: #333;
  line-height: 1.65;
  font-weight: 500;
}
.card-glow {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: none;
  opacity: 1;
  transition: none;
  pointer-events: none;
  border: 3px solid #000;
}
.feature-card:hover .card-glow { 
  box-shadow: inset 0 0 0 3px #000;
}

/* ── Tech grid ── */
.tech-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  justify-content: center;
}

.tech-chip {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.7rem 1.3rem;
  border-radius: 0;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: default;
  border: 3px solid #000;
  background: #fff;
  color: #000;
}
.tech-chip:hover { transform: translate(2px, 2px); }
.tech-dot {
  width: 8px; height: 8px;
  border-radius: 0;
  flex-shrink: 0;
  box-shadow: none;
}

/* ── CTA ── */
.cta-card {
  padding: 3.5rem 2.5rem;
  text-align: center;
  border-color: #000;
  border: 4px solid #000;
  background: #ffffcc !important;
}
.cta-card:hover { transform: none; }
.cta-glow {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: none;
  pointer-events: none;
}
.cta-title {
  font-size: clamp(2rem, 4vw, 2.8rem);
  font-weight: 900;
  letter-spacing: -0.04em;
  margin: 0.75rem 0 0.9rem;
  color: #000;
}
.cta-desc {
  color: #333;
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 2rem;
  font-weight: 600;
}

/* ── Footer ── */
.site-footer {
  position: relative;
  z-index: 10;
  background: #000;
  backdrop-filter: none;
  border-top: 4px solid #000;
  padding: 3.5rem 0 2rem;
  color: #fff;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2.5rem;
}
@media (max-width: 768px) {
  .footer-grid { grid-template-columns: 1fr 1fr; }
  .footer-brand { grid-column: 1 / -1; }
}
@media (max-width: 480px) {
  .footer-grid { grid-template-columns: 1fr; }
}

.logo-text { color: #fff; }
.footer-tagline {
  font-size: 0.85rem;
  color: #ccc;
  line-height: 1.6;
  font-weight: 600;
}

.footer-col-title {
  font-size: 0.8rem;
  font-weight: 800;
  color: #fff;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  margin-bottom: 0.85rem;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}
.footer-links a {
  font-size: 0.875rem;
  color: #ccc;
  text-decoration: none;
  transition: none;
  font-weight: 600;
  border-bottom: 2px solid transparent;
}
.footer-links a:hover { 
  color: #ffffcc;
  border-bottom: 2px solid #ffffcc;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid #fff;
  font-size: 0.8rem;
  color: #ccc;
  font-weight: 600;
}

/* ── Animations ── */
.animate-fade-up {
  animation: fade-up 0.65s ease both;
}

@keyframes blob-drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25%       { transform: translate(24px, -32px) scale(1.05); }
  50%       { transform: translate(-18px, 18px) scale(0.96); }
  75%       { transform: translate(28px, 12px) scale(1.02); }
}
@keyframes blob-drift-alt {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33%       { transform: translate(-28px, 22px) scale(1.07); }
  66%       { transform: translate(16px, -18px) scale(0.93); }
}
@keyframes fade-up {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-glow {
  0%, 100% { opacity: 0.5; }
  50%       { opacity: 0.85; }
}
</style>
