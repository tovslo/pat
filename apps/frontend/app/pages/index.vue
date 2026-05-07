<script setup lang="ts">
definePageMeta({ layout: false })

useSeoMeta({
  title: 'MyApp — ИИ-платформа для документов',
  description: 'Self-hosted платформа для анализа, поиска и автоматизации работы с документами на базе FastAPI и Nuxt 3.',
})

const navLinks = [
  { label: 'Возможности', href: '#features' },
  { label: 'Технологии', href: '#tech' },
  { label: 'Тарифы', href: '#pricing' },
  { label: 'Контакты', href: '#contact' },
]

const features = [
  {
    icon: '🧠',
    title: 'ИИ-анализ документов',
    desc: 'Автоматическое извлечение данных, суммаризация и классификация любых документов с помощью языковых моделей.',
  },
  {
    icon: '⚡',
    title: 'Семантический поиск',
    desc: 'Мгновенный поиск по всему архиву документов. Находит смысл, а не только ключевые слова.',
  },
  {
    icon: '🔒',
    title: 'Полная безопасность',
    desc: 'Self-hosted решение — данные остаются на вашем сервере. Шифрование на каждом уровне.',
  },
  {
    icon: '🔄',
    title: 'Автоматизация задач',
    desc: 'Гибкие пайплайны обработки с Celery + RabbitMQ. Уведомления в реальном времени через WebSocket.',
  },
  {
    icon: '📊',
    title: 'Аналитика и отчёты',
    desc: 'Дашборды с метриками, трендами и экспортом. Grafana + Prometheus из коробки.',
  },
  {
    icon: '🌐',
    title: 'API-first подход',
    desc: 'RESTful API с OpenAPI-документацией. Type-safe клиент из схемы для быстрой интеграции.',
  },
]

