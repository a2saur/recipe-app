import { useEffect, useState } from "react";
import { getRecipesToMake, setRecipeDay } from "../api/recipes";

export default function Planner() {
    const [recipes, setRecipes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    // Day index currently being dragged over, or "unplanned" for the pool
    const [dragOver, setDragOver] = useState(null);
    const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    const [plannerOpen, setPlannerOpen] = useState(false);

    useEffect(() => {
        getRecipesToMake()
            .then(setRecipes)
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    function handleDragStart(e, recipe) {
        e.dataTransfer.setData("text/plain", recipe.id);
        e.dataTransfer.effectAllowed = "move";
    }

    function handleDragOver(e, target) {
        e.preventDefault(); // required to allow dropping
        e.dataTransfer.dropEffect = "move";
        setDragOver(target);
    }

    function handleDrop(e, day) {
        e.preventDefault();
        setDragOver(null);
        const id = e.dataTransfer.getData("text/plain");
        const recipe = recipes.find((r) => String(r.id) === id);
        if (!recipe || recipe.day_to_make === day) return;

        const previousDay = recipe.day_to_make;
        const updateDay = (d) =>
            setRecipes((prev) =>
                prev.map((r) => (String(r.id) === id ? { ...r, day_to_make: d } : r))
            );

        // Update optimistically, roll back if the save fails
        updateDay(day);
        setRecipeDay(recipe.id, day).catch((err) => {
            updateDay(previousDay);
            setError(err.message);
        });
    }

    function renderRecipe(recipe) {
        return (
            <div
                key={recipe.id}
                className="planned-recipe"
                draggable
                onDragStart={(e) => handleDragStart(e, recipe)}
            >
                {recipe.title}
            </div>
        );
    }

    function handleTogglePlanner(){
        setPlannerOpen(!plannerOpen);
    }

    if (loading) return <p>Loading planner...</p>;

    return (
        <>
        {error && <p className="error">{error}</p>}
        <div className="planner-title">
            <h1 style={{textAlign:'left'}}>Planner</h1>
            <button
            className={`to-make-btn${plannerOpen ? "" : " active"}`}
            onClick={handleTogglePlanner}
            // disabled={savingToMake}
            aria-pressed={plannerOpen}
            title={plannerOpen ? "Hide planner" : "Show planner"}
            >
                <i className={`bi ${plannerOpen ? "bi-caret-up" : "bi-caret-down-fill"}`}></i>
            </button>
        </div>
        <table className={`planner${plannerOpen ? "" : " hidden"}`}>
            <thead>
                <tr>
                    {days.map((day) => (
                        <th key={day} className="planner-day">
                            {day}
                        </th>
                    ))}
                </tr>
            </thead>
            <tbody>
                <tr>
                    {days.map((day, i) => (
                        <td
                            key={day}
                            className={`planner-cell${dragOver === i ? " drag-over" : ""}`}
                            onDragOver={(e) => handleDragOver(e, i)}
                            onDragLeave={() => setDragOver(null)}
                            onDrop={(e) => handleDrop(e, i)}
                        >
                            {recipes
                                .filter((recipe) => recipe.day_to_make === i)
                                .map(renderRecipe)}
                        </td>
                    ))}
                </tr>
            </tbody>
        </table>
        <div
            className={`planner-unplanned${dragOver === "unplanned" ? " drag-over" : ""}`}
            onDragOver={(e) => handleDragOver(e, "unplanned")}
            onDragLeave={() => setDragOver(null)}
            onDrop={(e) => handleDrop(e, null)}
        >
            {recipes
                .filter((recipe) => recipe.day_to_make == null)
                .map(renderRecipe)}
        </div>
        </>
    );
}
