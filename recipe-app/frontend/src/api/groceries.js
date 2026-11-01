const API_BASE_URL = "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}/groceries${path}`, {
    ...options,
    headers: { "Content-Type": "application/json" },
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error || "Grocery request failed");
  }

  return response.status === 204 ? null : response.json();
}

export function getGroceries() {
  return request("/");
}

export function addOwnedGrocery(grocery) {
  return request("/owned", {
    method: "POST",
    body: JSON.stringify(grocery),
  });
}

export function deleteOwnedGrocery(id) {
  return request(`/owned/${id}`, { method: "DELETE" });
}

export function addListItem(item) {
  return request("/list", {
    method: "POST",
    body: JSON.stringify(item),
  });
}

export function setListItemChecked(id, isChecked) {
  return request(`/list/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ is_checked: isChecked }),
  });
}

export function deleteListItem(id) {
  return request(`/list/${id}`, { method: "DELETE" });
}
