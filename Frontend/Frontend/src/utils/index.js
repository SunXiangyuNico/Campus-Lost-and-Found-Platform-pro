/**
 * 公共工具函数
 */

/**
 * 处理头像URL
 * @param {string} avatar - 头像路径
 * @returns {string|undefined} 完整的头像URL
 */
export function getAvatarUrl(avatar) {
  if (!avatar) return undefined
  if (avatar.startsWith('/static/avatars/')) {
    return `http://localhost:5000${avatar}`
  }
  if (avatar.startsWith('http')) {
    return avatar
  }
  return `http://localhost:5000${avatar}`
}

/**
 * 格式化时间显示
 * @param {string} timeStr - ISO时间字符串
 * @returns {string} 格式化后的时间
 */
export function formatTime(timeStr) {
  if (!timeStr) return '未知时间'
  
  try {
    const date = new Date(timeStr)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffMinutes = Math.ceil(diffTime / (1000 * 60))
    const diffHours = Math.ceil(diffTime / (1000 * 60 * 60))
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffMinutes < 60) {
      return `${diffMinutes}分钟前`
    } else if (diffHours < 24) {
      return `${diffHours}小时前`
    } else if (diffDays === 1) {
      return '昨天'
    } else if (diffDays <= 7) {
      return `${diffDays}天前`
    } else {
      return date.toLocaleDateString('zh-CN', { 
        month: 'short', 
        day: 'numeric',
        year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
      })
    }
  } catch (e) {
    return '时间格式错误'
  }
}

/**
 * 获取用户显示名称
 * @param {Object} user - 用户对象
 * @returns {string} 用户显示名称
 */
export function getUserDisplayName(user) {
  return user?.name || user?.nickname || user?.username || '未知用户'
}

/**
 * 防抖函数
 * @param {Function} func - 要防抖的函数
 * @param {number} wait - 等待时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
export function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

/**
 * 节流函数
 * @param {Function} func - 要节流的函数
 * @param {number} limit - 时间限制（毫秒）
 * @returns {Function} 节流后的函数
 */
export function throttle(func, limit) {
  let inThrottle
  return function executedFunction(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
} 