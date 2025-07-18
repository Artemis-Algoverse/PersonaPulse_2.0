// Event matching API service
const API_BASE_URL = 'http://localhost:5000/api';

export async function matchEvents(keywords) {
  const response = await fetch(`${API_BASE_URL}/events/match`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ keywords }),
  });
  if (!response.ok) {
    throw new Error('Failed to fetch matched events');
  }
  return response.json();
}
