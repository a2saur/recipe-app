import { useEffect, useState } from "react";
import {
  addListItem,
  addOwnedGrocery,
  deleteListItem,
  deleteOwnedGrocery,
  getGroceries,
  setListItemChecked,
} from "../api/groceries";
import { INGREDIENT_UNITS } from "../utils/ingredientUnits";
import { useGinghamBackground } from "../utils/useGinghamBackground";

// Keep in sync with GROCERY_LOCATIONS in backend/models.py.
const GROCERY_LOCATIONS = ["fridge", "freezer", "cupboard"];

function formatAmount({ amount, unit }) {
  return unit ? `${amount} ${unit}` : `${amount}`;
}

function formatExpiration(isoDate) {
  // Parse as a local date so it doesn't shift a day in timezones behind UTC
  const [year, month, day] = isoDate.split("-").map(Number);
  return new Date(year, month - 1, day).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
}

function isExpired(isoDate) {
  const today = new Date().toLocaleDateString("en-CA"); // YYYY-MM-DD
  return isoDate < today;
}

// Unchecked items first, then in the order they were added
function sortListItems(items) {
  return [...items].sort(
    (a, b) => a.is_checked - b.is_checked || a.id - b.id
  );
}

export default function GroceryList() {
  const [listItems, setListItems] = useState([]);
  const [owned, setOwned] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useGinghamBackground();

  useEffect(() => {
    getGroceries()
      .then((data) => {
        setListItems(data.list);
        setOwned(data.owned);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  // Runs an API call and shows its error instead of throwing
  async function run(action) {
    setError(null);
    try {
      await action();
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  }

  function handleAddListItem(item) {
    return run(async () => {
      const created = await addListItem(item);
      setListItems((current) => sortListItems([...current, created]));
    });
  }

  function handleToggleListItem(item) {
    return run(async () => {
      const updated = await setListItemChecked(item.id, !item.is_checked);
      setListItems((current) =>
        sortListItems(current.map((i) => (i.id === item.id ? updated : i)))
      );
    });
  }

  function handleDeleteListItem(id) {
    return run(async () => {
      await deleteListItem(id);
      setListItems((current) => current.filter((i) => i.id !== id));
    });
  }

  function handleAddOwned(grocery) {
    return run(async () => {
      const created = await addOwnedGrocery(grocery);
      setOwned((current) => [...current, created]);
    });
  }

  function handleDeleteOwned(id) {
    return run(async () => {
      await deleteOwnedGrocery(id);
      setOwned((current) => current.filter((g) => g.id !== id));
    });
  }

  if (loading) return <p>Loading groceries...</p>;

  return (
    <main>
      <div className="recipe-page grocery-page">
        <h1>Groceries</h1>

        {error && <p className="form-error" role="alert">{error}</p>}

        <div className="grocery-columns">
            <section className="grocery-section">
            <h2>Owned</h2>

            <IngredientForm submitLabel="Add" onSubmit={handleAddOwned} withStorage />

            {owned.length === 0 && (
              <p className="form-hint">You haven't added any groceries yet.</p>
            )}

            {GROCERY_LOCATIONS.map((location) => {
              const groceries = owned.filter((g) => g.location === location);
              if (groceries.length === 0) return null;

              return (
                <div key={location} className="grocery-location">
                  <h3>{location}</h3>
                  <ul className="grocery-items">
                    {groceries.map((grocery) => (
                      <li key={grocery.id} className="grocery-item">
                        <span className="grocery-name">{grocery.name}</span>
                        <span className="grocery-amount">{formatAmount(grocery)}</span>
                        {grocery.expiration_date && (
                          <ExpirationBadge grocery={grocery} />
                        )}

                        <button
                          type="button"
                          className="icon-btn remove-btn"
                          onClick={() => handleDeleteOwned(grocery.id)}
                          aria-label={`Remove ${grocery.name} from owned groceries`}
                        >
                          <i className="bi bi-x-lg"></i>
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              );
            })}
          </section>

          <section className="grocery-section">
            <h2>To buy</h2>

            <IngredientForm submitLabel="Add" onSubmit={handleAddListItem} />

            {listItems.length === 0 ? (
              <p className="form-hint">Your grocery list is empty.</p>
            ) : (
              <ul className="grocery-items">
                {listItems.map((item) => (
                  <li
                    key={item.id}
                    className={item.is_checked ? "grocery-item checked" : "grocery-item"}
                  >
                    <label className="grocery-check">
                      <input
                        type="checkbox"
                        checked={item.is_checked}
                        onChange={() => handleToggleListItem(item)}
                      />
                      <span className="grocery-name">{item.name}</span>
                      <span className="grocery-amount">{formatAmount(item)}</span>
                    </label>

                    <button
                      type="button"
                      className="icon-btn remove-btn"
                      onClick={() => handleDeleteListItem(item.id)}
                      aria-label={`Remove ${item.name} from the list`}
                    >
                      <i className="bi bi-x-lg"></i>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}

function ExpirationBadge({ grocery }) {
  const expired = isExpired(grocery.expiration_date);
  const label = grocery.is_hard_expiration ? "Use by" : "Best before";

  let className = "expiration-badge";
  if (expired) className += grocery.is_hard_expiration ? " expired-hard" : " expired-soft";

  return (
    <span className={className}>
      {grocery.is_hard_expiration && <i className="bi bi-exclamation-circle"></i>}{" "}
      {label} {formatExpiration(grocery.expiration_date)}
    </span>
  );
}

// Name / amount / unit form; withStorage adds location and expiration fields
function IngredientForm({ submitLabel, onSubmit, withStorage = false }) {
  const [name, setName] = useState("");
  const [amount, setAmount] = useState("1");
  const [unit, setUnit] = useState("");
  const [location, setLocation] = useState(GROCERY_LOCATIONS[0]);
  const [expirationDate, setExpirationDate] = useState("");
  const [isHardExpiration, setIsHardExpiration] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!name.trim()) return;

    const item = { name: name.trim(), amount: Number(amount || 1), unit };
    if (withStorage) {
      item.location = location;
      item.expiration_date = expirationDate || null;
      item.is_hard_expiration = Boolean(expirationDate) && isHardExpiration;
    }

    // Only clear the form if it saved, so a failed entry isn't lost
    if (await onSubmit(item)) {
      setName("");
      setAmount("1");
      setUnit("");
      setExpirationDate("");
      setIsHardExpiration(false);
    }
  }

  return (
    <form className="grocery-form" onSubmit={handleSubmit}>
      <div className="grocery-form-row">
        <input
          type="text"
          value={name}
          onChange={(event) => setName(event.target.value)}
          placeholder="e.g. Milk"
          aria-label="Ingredient name"
          required
        />
        <input
          type="number"
          min="0.0001"
          step="any"
          value={amount}
          onChange={(event) => setAmount(event.target.value)}
          aria-label="Amount"
        />
        <select
          value={unit}
          onChange={(event) => setUnit(event.target.value)}
          aria-label="Unit"
        >
          {INGREDIENT_UNITS.map(({ value, label }) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </div>

      {withStorage && (
        <div className="grocery-form-row storage-row">
          <select
            value={location}
            onChange={(event) => setLocation(event.target.value)}
            aria-label="Location"
          >
            {GROCERY_LOCATIONS.map((loc) => (
              <option key={loc} value={loc}>
                {loc}
              </option>
            ))}
          </select>
          <input
            type="date"
            value={expirationDate}
            onChange={(event) => setExpirationDate(event.target.value)}
            aria-label="Expiration date (optional)"
          />
          <label className="grocery-hard-toggle">
            <input
              type="checkbox"
              checked={isHardExpiration}
              onChange={(event) => setIsHardExpiration(event.target.checked)}
              disabled={!expirationDate}
            />
            Hard deadline
          </label>
        </div>
      )}

      <button type="submit" className="add-btn">
        <i className="bi bi-plus-lg"></i> {submitLabel}
      </button>
    </form>
  );
}
