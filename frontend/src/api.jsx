const API_BASE = import.meta.env.VITE_API_URL;

export async function createPaste(data) {
  const res = await fetch(`${API_BASE}/api/pastes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  return res.json();
}

export async function fetchPaste(id) {
  const res = await fetch(`${API_BASE}/api/pastes/${id}`);
  if (!res.ok) throw new Error("Paste unavailable");
  return res.json();
}
