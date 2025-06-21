"use strict";
window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
        location.reload();
    }
});
const playBtn = document.getElementById("play-button");
const statsBtn = document.getElementById("stats-button");
const howBtn = document.getElementById("how-button");
const settingsBtn = document.getElementById("settings-button");
const accountBtn = document.getElementById("account-button");
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
    splitURL.push("play");
    splitURL = splitURL.join("/");
    redirectSmooth(splitURL);
});
async function auth_user() {
    const res = await fetch("/auth-me", {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" }
    });
    const newData = await res.json();
    return newData.login;
}
(async () => {
    if (await auth_user()) {
        accountBtn.textContent = "Logout";
        accountBtn.addEventListener("click", async (e) => {
            const res = await fetch("/logout-user", {
                method: "POST",
                credentials: "include",
                headers: { "Content-Type": "application/json" }
            });
            const newData = await res.json();
            if (!newData.logout) {
                return;
            }
            let splitURL = window.location.pathname.split("/");
            splitURL.pop();
            splitURL.push("");
            splitURL = splitURL.join("/");
            redirectSmooth(splitURL);
        });
    }
    else {
        accountBtn.textContent = "Login";
        accountBtn.addEventListener("click", (e) => {
            let splitURL = window.location.pathname.split("/");
            splitURL.pop();
            splitURL.push("login");
            splitURL = splitURL.join("/");
            redirectSmooth(splitURL);
        });
    }
})();
statsBtn.addEventListener("click", () => {
    let splitURL = window.location.pathname.split("/");
    splitURL.pop();
    splitURL.push("stats");
    splitURL = splitURL.join("/");
    redirectSmooth(splitURL);
});
settingsBtn.addEventListener("click", () => {
    let splitURL = window.location.pathname.split("/");
    splitURL.pop();
    splitURL.push("settings");
    splitURL = splitURL.join("/");
    redirectSmooth(splitURL);
});
function redirectSmooth(targetPage) {
    document.body.style.opacity = 0;
    setTimeout(() => {
        window.location.href = targetPage;
    }, 300);
}
;
let index = 0;
function typeTitle() {
    if (index < title.length) {
        heading.textContent += title[index++];
        setTimeout(typeTitle, 100);
    }
}
;
heading.textContent = "";
setTimeout(typeTitle, 700);
