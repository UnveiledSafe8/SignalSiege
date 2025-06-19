"use strict";
const registerBtn = document.getElementById("register-button");
const loginBtn = document.getElementById("login-button");
registerBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const emailInput = document.getElementById("email-input");
    const passwordInput = document.getElementById("password-input");
    const emailVal = emailInput.value;
    const passwordVal = passwordInput.value;
    const res = await fetch("/register-user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "email": emailVal, "password": passwordVal })
    });
    const newData = await res.json();
    if (newData.id) {
        let splitURL = window.location.pathname.split("/");
        splitURL.pop();
        splitURL.push("login");
        splitURL = splitURL.join("/");
        alert("Account Created");
        window.location.href = splitURL;
    }
    else {
        alert("An Account With That Email Already Exists");
    }
});
loginBtn.addEventListener("click", () => {
    let splitURL = window.location.pathname.split("/");
    splitURL.pop();
    splitURL.push("login");
    splitURL = splitURL.join("/");
    window.location.href = splitURL;
});