const techStack = [
  { label: 'Nuxt 3', color: '#00DC82' },
  { label: 'FastAPI', color: '#059669' },
  { label: 'PostgreSQL', color: '#3b82f6' },
  { label: 'Celery', color: '#8b5cf6' },
  { label: 'RabbitMQ', color: '#f59e0b' },
  { label: 'Docker Swarm', color: '#0ea5e9' },
  { label: 'Traefik', color: '#ec4899' },
  { label: 'Prometheus', color: '#ef4444' },
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
    <div class="bg-stage" aria-hidden="true">
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
        <NuxtLink to="/" class="logo-mark">
          <span class="logo-icon">◈</span>
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
          <button class="btn-ghost">Войти</button>
          <button class="btn-primary">Начать бесплатно</button>

          <!-- Burger (mobile) -->
          <button
            class="burger"
            :aria-expanded="mobileMenuOpen"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <span class="burger-line" :class="{ open: mobileMenuOpen }" />
            <span class="burger-line" :class="{ open: mobileMenuOpen }" />
            <span class="burger-line" :class="{ open: mobileMenuOpen }" />
          </button>
        </div>
      </div>

      <!-- Mobile menu -->
      <Transition name="slide-down">
        <nav v-if="mobileMenuOpen" class="mobile-nav">
          <a
            v-for="link in navLinks"
            :key="link.href"
            :href="link.href"
            class="mobile-nav-item"
            @click="mobileMenuOpen = false"
          >
            {{ link.label }}
          </a>
          <div class="flex gap-3 mt-4">
            <button class="btn-ghost flex-1">Войти</button>
            <button class="btn-primary flex-1">Начать</button>
          </div>
        </nav>
      </Transition>
    </header>

    <!-- ══════════════ HERO ══════════════ -->
    <section class="hero">
      <div class="wrap-narrow text-center">
        <div class="badge animate-fade-up" style="animation-delay: 0.1s">
          ✦ Открытый бета-доступ
        </div>

        <h1 class="hero-title animate-fade-up" style="animation-delay: 0.2s">
          Умная обработка<br>
          <span class="gradient-text">документов с ИИ</span>
        </h1>

        <p class="hero-desc animate-fade-up" style="animation-delay: 0.3s">
          Загружайте, анализируйте и извлекайте данные из любых документов.<br>
          Self-hosted платформа на FastAPI + Nuxt 3, готовая к продакшну.
        </p>

        <div class="hero-cta animate-fade-up" style="animation-delay: 0.4s">
          <button class="btn-primary btn-lg">
            Начать бесплатно
            <span class="ml-1.5">→</span>
          </button>
          <button class="btn-outline btn-lg">Смотреть демо</button>
        </div>

        <!-- Mock UI card -->
        <div class="glass-card mock-card animate-fade-up" style="animation-delay: 0.5s">
          <div class="mock-bar">
            <span class="mock-dot" style="background:#ef4444" />
            <span class="mock-dot" style="background:#f59e0b" />
            <span class="mock-dot" style="background:#22c55e" />
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
                  <div v-for="h in [30,55,40,70,50,80,60]" :key="h" class="mock-bar-item flex-1 rounded-t" :style="{ height: h + '%' }" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════ FEATURES ══════════════ -->
    <section id="features" class="section">
      <div class="wrap">
        <div class="section-head">
          <div class="badge">Возможности</div>
          <h2 class="section-title">Всё для работы с документами</h2>
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
            <div class="feature-icon">{{ f.icon }}</div>
            <h3 class="feature-title">{{ f.title }}</h3>
            <p class="feature-desc">{{ f.desc }}</p>
            <div class="card-glow" />
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════ TECH STACK ══════════════ -->
    <section id="tech" class="section">
      <div class="wrap">
        <div class="section-head">
          <div class="badge">Технологии</div>
          <h2 class="section-title">Проверенный стек</h2>
          <p class="section-desc">Production-ready технологии без избыточных зависимостей</p>
        </div>

        <div class="tech-grid">
          <div
            v-for="t in techStack"
            :key="t.label"
            class="glass-card tech-chip"
          >
            <span class="tech-dot" :style="{ background: t.color }" />
            {{ t.label }}
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════ CTA ══════════════ -->
    <section id="contact" class="section">
      <div class="wrap-narrow">
        <div class="glass-card cta-card">
          <div class="cta-glow" />
          <div class="badge mx-auto w-fit">Начните сегодня</div>
          <h2 class="cta-title">Готовы к запуску?</h2>
          <p class="cta-desc">
            Разверните платформу на своём сервере за 5 минут.<br>
            Полный контроль над данными, без vendor lock-in.
          </p>
          <div class="hero-cta">
            <button class="btn-primary btn-lg">Получить доступ</button>
            <button class="btn-outline btn-lg">Документация</button>
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
              <span class="logo-icon">◈</span>
              <span class="logo-text">MyApp</span>
            </div>
            <p class="footer-tagline">
              Современная ИИ-платформа<br>для работы с документами
            </p>
          </div>

          <div>
            <h4 class="footer-col-title">Продукт</h4>
            <ul class="footer-links">
              <li><a href="#features">Возможности</a></li>
              <li><a href="#tech">Технологии</a></li>
              <li><a href="#pricing">Тарифы</a></li>
              <li><a href="#">Документация</a></li>
            </ul>
          </div>

          <div>
            <h4 class="footer-col-title">Компания</h4>
            <ul class="footer-links">
              <li><a href="#">О нас</a></li>
              <li><a href="#contact">Контакты</a></li>
              <li><a href="#">Политика</a></li>
              <li><a href="#">Условия</a></li>
            </ul>
          </div>

          <div>
            <h4 class="footer-col-title">Сообщество</h4>
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
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;
  pointer-events: none;
  width: 600px;
  height: 600px;
  margin-left: -300px;
  margin-top: -300px;
  background: radial-gradient(
    circle at center,
    rgba(139, 92, 246, 0.12) 0%,
    rgba(99, 102, 241, 0.06) 35%,
    transparent 70%
  );
  border-radius: 50%;
  transition: transform 0.12s ease-out;
  will-change: transform;
}

/* ── Root ── */
.landing {
  min-height: 100vh;
  background: #07071a;
  color: #fff;
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
}

