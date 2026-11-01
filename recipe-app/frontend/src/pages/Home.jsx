
import { useEffect, useState } from "react";
import { getRecipes } from "../api/recipes";
import RecipeCarousel from "../components/RecipeCarousel";
import { useGinghamBackground } from "../utils/useGinghamBackground";

export default function Home() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useGinghamBackground();

  useEffect(() => {
    getRecipes()
      .then(setRecipes)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading recipes...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <main className="blank-bg">
      <h1>My Recipes</h1>

      {recipes.length === 0 ? (
        <p>You haven't added any recipes yet.</p>
      ) : (
        <RecipeCarousel recipes={recipes} />
      )}
    </main>
  );
}
