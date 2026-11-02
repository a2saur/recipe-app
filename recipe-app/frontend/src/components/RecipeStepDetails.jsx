import { Fragment } from "react";

// Get ingredients used in a recipe step and render
export function RecipeStepDetails({ step, ingredients }) {
    const ingNames = ingredients.map((ing) => ing.name.toLowerCase());
    const usedIngs = [];

    // Example: Combine <flour> with <water, 0.5> and mix
    const content = step.instruction.split("<").map((part, i) => {
        // --eg: content = ["Combine ", "flour> with ", "water, 0.5> and mix"]
        const [ingInfo, rest] = part.split(">");
        // --eg for idx 2: name = "water, 0.5", rest = " and mix"

        if (rest === undefined){
            // There was no ingredient, e.g. "Combine "
            return part;
        } else {
            // Could be ingredient, portion
            const [name, portion] = ingInfo.split(", ");
            const index = ingNames.indexOf(name.toLowerCase());
            
            if (index != -1){
                const ingUse = portion === undefined ? ingredients[index].amount : ingredients[index].amount*parseFloat(portion);
                usedIngs.push(ingUse + " " + ingredients[index].unit + " " + ingredients[index].name);
    
                return (
                <Fragment key={i}>
                    <span className="ingredient-text">{name}</span>
                    {rest}
                </Fragment>
                );
            } else {
                // Wasn't a valid ingredient
                return part;
            }
        }
    });

    return (
        <>
        <span>{step.step_number}. {content}</span>
        {usedIngs.length > 0 && <span className="step-ingredients"> 
            <ul className="recipe-step-used-ings">
              {usedIngs.join(", ")}
            </ul>
            </span>}
        </>
    );
}