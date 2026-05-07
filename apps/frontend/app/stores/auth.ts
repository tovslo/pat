import { defineStore } from 'pinia'

export interface AuthUser {
  id: string
  email: string
  isVerified: boolean
}

interface AuthState {
  user: AuthUser | null
  pending: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    pending: false
  }),

  getters: {
    isLoggedIn: state => state.user !== null,
    isVerified: state => state.user?.isVerified ?? false
  },

  actions: {
    async register(email: string, password: string) {
      this.pending = true
      try {
        await $fetch('/api/v1/auth/register', {
          method: 'POST',
          body: { email, password }
        })
      } finally {
        this.pending = false
      }
    },

    async login(email: string, password: string) {
      this.pending = true
      try {
        const data = await $fetch<AuthUser>('/api/v1/auth/login', {
          method: 'POST',
          body: { email, password },
          credentials: 'include'
        })
        this.user = data
      } finally {
        this.pending = false
      }
    },

    async logout() {
      await $fetch('/api/v1/auth/logout', { method: 'POST', credentials: 'include' })
      this.user = null
    },

    async fetchMe() {
      try {
        const data = await $fetch<AuthUser>('/api/v1/auth/me', { credentials: 'include' })
        this.user = data
      } catch {
        this.user = null
      }
    }
  }
})
