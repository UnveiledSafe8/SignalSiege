"use strict";
const loginBtn = document.getElementById("login-button");
const registerBtn = document.getElementById("register-button");
registerBtn.addEventListener("click", () => {
    let splitURL = window.location.pathname.split("/");
    splitURL.pop();
    splitURL.push("register");
    splitURL = splitURL.join("/");
    window.location.href = splitURL;
});
loginBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    const emailInput = document.getElementById("email-input");
    const passwordInput = document.getElementById("password-input");
    const emailVal = emailInput.value;
    const passwordVal = passwordInput.value;
    if (!emailVal.match(/^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+$/)) {
        alert("Invalid Email");
        return;
    }
    const res = await fetch("/login-user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ "email": emailVal, "password": passwordVal })
    });
    const newData = await res.json();
    if (newData.login) {
        let splitURL = window.location.pathname.split("/");
        splitURL.pop();
        splitURL.push("");
        splitURL = splitURL.join("/");
        window.location.href = splitURL;
    }
    else {
        alert("Authentication Failed");
    }
});
