const API_BASE_URL = "/api";

export async function getRecipes() {
  const response = await fetch(`${API_BASE_URL}/recipes/`);

  if (!response.ok) {
    throw new Error("Failed to fetch recipes");
  }

  return response.json();
}

export async function getRecipe(id) {
  const response = await fetch(`${API_BASE_URL}/recipes/${id}/view`);

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error || "Failed to fetch recipe");
  }

  return response.json();
}
