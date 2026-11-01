// Singular units an ingredient can be measured in; "" means individual items.
// Keep in sync with INGREDIENT_UNITS in backend/models.py.
export const INGREDIENT_UNITS = [
  { value: "", label: "— (individual items)" },
  { value: "clove", label: "clove" },
  { value: "cup", label: "cup" },
  { value: "tbsp", label: "tbsp" },
  { value: "tsp", label: "tsp" },
  { value: "fl oz", label: "fl oz" },
  { value: "ml", label: "ml" },
  { value: "lb", label: "lb" },
  { value: "oz", label: "oz" },
  { value: "g", label: "g" },
];
