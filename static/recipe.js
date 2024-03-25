document.addEventListener('DOMContentLoaded', function() {
    const addRecipeBtn = document.getElementById('addRecipeBtn');
    const addRecipeModal = document.getElementById('addRecipeModal');
    const closeBtn = document.querySelector('.close');
    const recipeForm = document.getElementById('recipeForm');
    const recipesContainer = document.getElementById('recipesContainer');
    const ingredientFilter = document.getElementById('ingredientFilter');

    addRecipeBtn.addEventListener('click', function() {
        addRecipeModal.style.display = 'block';
    });

    closeBtn.addEventListener('click', function() {
        addRecipeModal.style.display = 'none';
    });

    recipeForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const recipeName = document.getElementById('recipeName').value;
        const ingredients = document.getElementById('ingredients').value;
        const instructions = document.getElementById('instructions').value;

        const recipe = {
            name: recipeName,
            ingredients: ingredients,
            instructions: instructions
        };

        displayRecipe(recipe);
        addRecipeModal.style.display = 'none';
        recipeForm.reset();
    });

    ingredientFilter.addEventListener('input', function() {
        const filterValue = ingredientFilter.value.toLowerCase();
        const recipes = document.querySelectorAll('.recipe-card');

        recipes.forEach(function(recipe) {
            const ingredients = recipe.querySelector('p.ingredients').textContent.toLowerCase();
            if (ingredients.includes(filterValue)) {
                recipe.style.display = 'block';
            } else {
                recipe.style.display = 'none';
            }
        });
    });

    function displayRecipe(recipe) {
        const recipeCard = document.createElement('div');
        recipeCard.classList.add('recipe-card');
        recipeCard.innerHTML = `
            <h2>${recipe.name}</h2>
            <h3>Ingredients:</h3>
            <p class="ingredients">${recipe.ingredients}</p>
            <h3>Instructions:</h3>
            <p>${recipe.instructions}</p>
        `;
        recipesContainer.appendChild(recipeCard);
    }
});