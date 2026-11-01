import { Fragment } from "react";

// Get ingredients used in a recipe step and render
export function RecipeStepDetails({ step, ingredients }) {
    const ingNames = ingredients.map((ing) => ing.name.toLowerCase());
    const used = [];

    const content = step.instruction.split("<").map((part, i) => {
        const [name, rest] = part.split(">");
        const index = rest === undefined ? -1 : ingNames.indexOf(name.toLowerCase());
        if (index === -1) return part; // no ingredient included

        used.push(ingredients[index].name);
        return (
        <Fragment key={i}>
            <span className="ingredient-text">{name}</span>
            {rest}
        </Fragment>
        );
    });

    return (
        <>
        <span>{step.step_number}. {content}</span>
        {used.length > 0 && <span className="step-ingredients"> ({used.join(", ")})</span>}
        </>
    );
}

// // Get ingredients used in a recipe step and render
// export function RecipeStepDetails({ stepInstruction, ingredients }) {
//   let ingNames = ingredients.map(ing => ing.name.toLowerCase());
//   let parts = stepInstruction.split("<");

//   let formattedStep = document.createElement('span');
//   let ingredientsUsed = document.createElement('span');
//   for (let i = 0; i < parts.length; i++){
//     let subparts = parts[i].split(">");
//     if (subparts.length == 1){
//         // no ingredient included
//         formattedStep.textContent += parts[i];
//     } else {
//         if (ingNames.includes(subparts[0].toLowerCase())){
//             let subStep = document.createElement('span');
//             subStep.textContent = subparts[0];
//             subStep.classList.add('ingredient-text');
//             formattedStep.appendChild(subStep);
//             formattedStep.textContent += subparts[1];

//             let ingredientInfo = ingredients[ingNames.indexOf(subparts[0].toLowerCase())];
//             if (ingredientInfo){
//                 ingredientsUsed.textContent += ingredientInfo.name;
//                 ingredientsUsed.textContent += ", ";
//             }
//         } else {
//             formattedStep.textContent += parts[i];
//         }
//     }
//   }

//   console.log(formattedStep);
// }
