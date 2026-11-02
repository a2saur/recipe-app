import { Routes, Route, NavLink, useNavigate } from "react-router";

import RecipeDetail from "./pages/RecipeDetail.jsx";
import RecipeForm from "./pages/RecipeForm.jsx";
import Home from "./pages/Home.jsx";
import GroceryList from "./pages/GroceryList.jsx";
import GroceryCosts from "./pages/GroceryCosts.jsx";

function NewRecipePage() {
  const navigate = useNavigate();

  async function saveRecipe(recipe) {
    const response = await fetch(
      "/api/recipes/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(recipe),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to save recipe");
    }

    navigate("/");
  }

  return <RecipeForm onSave={saveRecipe} />;
}
export default function App() {
  return (
    <>
      <nav>
        <NavLink to="/" end className={({ isActive }) => isActive ? 'nav-link active-page' : 'nav-link'}>
          Home
        </NavLink>
        <NavLink to="/recipes/new" className={({ isActive }) => isActive ? 'nav-link active-page' : 'nav-link'}>
          Add Recipe
        </NavLink>
        <NavLink to="/groceries/view" className={({ isActive }) => isActive ? 'nav-link active-page' : 'nav-link'}>
          Grocery List
        </NavLink>
        <NavLink to="/groceries/cost" className={({ isActive }) => isActive ? 'nav-link active-page' : 'nav-link'}>
          Grocery Costs
        </NavLink>
        {/* <Link to="/">Home</Link>
        <Link to="/recipes/new">Add Recipe</Link> */}
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/recipes/new" element={<NewRecipePage />} />
        <Route path="/recipes/:id/view" element={<RecipeDetail />} />
        <Route path="/groceries/view" element={<GroceryList />} />
        <Route path="/groceries/cost" element={<GroceryCosts />} />
      </Routes>
    </>
  );
}