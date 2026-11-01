
from datetime import date, datetime, timezone
from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

db = SQLAlchemy()

# Units an ingredient amount can be measured in, always singular.
# "" means individual items (e.g. "2 eggs").
# Keep in sync with INGREDIENT_UNITS in frontend/src/utils/ingredientUnits.js.
INGREDIENT_UNITS = [
    "",
    "clove",
    "cup",
    "tbsp",
    "tsp",
    "fl oz",
    "ml",
    "lb",
    "oz",
    "g",
]

# Where a grocery item is stored.
GROCERY_LOCATIONS = [
    "fridge",
    "freezer",
    "cupboard",
]


# ============================================================
# Recipe
# ============================================================

class Recipe(db.Model):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    serving_size: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    active_time: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Minutes
    overall_time: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Minutes

    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False,)

    is_draft: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    to_make: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    ingredient_uses: Mapped[list["RecipeIngredientUse"]] = (
        relationship(
            back_populates="recipe",
            cascade="all, delete-orphan",
            order_by="RecipeIngredientUse.id",
        )
    )

    steps: Mapped[list["RecipeStep"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        order_by="RecipeStep.step_number",
    )


# ============================================================
# Ingredient
# ============================================================

class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)

    group_links: Mapped[list["IngredientGroupMembership"]] = (
        relationship(
            back_populates="ingredient",
            cascade="all, delete-orphan",
        )
    )

    recipe_uses: Mapped[list["RecipeIngredientUse"]] = (
        relationship(back_populates="ingredient")
    )

    cost_entries: Mapped[list["IngredientCostEntry"]] = (
        relationship(
            back_populates="ingredient",
            cascade="all, delete-orphan",
        )
    )

    owned_groceries: Mapped[list["OwnedGrocery"]] = (
        relationship(back_populates="ingredient")
    )

    grocery_list_items: Mapped[list["GroceryListItem"]] = (
        relationship(back_populates="ingredient")
    )


# ============================================================
# Allergen / Dietary Restriction Groups
# ============================================================

class IngredientGroup(db.Model):
    __tablename__ = "ingredient_groups"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    group_type: Mapped[str] = mapped_column(
        String(30), nullable=False
    )  # "allergen" or "dietary"

    __table_args__ = (
        UniqueConstraint(
            "name", "group_type",
            name="uq_ingredient_group_name_type",
        ),
    )

    ingredient_links: Mapped[list["IngredientGroupMembership"]] = (
        relationship(
            back_populates="group",
            cascade="all, delete-orphan",
        )
    )


class IngredientGroupMembership(db.Model):
    __tablename__ = "ingredient_group_memberships"

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        primary_key=True,
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient_groups.id", ondelete="CASCADE"),
        primary_key=True,
    )

    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="group_links"
    )
    group: Mapped["IngredientGroup"] = relationship(
        back_populates="ingredient_links"
    )


# ============================================================
# Recipe Ingredient Use
# ============================================================

class RecipeIngredientUse(db.Model):
    __tablename__ = "recipe_ingredient_uses"

    id: Mapped[int] = mapped_column(primary_key=True)

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
    )
    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="RESTRICT"),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False
    )
    unit: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    recipe: Mapped["Recipe"] = relationship(
        back_populates="ingredient_uses"
    )
    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="recipe_uses"
    )

    steps: Mapped[list["RecipeStep"]] = relationship(
        back_populates="ingredient_use"
    )

    __table_args__ = (
        CheckConstraint(
            "unit IN ("
            + ", ".join(f"'{unit}'" for unit in INGREDIENT_UNITS)
            + ")",
            name="ck_recipe_ingredient_use_unit",
        ),
    )

    @validates("unit")
    def validate_unit(self, key, unit):
        if unit not in INGREDIENT_UNITS:
            raise ValueError(f"Invalid ingredient unit: {unit!r}")
        return unit


# ============================================================
# Ingredient Cost Entry
# ============================================================

