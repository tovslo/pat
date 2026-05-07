import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '~/stores/auth'

// Mock $fetch globally
const mockFetch = vi.fn()
vi.stubGlobal('$fetch', mockFetch)

describe('useAuthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    mockFetch.mockReset()
  })

  it('initial state: not logged in', () => {
    const auth = useAuthStore()
    expect(auth.isLoggedIn).toBe(false)
    expect(auth.user).toBeNull()
  })

  it('register: calls POST /api/v1/auth/register with FormData', async () => {
    mockFetch.mockResolvedValueOnce({})
    const auth = useAuthStore()
    await auth.register('user@example.com', 'password123')
    expect(mockFetch).toHaveBeenCalledOnce()
    const [url, opts] = mockFetch.mock.calls[0]
    expect(url).toBe('/api/v1/auth/register')
    expect(opts.method).toBe('POST')
    expect(opts.body).toBeInstanceOf(FormData)
    expect(opts.body.get('email')).toBe('user@example.com')
    expect(opts.body.get('password')).toBe('password123')
  })

  it('register: appends avatar to FormData when provided', async () => {
    mockFetch.mockResolvedValueOnce({})
    const auth = useAuthStore()
    const file = new File(['data'], 'avatar.png', { type: 'image/png' })
    await auth.register('user@example.com', 'password123', file)
    const [, opts] = mockFetch.mock.calls[0]
    expect(opts.body.get('avatar')).toBe(file)
  })

  it('login: sets user on success', async () => {
    const fakeUser = { id: '1', email: 'user@example.com', isVerified: true, avatarUrl: null }
    mockFetch.mockResolvedValueOnce(fakeUser)
    const auth = useAuthStore()
    await auth.login('user@example.com', 'password123')
    expect(auth.user).toEqual(fakeUser)
    expect(auth.isLoggedIn).toBe(true)
    expect(auth.isVerified).toBe(true)
  })

  it('login: does not set user on error', async () => {
    mockFetch.mockRejectedValueOnce({ status: 401, data: { detail: 'Invalid credentials' } })
    const auth = useAuthStore()
    await expect(auth.login('user@example.com', 'wrong')).rejects.toBeDefined()
    expect(auth.user).toBeNull()
    expect(auth.isLoggedIn).toBe(false)
  })

  it('logout: clears user', async () => {
    const auth = useAuthStore()
    auth.user = { id: '1', email: 'user@example.com', isVerified: true, avatarUrl: null }
    mockFetch.mockResolvedValueOnce({})
    await auth.logout()
    expect(auth.user).toBeNull()
    expect(auth.isLoggedIn).toBe(false)
  })

  it('fetchMe: sets user on success', async () => {
    const fakeUser = { id: '2', email: 'a@b.com', isVerified: false, avatarUrl: null }
    mockFetch.mockResolvedValueOnce(fakeUser)
    const auth = useAuthStore()
    await auth.fetchMe()
    expect(auth.user).toEqual(fakeUser)
  })

  it('fetchMe: silently clears user on 401', async () => {
    mockFetch.mockRejectedValueOnce({ status: 401 })
    const auth = useAuthStore()
    auth.user = { id: '1', email: 'x@y.com', isVerified: true, avatarUrl: null }
    await auth.fetchMe()
    expect(auth.user).toBeNull()
  })

  it('isVerified: false when user not verified', () => {
    const auth = useAuthStore()
    auth.user = { id: '1', email: 'x@y.com', isVerified: false, avatarUrl: null }
    expect(auth.isVerified).toBe(false)
  })

  it('pending: true during login request', async () => {
    let resolveFetch!: (v: unknown) => void
    mockFetch.mockReturnValueOnce(new Promise(r => (resolveFetch = r)))
    const auth = useAuthStore()
    const loginPromise = auth.login('user@example.com', 'pass')
    expect(auth.pending).toBe(true)
    resolveFetch({ id: '1', email: 'user@example.com', isVerified: true, avatarUrl: null })
    await loginPromise
    expect(auth.pending).toBe(false)
  })
})
