const playBtn = document.getElementById("play-button");
const statsBtn = document.getElementById("stats-button");
const howBtn = document.getElementById("how-button");
const settingsBtn = document.getElementById("settings-button");
const heading = document.querySelector("h1");

const title = heading.textContent;

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

playBtn.addEventListener("click", () => {
    let splitURL = window.location.pathname.split("/");
    splitURL.pop();
    splitURL.push("play.html");
    splitURL = splitURL.join("/");
    redirectSmooth(splitURL);
});

howBtn.addEventListener("click", () => {
    let splitURL = window.location.pathname.split("/");
    splitURL.pop();
    splitURL.push("guide.html");
    splitURL = splitURL.join("/");
    redirectSmooth(splitURL);
});

function redirectSmooth(targetPage) {
    document.body.style.opacity = 0;
    setTimeout(() => {
        window.location.href = targetPage;
    }, 300);
};

let index = 0;
function typeTitle() {
    if (index < title.length) {
        heading.textContent += title[index++];
        setTimeout(typeTitle, 100);
    }
};

heading.textContent = "";
setTimeout(typeTitle, 200);