const backBtn = document.querySelector('button[type="button"]:first-of-type');
const heightInput = document.getElementById("height");
const widthInput = document.getElementById("width");
const fullInput = document.querySelector("input[type='checkbox']");
const board = document.getElementById("board-display");
const submitBtn = document.querySelector('button[type="submit"]');
const form = document.getElementById("game-settings");
const humanBtn = document.querySelector('input[value="human"]');
const computerBtn = document.querySelector('input[value="computer"]');
const localBtn = document.querySelector('input[value="local"]');
const opponentRadioGroup = document.getElementById("opponent-radio-group");
const radioGroup = [humanBtn, computerBtn, localBtn];
const computerDifficultyInput = document.querySelector('select[name="difficulty"]');

const maxHeight = 25;
const minHeight = 3;
const maxWidth = 25;
const minWidth = 3;

backBtn.addEventListener("click", () => {
    let splitURL = window.location.pathname.split("/");
    splitURL.pop();
    splitURL.push("index.html");
    splitURL = splitURL.join("/");
    redirectSmooth(splitURL);
});
heightInput.addEventListener("change", updateBoard);
widthInput.addEventListener("change", updateBoard);
fullInput.addEventListener("change", updateBoard);
radioGroup.forEach(element => element.addEventListener("change", (event) => updateAdditionalSettingsDisplay(event.target.value)));
submitBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = {
        "height": Number(formData.get("height")),
        "width": Number(formData.get("width")),
        "full": formData.get("full") ? true:false,
        "opponent": formData.get("opponent"),
        "difficulty": formData.get("difficulty")
    };

    if (isNaN(data.height) || data.height > maxHeight || data.height < minHeight) {
        alert(`Invalid height, ensure your number is between ${minHeight} and ${maxHeight} inclusive`);
        return;
    } else if (isNaN(data.width) || data.width > maxWidth || data.width < minWidth) {
        alert(`Invalid width, ensure your number is between ${minWidth} and ${maxWidth} inclusive`);
        return;
    }else if (data.opponent === "computer" && !data.difficulty) {
        alert("Must select a difficulty");
        return;
    };

    localStorage.setItem("game-settings", JSON.stringify(data));

});
document.addEventListener("mousemove", (e) => {
  const trail = document.createElement("div");
  trail.className = "trail";
  trail.style.left = `${e.pageX}px`;
  trail.style.top = `${e.pageY}px`;
  trail.textContent = Math.floor(Math.random() * 2);
  document.body.appendChild(trail);

  setTimeout(() => {
    trail.remove();
  }, 500);
});

function updateBoard() {
    const heightVal = heightInput.value;
    const widthVal = widthInput.value;
    const fullValue = fullInput.checked;

    board.innerHTML = "";

    for (let i = 0; i < heightVal; i++) {
        board.innerHTML += `<div class='board-row' id="row-${i}">`;
        let currRow = document.getElementById("row-" + i);
        for (let j = 0; j < widthVal ; j++) {
            if (fullValue) {
                currRow.innerHTML += `<span class="node" id="${i+1}.${j+1}"></span>`;
            } else {
                let empty = Math.floor(Math.random() * 20);
                if (empty === 0) {
                    currRow.innerHTML += `<span class="node empty" id="${i+1}.${j+1}"></span>`;
                } else {
                    currRow.innerHTML += `<span class="node" id="${i+1}.${j+1}"></span>`;
                }
            }
        }
        board.innerHTML += "</div>";
    }

};

function updateAdditionalSettingsDisplay(value) {
    if (value === "computer") {
        computerDifficultyInput.style.opacity = 1;
        computerDifficultyInput.required = true;
    } else {
        computerDifficultyInput.style.opacity = 0;
        computerDifficultyInput.required = false;
    };
};

function redirectSmooth(targetPage) {
    document.body.style.opacity = 0;
    setTimeout(() => {
        window.location.href = targetPage;
    }, 300);
};


rawData = localStorage.getItem("game-settings");
if (rawData) {
    currData = JSON.parse(rawData);
    heightInput.value = currData.height;
    widthInput.value = currData.width;
    fullInput.checked = currData.full;
    if (currData.opponent === humanBtn.value) {
        humanBtn.checked = true;
        updateAdditionalSettingsDisplay("human");
    } else if (currData.opponent === localBtn.value) {
        localBtn.checked = true;
        updateAdditionalSettingsDisplay("local");
    } else {
        computerBtn.checked = true;
        updateAdditionalSettingsDisplay("computer");
    };
    computerDifficultyInput.value = currData.difficulty;
} else {
    heightInput.value = 10;
    widthInput.value = 10;
    fullInput.checked = true;
    humanBtn.checked = true;
    computerDifficultyInput.style.opacity = 0;
    computerDifficultyInput.value = "";
};

updateBoard();