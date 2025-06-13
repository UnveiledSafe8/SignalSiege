"use strict";
const searchQuery = new URLSearchParams(window.location.search);
const gameId = searchQuery.get("game_id");
const board = document.getElementById("board");
const startButton = document.getElementById("startButton");
const passButton = document.getElementById("passButton");
const newSubnetButton = document.getElementById("newSubnet");
const scoresDisplay = document.getElementById("scores");
const title = document.querySelector("#title h1");
let currGameBoard = null;
let currScores = null;
let gameStarted = false;
let currTurn = false;
startButton.addEventListener("click", () => {
    fetch(`/${gameId}/start`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(getGameState)
        .then(() => {
        startButton.style.display = "none";
        gameStarted = true;
        currTurn = true;
        passButton.style.display = "inline-block";
        newSubnetButton.style.display = "inline-block";
    });
});
passButton.addEventListener("click", () => {
    tryMove("pass");
});
newSubnetButton.addEventListener("click", () => {
    const url = window.location.href.split("/");
    url.pop();
    url.push("play");
    window.location.href = url.join("/");
});
async function getGameState() {
    fetch(`/${gameId}/state`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(async (newData) => {
        currGameBoard = newData.board;
        currScores = newData.scores;
        if (newData.difficulty === "self") {
            title.textContent = `You VS Opponent`;
        }
        else {
            title.textContent = `You (${newData.human_players[0]}) VS ${newData.difficulty} AI (${newData.ai_players[0]})`;
        }
        displayGame();
        return newData;
    });
}
;
function displayGame() {
    let index = 0;
    board.innerHTML = "";
    for (const row of currGameBoard) {
        const newRow = document.createElement("div");
        newRow.setAttribute("id", `row-${index}`);
        newRow.setAttribute("class", "row");
        board.appendChild(newRow);
        let index2 = 0;
        for (const node of row) {
            const newButton = document.createElement("button");
            newButton.setAttribute("class", "node");
            newButton.setAttribute("type", "button");
            newButton.setAttribute("id", `${index}.${index2}`);
            const buttonText = document.createElement("p");
            buttonText.textContent = `${index}.${index2}`;
            buttonText.setAttribute("class", "nodeId");
            newButton.appendChild(buttonText);
            newButton.appendChild(document.createElement("span"));
            newButton.addEventListener("click", (event) => {
                tryMove(event.currentTarget.id);
            });
            newButton.addEventListener("mouseenter", (event) => {
                const children = event.target.children;
                for (const child of children) {
                    if (!child.classList.contains("rock")) {
                        child.style.display = "inline-block";
                    }
                }
                ;
            });
            newButton.addEventListener("mouseleave", (event) => {
                const children = event.target.children;
                for (const child of children) {
                    if (!child.classList.contains("rock")) {
                        child.style.display = "none";
                    }
                }
                ;
            });
            document.getElementById(`row-${index}`).appendChild(newButton);
            index2++;
            if (node === '.') {
                const circle = document.createElement("div");
                circle.setAttribute("class", "circle");
                newButton.appendChild(circle);
            }
            else if (node === "B") {
                const rock = document.createElement("div");
                rock.setAttribute("class", "rock");
                rock.classList.add("black");
                newButton.appendChild(rock);
            }
            else if (node === "W") {
                const rock = document.createElement("div");
                rock.setAttribute("class", "rock");
                rock.classList.add("white");
                newButton.appendChild(rock);
            }
            else if (node == "w") {
                const circle = document.createElement("div");
                circle.setAttribute("class", "circle");
                newButton.appendChild(circle);
                newButton.classList.add("white");
            }
            else if (node == "b") {
                const circle = document.createElement("div");
                circle.setAttribute("class", "circle");
                newButton.appendChild(circle);
                newButton.classList.add("black");
            }
        }
        ;
        index++;
    }
    ;
    scoresDisplay.innerHTML = "";
    for (const [color, score] of Object.entries(currScores)) {
        scoresDisplay.textContent += ` ${color}: ${score} | `;
    }
    ;
    scoresDisplay.textContent = scoresDisplay.textContent.split("").splice(0, scoresDisplay.textContent.length - 3).join("");
}
;
async function tryMove(move) {
    if (gameStarted && currTurn) {
        currTurn = false;
        fetch(`/${gameId}/move`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "move": move })
        })
            .then((response) => response.json())
            .then(async (newData) => {
            if (newData.valid_move) {
                currGameBoard = newData.board;
                currScores = newData.scores;
                displayGame();
                await getGameState();
                currTurn = true;
            }
            ;
        });
    }
    ;
}
;
getGameState();
