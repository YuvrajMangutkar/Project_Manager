import React from 'react';

// CSRF wrapper for Django
export function getCsrfToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, 10) === 'csrftoken=') {
            cookieValue = decodeURIComponent(cookie.substring(10));
            break;
        }
    }
  }
  return cookieValue;
}

export default function apiFetch(url, options = {}) {
    options.headers = options.headers || {};
    options.headers['X-CSRFToken'] = getCsrfToken();
    options.headers['Accept'] = 'application/json';
    if (!options.headers['Content-Type'] && !(options.body instanceof FormData)) {
        options.headers['Content-Type'] = 'application/json';
    }
    options.credentials = 'same-origin'; // Send cookies naturally

    return fetch(url, options).then(async (res) => {
        if(res.status === 403 || res.redirected && res.url.includes('/login')) {
            window.location.href = '/login/';
            throw new Error('Unauthorized');
        }
        
        let data = null;
        try {
            data = await res.json();
        } catch { /* not json */ }

        if (!res.ok) {
            throw new Error(data?.error || data?.detail || 'Network error');
        }
        return data;
    });
}
