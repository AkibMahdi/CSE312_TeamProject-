document.addEventListener('DOMContentLoaded', function() {
    const timerElement = document.getElementById('timer');
    const timerWrapper = document.getElementById('timer-container');
    const dishNameElement = document.getElementById('dish-name');
    const buttonsContainer = document.getElementById('ingredient-buttons');
    const messageDisplay = document.getElementById('message-display');
    let currentGameId = null; // Define game ID at the top to be used across functions
    let timeLeft = 20;
    let gameTimer;

    function startGame() {
        fetch('/scramble/start').then(response => response.json()).then(data => {
            currentGameId = data.game_id; // Store the current game ID from the server response
            setupGame(data);
        }).catch(error => console.error('Failed to start game:', error));
    }

    function setupGame(data) {
        dishNameElement.textContent = data.dish_name;
        buttonsContainer.innerHTML = '';
        data.ingredients.forEach(ingredient => {
            const button = document.createElement('button');
            button.textContent = ingredient;
            button.onclick = () => toggleIngredientSelection(button, ingredient);
            buttonsContainer.appendChild(button);
        });
        dishNameElement.style.display = 'block';
        buttonsContainer.style.display = 'grid'; 
        timerWrapper.style.display = 'block';
        messageDisplay.textContent = ''; 
        timeLeft = 20;
        gameTimer = setInterval(updateTimer, 1000);
    }

    function updateTimer() {
        if (timeLeft > 0) {
            timeLeft--;
            timerElement.textContent = timeLeft;
        } else {
            clearInterval(gameTimer);
            endGame(false, "Time is up! Try again!");
        }
    }

    function toggleIngredientSelection(button, ingredient) {
        button.classList.toggle('active');
        fetch('/scramble/guess', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                game_id: currentGameId,
                guessed_ingredient: ingredient
            })
        }).then(response => response.json()).then(data => {
            if (data.win) {
                clearInterval(gameTimer);
                endGame(true, "Congratulations! You've guessed all ingredients correctly!", data.all_correct);
            } else {
                button.style.backgroundColor = 'red'; // Indicate incorrect guess if not a win
                if (data.hint) {
                    messageDisplay.textContent = `Hint: ${data.hint} is one of the ingredients.`;
                }
            }
        }).catch(error => console.error('Error guessing ingredients:', error));
    }

    function endGame(won, message, correctIngredients = []) {
        disableButtons();
        if (!won) {
            highlightCorrectIngredients(correctIngredients);
        }
        messageDisplay.textContent = message;
        messageDisplay.style.color = won ? 'green' : 'red';
    }

    function highlightCorrectIngredients(correctIngredients) {
        document.querySelectorAll('#ingredient-buttons button').forEach(button => {
            if (correctIngredients.includes(button.textContent)) {
                button.style.backgroundColor = 'green';
            }
        });
    }

    function disableButtons() {
        document.querySelectorAll('#ingredient-buttons button').forEach(button => {
            button.disabled = true;
        });
    }

    window.startGame = startGame;
});
