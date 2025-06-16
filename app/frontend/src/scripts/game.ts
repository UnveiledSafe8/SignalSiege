const searchQuery = new URLSearchParams(window.location.search);
const gameId = searchQuery.get("game_id");
const board = document.getElementById("board");
const startButton = document.getElementById("startButton");
const passButton = document.getElementById("passButton");
const newSubnetButton = document.getElementById("newSubnet");
const scoresDisplay = document.getElementById("scores");
const title = document.querySelector("#title h1");
let currGameBoard = null;
let gameOver = false;
let currTurn = false;

async function getGame() {
    const res = await fetch(`/${gameId}`, {method: "GET"});
    const newData = await res.json();
    currGameBoard = newData.game;
    gameOver = newData.game_over;
    await updateDisplay();
}

async function makeAIMove() {
    if (currTurn) {
        return;
    }

    const res = await fetch(`${gameId}/ai`, {method: "PUT"});
    const newData = await res.json();
    if (newData.valid_move) {
        await getGame();
        currTurn = true;
    }
}

async function makePlayerMove(move: string) {
    if (!currTurn) {
        return;
    }

    const res = await fetch(`${gameId}/move`, {method: "PUT",headers: {"Content-Type": "application/json"},body: JSON.stringify({"move": move})});
    const newData = await res.json();
    if (newData.valid_move) {
        currTurn = false;
        await getGame();
        await makeAIMove();
    }
}

function updateDisplay() {

    scoresDisplay.textContent = "";
    if (["easy", "medium", "hard", "very_hard", "insane"].includes(currGameBoard.difficulty)) {
        let humanColor = null;
        let humanScore = null;
        let aiColor = null;
        let aiScore = null;
        for (const player of Object.values(currGameBoard.players)) {
            if (!currGameBoard.ai_players.includes(player.color)) {
                humanColor = player.color;
                humanScore = player.score;
            } else {
                aiColor = player.color;
                aiScore = player.score;
            }
        }

        if(!gameOver) {
            title.textContent = `You (${humanColor}) VS ${currGameBoard.difficulty.charAt(0).toUpperCase() + currGameBoard.difficulty.slice(1,)} AI (${aiColor})`;
        } else {
            if (humanScore > aiScore) {
                title.textContent = `You (${humanColor}) Win!`;
            } else if (aiScore > humanScore) {
                title.textContent = `You (${humanColor}) Lost.`;
            } else {
                title.textContent = `You (${humanColor}) Tied!`;
            }
            passButton.style.display = "none";
        }
        scoresDisplay.textContent = `You (${humanColor}) - ${humanScore}  |  AI (${aiColor}) - ${aiScore}`;

    } else {
        title.textContent = `You VS Other`;
        scoresDisplay.textContent = `You () -   |  Other () - `;
    }

    board.innerHTML = "";

    for (let row = 0; row < currGameBoard.height; row++) {
        const rowDiv = document.createElement("div");
        rowDiv.className = "row";
        rowDiv.id = `row-${row}`;
        board.appendChild(rowDiv);
        for (let col = 0; col < currGameBoard.width; col++) {
            const nodeId = `${row}.${col}`;

            const node = document.createElement("button");
            node.className = "node";
            node.id = `node-${nodeId}`;
            node.type = "button";
            const nodeTitle = document.createElement("p");
            nodeTitle.className = "nodeId";
            nodeTitle.textContent = `${nodeId}`;
            node.appendChild(nodeTitle);

            document.getElementById(`row-${row}`).appendChild(node);
            document.getElementById(`node-${nodeId}`).addEventListener("click", () => {
                makePlayerMove(`${nodeId}`);
            });
            document.getElementById(`node-${nodeId}`).addEventListener("mouseenter", (e) => {
                for (const child of e.target.children) {
                    if (child.classList.contains("circle")) {
                        child.style.display = "inline-block";
                    }
                }
            });
            document.getElementById(`node-${nodeId}`).addEventListener("mouseleave", (e) => {
                for (const child of e.target.children) {
                    if (child.classList.contains("circle")) {
                        child.style.display = "none";
                    }
                }
            });

            const innerEle = document.createElement("div");
            const routerOwner = currGameBoard.graph[nodeId].router_owner;
            const nodeController = currGameBoard.graph[nodeId].controlled;
            
            if (routerOwner === "Black") {
                innerEle.classList.add("router", "black");
            } else if (routerOwner === "White") {
                innerEle.classList.add("router", "white");
            } else {
                innerEle.classList.add("circle");
            }

            if (nodeController == "Black") {
                document.getElementById(`node-${nodeId}`).classList.add("black");
            } else if (nodeController == "White") {
                document.getElementById(`node-${nodeId}`).classList.add("white");
            }

            document.getElementById(`node-${nodeId}`).appendChild(innerEle);
        }
    }
}



getGame();

startButton.addEventListener("click", () => {
    makeAIMove();
    getGame();
    startButton.style.display = "none";
    passButton.style.display = "inline-block";
    newSubnetButton.style.display = "inline-block";
});

passButton.addEventListener("click", () => {
    makePlayerMove("pass");
});

newSubnetButton.addEventListener("click", () => {
    const splitUrl = window.location.href.split("/");
    splitUrl.pop();
    splitUrl.push("play");
    const newUrl = splitUrl.join("/");
    window.location.href = newUrl;
});