.orb {
  position: absolute;
  border-radius: 50%;
  animation: blob-drift 22s infinite ease-in-out;
}
.orb-1 {
  width: 700px; height: 700px;
  background: radial-gradient(circle at 40% 40%, #6d28d9 0%, transparent 65%);
  top: -280px; left: -180px;
  opacity: 0.55;
  animation-duration: 24s;
}
.orb-2 {
  width: 560px; height: 560px;
  background: radial-gradient(circle at 60% 40%, #1d4ed8 0%, transparent 65%);
  top: 25%; right: -150px;
  opacity: 0.45;
  animation-name: blob-drift-alt;
  animation-duration: 28s;
}
.orb-3 {
  width: 440px; height: 440px;
  background: radial-gradient(circle at 50% 60%, #059669 0%, transparent 65%);
  bottom: 5%; left: 15%;
  opacity: 0.38;
  animation-duration: 32s;
  animation-delay: -10s;
}
.orb-4 {
  width: 380px; height: 380px;
  background: radial-gradient(circle at 50% 50%, #be185d 0%, transparent 65%);
  top: 55%; right: 25%;
  opacity: 0.35;
  animation-name: blob-drift-alt;
  animation-duration: 26s;
  animation-delay: -6s;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
}

/* ── Glass card ── */
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 1.25rem;
  box-shadow: 0 8px 32px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.08);
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease, border-color 0.3s ease;
  position: relative;
  overflow: hidden;
}
.glass-card:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.16);
  transform: translateY(-5px);
  box-shadow: 0 20px 60px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.12);
}

/* ── Header ── */
.site-header {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  background: rgba(7, 7, 26, 0.72);
  border-bottom: 1px solid rgba(255,255,255,.07);
  padding: 0 1.5rem;
  transition: background 0.3s;
}

.logo-mark {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  font-weight: 700;
  font-size: 1.15rem;
  letter-spacing: -0.02em;
  color: #fff;
  transition: opacity 0.2s;
}
.logo-mark:hover { opacity: 0.8; }
.logo-icon { color: #8b5cf6; font-size: 1.3rem; }

.desktop-nav {
  display: none;
  gap: 0.25rem;
}
@media (min-width: 768px) {
  .desktop-nav { display: flex; }
}

.nav-item {
  padding: 0.45rem 0.9rem;
  border-radius: 0.6rem;
  font-size: 0.875rem;
  color: rgba(255,255,255,.65);
  text-decoration: none;
  transition: color 0.2s, background 0.2s;
  position: relative;
}
.nav-item::after {
  content: '';
  position: absolute;
  bottom: 4px; left: 50%; right: 50%;
  height: 2px;
  background: #8b5cf6;
  border-radius: 1px;
  transition: left 0.25s ease, right 0.25s ease;
}
.nav-item:hover { color: #fff; background: rgba(255,255,255,.06); }
.nav-item:hover::after { left: 0.9rem; right: 0.9rem; }

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

/* ── Buttons ── */
.btn-ghost {
  padding: 0.45rem 1rem;
  border-radius: 0.65rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(255,255,255,.7);
  background: transparent;
  border: 1px solid rgba(255,255,255,.12);
  cursor: pointer;
  transition: color 0.2s, background 0.2s, border-color 0.2s, transform 0.15s;
}
.btn-ghost:hover {
  color: #fff;
  background: rgba(255,255,255,.07);
  border-color: rgba(255,255,255,.22);
  transform: translateY(-1px);
}

.btn-primary {
  padding: 0.45rem 1.1rem;
  border-radius: 0.65rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
  border: 1px solid rgba(139,92,246,.4);
  cursor: pointer;
  transition: filter 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 4px 20px rgba(124,58,237,.35);
}
.btn-primary:hover {
  filter: brightness(1.12);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(124,58,237,.5);
}
.btn-primary:active { transform: translateY(0); }

.btn-outline {
  padding: 0.45rem 1.1rem;
  border-radius: 0.65rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: rgba(255,255,255,.8);
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.15);
  cursor: pointer;
  backdrop-filter: blur(8px);
  transition: color 0.2s, background 0.2s, border-color 0.2s, transform 0.15s;
}
.btn-outline:hover {
  color: #fff;
  background: rgba(255,255,255,.09);
  border-color: rgba(255,255,255,.28);
  transform: translateY(-2px);
}

.btn-lg { padding: 0.75rem 1.75rem; font-size: 1rem; border-radius: 0.85rem; }

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
  height: 2px;
  background: rgba(255,255,255,.7);
  border-radius: 1px;
  transition: transform 0.25s, opacity 0.25s;
}
.burger-line.open:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.burger-line.open:nth-child(2) { opacity: 0; }
.burger-line.open:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

