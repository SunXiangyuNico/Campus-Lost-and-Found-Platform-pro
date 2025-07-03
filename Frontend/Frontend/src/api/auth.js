import axios from 'axios'

const API_BASE = '/api/auth'

export function register(data) {
  // 支持表单数据（用于头像上传）
  const formData = new FormData()
  Object.keys(data).forEach(key => {
    if (data[key] !== null && data[key] !== undefined) {
      formData.append(key, data[key])
    }
  })
  return axios.post(`${API_BASE}/register`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export function login(data) {
  return axios.post(`${API_BASE}/login`, data)
}

export function getUserInfo(token) {
  return axios.get(`${API_BASE}/me`, {
    headers: { Authorization: `Bearer ${token}` }
  })
}

export function updateProfile(data, token) {
  return axios.put(`${API_BASE}/me`, data, {
    headers: { Authorization: `Bearer ${token}` }
  })
}

export function changePassword(data, token) {
  return axios.post(`${API_BASE}/change-password`, data, {
    headers: { Authorization: `Bearer ${token}` }
  })
}

export function updateAvatar(file, token) {
  const formData = new FormData()
  formData.append('avatar', file)
  return axios.post(`${API_BASE}/update-avatar`, formData, {
    headers: { 
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  })
}

export function deleteAccount(password, token) {
  return axios.delete(`${API_BASE}/account`, {
    data: { password },
    headers: { Authorization: `Bearer ${token}` }
  })
}

export function getMyPosts() {
  return axios.get(`${API_BASE}/my-posts`)
} 