
import { useState } from "react";
import { useGinghamBackground } from "../utils/useGinghamBackground";
import { INGREDIENT_UNITS } from "../utils/ingredientUnits";

function createIngredient() {
  return {
    id: crypto.randomUUID(),
    name: "",
    amount: "1",
    unit: "",
  };
}

function createStep() {
  return {
    id: crypto.randomUUID(),
    text: "",
  };
}

function getTotalMinutes(hours, minutes) {
  if (hours === "" && minutes === "") return null;
  return Number(hours || 0) * 60 + Number(minutes || 0);
}

export default function RecipeForm({ onSave }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [servingSize, setServingSize] = useState(4);

  const [activeHours, setActiveHours] = useState("");
  const [activeMinutes, setActiveMinutes] = useState("");
  const [overallHours, setOverallHours] = useState("");
  const [overallMinutes, setOverallMinutes] = useState("");

  const [ingredients, setIngredients] = useState([
    createIngredient(),
  ]);
  const [steps, setSteps] = useState([createStep()]);

  const [error, setError] = useState("");

  useGinghamBackground();

  function updateIngredient(id, field, value) {
    setIngredients((current) =>
      current.map((ingredient) =>
        ingredient.id === id
          ? { ...ingredient, [field]: value }
          : ingredient
      )
    );
  }

  function addIngredient() {
    setIngredients((current) => [...current, createIngredient()]);
  }

  function removeIngredient(id) {
    setIngredients((current) =>
      current.filter((ingredient) => ingredient.id !== id)
    );
  }

  function updateStep(id, text) {
    setSteps((current) =>
      current.map((step) =>
        step.id === id ? { ...step, text } : step
      )
    );
  }

  function addStep() {
    setSteps((current) => [...current, createStep()]);
  }

  function removeStep(id) {
    setSteps((current) =>
      current.filter((step) => step.id !== id)
    );
  }

  function moveStep(index, direction) {
    const newIndex = index + direction;

    if (newIndex < 0 || newIndex >= steps.length) return;

    setSteps((current) => {
      const updated = [...current];
      [updated[index], updated[newIndex]] = [
        updated[newIndex],
        updated[index],
      ];
      return updated;
    });
  }

  function handleSubmit(event) {
    event.preventDefault();
    setError("");

    // Which submit button was clicked ("Save recipe" or "Save as draft").
    const isDraft = event.nativeEvent.submitter?.value === "draft";

    if (!title.trim()) {
      setError("Please enter a recipe title.");
      return;
    }

    if (servingSize < 1) {
      setError("Serving size must be at least 1.");
      return;
    }

    // Ignore completely empty ingredient rows.
    const filledIngredients = ingredients
      .filter((ingredient) => ingredient.name.trim())
      .map((ingredient) => ({
        ...ingredient,
        name: ingredient.name.trim(),
        amount: Number(ingredient.amount || 1),
        unit: ingredient.unit,
      }));

    // Ingredient names must be unique so references are unambiguous.
    const ingredientNames = filledIngredients.map((ingredient) =>
      ingredient.name.toLowerCase()
    );

    if (new Set(ingredientNames).size !== ingredientNames.length) {
      setError("Each ingredient must have a unique name.");
      return;
    }

    if (
      filledIngredients.some(
        (ingredient) =>
          !Number.isFinite(ingredient.amount) ||
          ingredient.amount <= 0
      )
    ) {
      setError("Ingredient amounts must be greater than zero.");
      return;
    }

    // Find every reference written as <ingredient name>.
    const parsedSteps = steps
      .filter((step) => step.text.trim())
      .map((step, index) => {
        const references = [
          ...step.text.matchAll(/<([^<>]+)>/g),
        ].map((match) => match[1].trim());

        return {
          step_number: index + 1,
          instruction: step.text.trim(),
          ingredient_refs: references,
        };
      });

    // Ensure every reference points to an ingredient in the form.
    const knownNames = new Set(ingredientNames);

    for (const step of parsedSteps) {
      for (const reference of step.ingredient_refs) {
        if (!knownNames.has(reference.split(", ")[0].toLowerCase())) {
          setError(
            `Step ${step.step_number} references "${reference}", ` +
            "but that ingredient hasn't been added. Check its name."
          );
          return;
        }
      }
    }

    const recipe = {
      title: title.trim(),
      description: description.trim(),
      serving_size: servingSize,
      active_time: getTotalMinutes(activeHours, activeMinutes),
      overall_time: getTotalMinutes(overallHours, overallMinutes),
      is_draft: isDraft,
      to_make: false,

      ingredients: filledIngredients.map(
        ({ name, amount, unit }) => ({
          name,
          amount,
          unit,
        })
      ),

      steps: parsedSteps,
    };

    if (onSave) {
      onSave(recipe);
    } else {
      setError(
        "The form is valid, but saving isn't connected yet. " +
        "Connect an onSave handler to submit this recipe."
      );
    }
  }

  return (
    <main>
      <form className="recipe-page recipe-form" onSubmit={handleSubmit}>
        <h1>Add Recipe</h1>

        <fieldset className="form-section">
          <legend>Recipe Details</legend>

          <label className="form-field">
            <span className="form-label">Title</span>
            <input
              type="text"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              required
            />
          </label>

          <label className="form-field">
            <span className="form-label">Description</span>
            <textarea
              value={description}
              onChange={(event) =>
                setDescription(event.target.value)
              }
              rows={3}
            />
          </label>

          <div className="form-row">
            {/* A div, not a label, so clicking the text doesn't press − */}
            <div className="form-field" role="group" aria-labelledby="serving-size-label">
              <span className="form-label" id="serving-size-label">
                Serving size
              </span>
              <div className="stepper">
                <button
                  type="button"
                  className="icon-btn"
                  onClick={() =>
                    setServingSize((size) => Math.max(1, size - 1))
                  }
                  disabled={servingSize <= 1}
                  aria-label="Decrease serving size"
                >
                  <i className="bi bi-dash-lg"></i>
                </button>

                <output>{servingSize}</output>

                <button
                  type="button"
                  className="icon-btn"
                  onClick={() =>
                    setServingSize((size) => size + 1)
                  }
                  aria-label="Increase serving size"
                >
                  <i className="bi bi-plus-lg"></i>
                </button>
              </div>
            </div>

            <TimeInputs
              label="Active time"
              hours={activeHours}
              minutes={activeMinutes}
              onHoursChange={setActiveHours}
              onMinutesChange={setActiveMinutes}
            />

            <TimeInputs
              label="Overall time"
              hours={overallHours}
              minutes={overallMinutes}
              onHoursChange={setOverallHours}
              onMinutesChange={setOverallMinutes}
            />
          </div>
        </fieldset>

        <fieldset className="form-section">
          <legend>Ingredients</legend>

          <p className="form-hint">
            Use a clear, unique name for each ingredient.
            Choose "individual items" for things counted whole,
            like eggs.
          </p>

          <div className="ingredient-row ingredient-header" aria-hidden="true">
            <span>Name</span>
            <span>Amount</span>
            <span>Unit</span>
          </div>

          {ingredients.map((ingredient, index) => (
            <div className="ingredient-row" key={ingredient.id}>
              <input
                type="text"
                value={ingredient.name}
                onChange={(event) =>
                  updateIngredient(
                    ingredient.id,
                    "name",
                    event.target.value
                  )
                }
                placeholder="e.g. Flour"
                aria-label={`Ingredient ${index + 1} name`}
              />

              <input
                type="number"
                min="0.0001"
                step="any"
                value={ingredient.amount}
                onChange={(event) =>
                  updateIngredient(
                    ingredient.id,
                    "amount",
                    event.target.value
                  )
                }
                aria-label={`Ingredient ${index + 1} amount`}
              />

              <select
                value={ingredient.unit}
                onChange={(event) =>
                  updateIngredient(
                    ingredient.id,
                    "unit",
                    event.target.value
                  )
                }
                aria-label={`Ingredient ${index + 1} unit`}
              >
                {INGREDIENT_UNITS.map(({ value, label }) => (
                  <option key={value} value={value}>
                    {label}
                  </option>
                ))}
              </select>

              <button
                type="button"
                className="icon-btn remove-btn"
                onClick={() => removeIngredient(ingredient.id)}
                aria-label={`Remove ingredient ${index + 1}`}
              >
                <i className="bi bi-x-lg"></i>
              </button>
            </div>
          ))}

          <button type="button" className="add-btn" onClick={addIngredient}>
            <i className="bi bi-plus-lg"></i> Add ingredient
          </button>
        </fieldset>

        <fieldset className="form-section">
          <legend>Steps</legend>

          <p className="form-hint">
            Reference an ingredient by typing its name in angle
            brackets, such as{" "}
            <code>{"<Flour>"}</code>.
          </p>

          <ol className="step-list">
            {steps.map((step, index) => (
              <li className="step-row" key={step.id}>
                <span className="step-number" aria-hidden="true">
                  {index + 1}
                </span>

                <textarea
                  value={step.text}
                  onChange={(event) =>
                    updateStep(step.id, event.target.value)
                  }
                  placeholder="e.g. Mix <Flour> with <Milk>."
                  rows={2}
                  aria-label={`Step ${index + 1} instructions`}
                />

                <div className="step-actions">
                  <button
                    type="button"
                    className="icon-btn"
                    onClick={() => moveStep(index, -1)}
                    disabled={index === 0}
                    aria-label={`Move step ${index + 1} up`}
                  >
                    <i className="bi bi-chevron-up"></i>
                  </button>

                  <button
                    type="button"
                    className="icon-btn"
                    onClick={() => moveStep(index, 1)}
                    disabled={index === steps.length - 1}
                    aria-label={`Move step ${index + 1} down`}
                  >
                    <i className="bi bi-chevron-down"></i>
                  </button>

                  <button
                    type="button"
                    className="icon-btn remove-btn"
                    onClick={() => removeStep(step.id)}
                    aria-label={`Remove step ${index + 1}`}
                  >
                    <i className="bi bi-x-lg"></i>
                  </button>
                </div>
              </li>
            ))}
          </ol>

          <button type="button" className="add-btn" onClick={addStep}>
            <i className="bi bi-plus-lg"></i> Add step
          </button>
        </fieldset>

        {error && <p className="form-error" role="alert">{error}</p>}

        {/* Save comes first so pressing Enter saves rather than drafts;
            CSS reverses the visual order */}
        <div className="form-actions">
          <button type="submit" className="save-btn">
            Save recipe
          </button>
          <button type="submit" value="draft" className="draft-btn">
            Save as draft
          </button>
        </div>
      </form>
    </main>
  );
}

function TimeInputs({
  label,
  hours,
  minutes,
  onHoursChange,
  onMinutesChange,
}) {
  return (
    <fieldset className="form-field time-inputs">
      <legend className="form-label">{label}</legend>

      <div className="time-fields">
        <label>
          <input
            type="number"
            min="0"
            step="1"
            value={hours}
            onChange={(event) => onHoursChange(event.target.value)}
            aria-label={`${label} hours`}
          />
          h
        </label>

        <label>
          <input
            type="number"
            min="0"
            max="59"
            step="1"
            value={minutes}
            onChange={(event) =>
              onMinutesChange(event.target.value)
            }
            aria-label={`${label} minutes`}
          />
          min
        </label>
      </div>
    </fieldset>
  );
}