.mobile-nav {
  padding: 1rem 0 1.25rem;
  border-top: 1px solid rgba(255,255,255,.07);
}
.mobile-nav-item {
  display: block;
  padding: 0.65rem 0;
  color: rgba(255,255,255,.7);
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s;
}
.mobile-nav-item:hover { color: #fff; }

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
  padding: 0.35rem 0.9rem;
  border-radius: 2rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: #a78bfa;
  background: rgba(139,92,246,.12);
  border: 1px solid rgba(139,92,246,.25);
  margin-bottom: 1.5rem;
  letter-spacing: 0.01em;
}

.hero-title {
  font-size: clamp(2.4rem, 6vw, 4rem);
  font-weight: 800;
  line-height: 1.12;
  letter-spacing: -0.03em;
  margin-bottom: 1.4rem;
}

.gradient-text {
  background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 50%, #10b981 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 1.1rem;
  color: rgba(255,255,255,.55);
  line-height: 1.7;
  margin-bottom: 2.25rem;
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
}

.mock-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: rgba(255,255,255,.04);
  border-bottom: 1px solid rgba(255,255,255,.07);
}
.mock-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.mock-url {
  flex: 1;
  font-size: 0.75rem;
  color: rgba(255,255,255,.3);
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
  background: rgba(255,255,255,.09);
  border-radius: 4px;
  animation: pulse-glow 2.5s infinite;
}

.mock-bar-item {
  background: linear-gradient(180deg, #8b5cf6 0%, rgba(139,92,246,.3) 100%);
  border-radius: 3px 3px 0 0;
  min-height: 4px;
  animation: pulse-glow 2s infinite;
}

/* ── Sections ── */
.section {
  position: relative;
  z-index: 10;
  padding: 6rem 0;
}

.section-head {
  text-align: center;
  margin-bottom: 3.5rem;
}
.section-title {
  font-size: clamp(1.8rem, 4vw, 2.6rem);
  font-weight: 750;
  letter-spacing: -0.025em;
  margin: 0.75rem 0 0.9rem;
}
.section-desc {
  color: rgba(255,255,255,.5);
  font-size: 1rem;
  line-height: 1.7;
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
}
.feature-icon {
  font-size: 2rem;
  margin-bottom: 1rem;
  display: block;
}
.feature-title {
  font-size: 1.05rem;
  font-weight: 650;
  margin-bottom: 0.6rem;
  letter-spacing: -0.01em;
}
.feature-desc {
  font-size: 0.875rem;
  color: rgba(255,255,255,.5);
  line-height: 1.65;
}
.card-glow {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(circle at 50% 0%, rgba(139,92,246,.12) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
}
.feature-card:hover .card-glow { opacity: 1; }

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
  padding: 0.6rem 1.2rem;
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: default;
}
.tech-chip:hover { transform: translateY(-3px) scale(1.03); }
.tech-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 6px currentColor;
}

/* ── CTA ── */
.cta-card {
  padding: 3.5rem 2.5rem;
  text-align: center;
  border-color: rgba(139,92,246,.2);
}
.cta-card:hover { transform: none; }
.cta-glow {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background: radial-gradient(ellipse 60% 50% at 50% 0%, rgba(109,40,217,.2) 0%, transparent 70%);
  pointer-events: none;
}
.cta-title {
  font-size: clamp(2rem, 4vw, 2.8rem);
  font-weight: 780;
  letter-spacing: -0.03em;
  margin: 0.75rem 0 0.9rem;
}
.cta-desc {
  color: rgba(255,255,255,.5);
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 2rem;
}

/* ── Footer ── */
.site-footer {
  position: relative;
  z-index: 10;
  background: rgba(255,255,255,.025);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255,255,255,.07);
  padding: 3.5rem 0 2rem;
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
  color: rgba(255,255,255,.38);
  line-height: 1.6;
}

.footer-col-title {
  font-size: 0.8rem;
  font-weight: 600;
  color: rgba(255,255,255,.55);
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
  color: rgba(255,255,255,.45);
  text-decoration: none;
  transition: color 0.2s;
}
.footer-links a:hover { color: rgba(255,255,255,.85); }

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255,255,255,.07);
  font-size: 0.8rem;
  color: rgba(255,255,255,.3);
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
