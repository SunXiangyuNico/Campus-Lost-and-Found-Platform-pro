import axios from 'axios'

const API_BASE = '/api/items'

// 只发送 JSON 数据，不再使用 FormData
export function createItem(data) {
  return axios.post(API_BASE, data)
}

export function getAllItems() {
  return axios.get(API_BASE)
}

export function addComment(itemId, content) {
  return axios.post(`${API_BASE}/${itemId}/comments`, { content })
}

export function searchItems(query, coordinates = null) {
  const params = { q: query }
  if (coordinates && coordinates.length >= 2) {
    params.x = coordinates[0]
    params.y = coordinates[1]
  }
  return axios.get(`${API_BASE}/search`, { params })
}

export function deleteItem(itemId) {
  console.log('API删除请求 - itemId:', itemId)
  console.log('API删除请求 - URL:', `${API_BASE}/${itemId}`)
  return axios.delete(`${API_BASE}/${itemId}`)
}

export function updateItem(itemId, data) {
  console.log('API更新请求 - itemId:', itemId)
  console.log('API更新请求 - URL:', `${API_BASE}/${itemId}`)
  console.log('API更新请求 - data:', data)
  return axios.put(`${API_BASE}/${itemId}`, data)
}

export function getMyClaims() {
  return axios.get(`/api/auth/my-claims`)
}