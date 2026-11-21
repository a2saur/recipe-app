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

export async function setRecipeToMake(id, toMake) {
  const response = await fetch(`${API_BASE_URL}/recipes/${id}/to-make`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ to_make: toMake }),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error || "Failed to update to-make list");
  }

  return response.json();
}

export async function getRecipesToMake() {
  const response = await fetch(`${API_BASE_URL}/recipes/to-make`);

  if (!response.ok) {
    throw new Error("Failed to fetch recipes");
  }

  return response.json();
}

export async function setRecipeDay(id, day) {
  const response = await fetch(`${API_BASE_URL}/recipes/${id}/day`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ day_to_make: day }),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error || "Failed to update recipe day");
  }

  return response.json();
}
