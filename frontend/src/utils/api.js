const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

export async function divinate(data) {
  const res = await fetch(`${BASE_URL}/api/divinate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  return await res.json()
}

export default {
  divinate
}
