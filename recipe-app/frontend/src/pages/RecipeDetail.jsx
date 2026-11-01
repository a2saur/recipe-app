import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { getRecipe } from "../api/recipes";
import { formatTime } from "../utils/formatTime";
import { RecipeStepDetails } from "../components/RecipeStepDetails";
import { useGinghamBackground } from "../utils/useGinghamBackground";

const MAX_SWING_DEG = 10; // side-to-side rotation around the pin
const MAX_TILT_X_DEG = 10; // bottom edge pushed back into the board
const MAX_TILT_Y_DEG = 15; // sides pushed back into the board

// Swing the card like it's pinned at the top middle, writing CSS variables directly so mouse moves don't re-render
function handleTiltMove(e) {
  const card = e.currentTarget;
  const rect = card.getBoundingClientRect();
  // x: -1 (left edge) to 1 (right edge); y: 0 (pin) to 1 (bottom edge)
  const x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
  const y = (e.clientY - rect.top) / rect.height;
  // Pushing further from the pin gives more leverage, so the swing grows toward the bottom
  // The side under the cursor is pressed back and the card swings away from it
  card.style.setProperty("--swing", `${-x * y * MAX_SWING_DEG}deg`);
  card.style.setProperty("--tilt-x", `${y * MAX_TILT_X_DEG}deg`);
  card.style.setProperty("--tilt-y", `${x * y * MAX_TILT_Y_DEG}deg`);
}

function handleTiltLeave(e) {
  const card = e.currentTarget;
  card.style.setProperty("--swing", "0deg");
  card.style.setProperty("--tilt-x", "0deg");
  card.style.setProperty("--tilt-y", "0deg");
}

export default function RecipeDetail() {
  const { id } = useParams();
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useGinghamBackground();

  useEffect(() => {
    setLoading(true);
    getRecipe(id)
      .then(setRecipe)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <p>Loading recipe...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <main>
      <div className="recipe-page">
        <div className="recipe-info">
          <div className="recipe-header">
            <h1>{recipe.title}</h1>
            <p>{recipe.description}</p>
          </div>

          
          <div className="recipe-details">
            <div className="recipe-details-header">
              <button className="to-make-btn"><i className="bi bi-pin-angle-fill"></i></button>
            </div>
            <div className="recipe-details-card">
              {/* Tape sits outside the tilting body so it stays still */}
              <div className="recipe-details-tape"></div>
              <div
                className="recipe-details-body"
                onMouseMove={handleTiltMove}
                onMouseLeave={handleTiltLeave}
              >
                <p>Serves {recipe.serving_size}</p>
                <p>Active time: {recipe.active_time != null ? formatTime(recipe.active_time) : "Not specified"}</p>
                <p>Overall time: {recipe.overall_time != null ? formatTime(recipe.overall_time) : "Not specified"}</p>
                <p>Last modified: {recipe.timestamp} </p>
              </div>
            </div>
          </div>
        </div>

        <div className="recipe-content">
          <div className="recipe-ingredients">
            <ul>
              {recipe.ingredient_uses.map((ingredient, index) => (
                <li>{ingredient.amount} {ingredient.unit} {ingredient.name}</li>
              ))}
            </ul>
          </div>
          
          <div className="recipe-directions">
            <ul>
              {/* {recipe.steps.map((step, index) => (
                <li>{step.step_number}. {step.instruction}</li>
              ))} */}
              {recipe.steps.map((step) => (
                <li className="recipe-step" key={step.step_number}>
                  <RecipeStepDetails step={step} ingredients={recipe.ingredient_uses} />
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </main>
  );
}