class IngredientCostEntry(db.Model):
    __tablename__ = "ingredient_cost_entries"

    id: Mapped[int] = mapped_column(primary_key=True)

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        nullable=False,
    )

    brand: Mapped[str | None] = mapped_column(
        String(150), nullable=True
    )
    additional_details: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Examples: "1 box", "1 bag", "1 bottle"
    payment_unit: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    # Examples: "16 oz", "500 g"; null if not applicable
    amount_unit: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    # Price paid for the payment unit/package
    cost_per_unit: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False
    )

    # Examples: "g", "oz", "ml", "each"
    cooking_unit: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    # Price per cooking unit, in the same currency as cost_per_unit
    cost_per_cooking_unit: Mapped[Decimal] = mapped_column(
        Numeric(14, 8), nullable=False
    )

    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="cost_entries"
    )


# ============================================================
# Owned Grocery (what's already in the kitchen)
# ============================================================

class OwnedGrocery(db.Model):
    __tablename__ = "owned_groceries"

    id: Mapped[int] = mapped_column(primary_key=True)

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="RESTRICT"),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False
    )
    unit: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    # One of GROCERY_LOCATIONS
    location: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    expiration_date: Mapped[date | None] = mapped_column(
        Date, nullable=True
    )
    # True for a hard deadline (e.g. "use by"),
    # False for a soft one (e.g. "best before")
    is_hard_expiration: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="owned_groceries"
    )

    __table_args__ = (
        CheckConstraint(
            "unit IN ("
            + ", ".join(f"'{unit}'" for unit in INGREDIENT_UNITS)
            + ")",
            name="ck_owned_grocery_unit",
        ),
        CheckConstraint(
            "location IN ("
            + ", ".join(f"'{location}'" for location in GROCERY_LOCATIONS)
            + ")",
            name="ck_owned_grocery_location",
        ),
    )

    @validates("unit")
    def validate_unit(self, key, unit):
        if unit not in INGREDIENT_UNITS:
            raise ValueError(f"Invalid ingredient unit: {unit!r}")
        return unit

    @validates("location")
    def validate_location(self, key, location):
        if location not in GROCERY_LOCATIONS:
            raise ValueError(f"Invalid grocery location: {location!r}")
        return location


# ============================================================
# Grocery List Item (what still needs to be bought)
# ============================================================

class GroceryListItem(db.Model):
    __tablename__ = "grocery_list_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredients.id", ondelete="RESTRICT"),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 4), nullable=False
    )
    unit: Mapped[str] = mapped_column(
        String(50), nullable=False
    )

    # Ticked off while shopping
    is_checked: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="grocery_list_items"
    )

    __table_args__ = (
        CheckConstraint(
            "unit IN ("
            + ", ".join(f"'{unit}'" for unit in INGREDIENT_UNITS)
            + ")",
            name="ck_grocery_list_item_unit",
        ),
    )

    @validates("unit")
    def validate_unit(self, key, unit):
        if unit not in INGREDIENT_UNITS:
            raise ValueError(f"Invalid ingredient unit: {unit!r}")
        return unit


# ============================================================
# Recipe Step
# ============================================================

class RecipeStep(db.Model):
    __tablename__ = "recipe_steps"

    id: Mapped[int] = mapped_column(primary_key=True)

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"),
        nullable=False,
    )

    step_number: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    instruction: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    # Optional: which recipe ingredient use is relevant to this step
    ingredient_use_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "recipe_ingredient_uses.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    recipe: Mapped["Recipe"] = relationship(
        back_populates="steps"
    )
    ingredient_use: Mapped["RecipeIngredientUse | None"] = (
        relationship(back_populates="steps")
    )

    __table_args__ = (
        UniqueConstraint(
            "recipe_id",
            "step_number",
            name="uq_recipe_step_number",
        ),
        CheckConstraint(
            "step_number > 0",
            name="ck_recipe_step_positive_number",
        ),
    )
