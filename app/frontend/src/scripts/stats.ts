async function auth_user() {
    const res = await fetch("/auth-me", {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" }
    });
    const newData = await res.json();

    return newData.login
}

async function get_user_info() {
    if (!await auth_user()) {
        return;
    }

    const res = await fetch("/get-player-info", {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" }
    });
    const newData = await res.json();

    const title = document.getElementById("title") as HTMLHeadingElement;

    if (newData.username) {
        title.textContent = newData.username;
    } else {
        title.textContent = newData.email.slice(0, newData.email.indexOf("@"));
    }
}

async function get_user_stats() {
    if (!await auth_user()) {
        return;
    }

    const res = await fetch("/get-player-stats", {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json"}
    });
    const newData = await res.json();

    let totalAiWins = 0;
    let totalAiLosses = 0;
    function updateAiStats(ai) {
        const aiWinsText = document.getElementById(`${ai.difficulty}-ai-wins`) as HTMLSpanElement;
        const aiWins = ai.wins;
        const aiLossesText = document.getElementById(`${ai.difficulty}-ai-losses`) as HTMLSpanElement;
        const aiLosses = ai.losses;
        const aiGamesText = document.getElementById(`${ai.difficulty}-ai-games`) as HTMLSpanElement;
        const aiGames = aiWins + aiLosses;
        const aiRatioBar = document.getElementById(`${ai.difficulty}-ai-ratio`) as HTMLDivElement;
        const aiRatio = aiGames > 0 ? aiWins / aiGames : 0;

        aiWinsText.textContent = aiWins;
        aiLossesText.textContent = aiLosses;
        aiGamesText.textContent = aiGames;
        aiRatioBar.style.background = `linear-gradient(90deg, var(--primary-dark-color) 0%, var(--primary-dark-color) ${aiRatio * 100}%,
        transparent ${aiRatio * 100}%, transparent 100%)`;

        totalAiWins += aiWins;
        totalAiLosses += aiLosses;
    }

    newData.forEach(updateAiStats);

    const totalAiGames = totalAiLosses + totalAiLosses;
    const totalAiGamesText = document.getElementById("total-ai-games");
    const totalAiWinsText = document.getElementById("total-ai-wins");
    const totalAiLossesText = document.getElementById("total-ai-losses");
    const totalAiRatio = totalAiGames > 0 ? totalAiWins / totalAiGames : 0;
    const totalAiRatioBar = document.getElementById("total-ai-ratio");

    totalAiGamesText.textContent = totalAiGames;
    totalAiLossesText.textContent = totalAiLosses;
    totalAiWinsText.textContent = totalAiWins;
    totalAiRatioBar.style.background = `linear-gradient(90deg, var(--primary-dark-color) 0%, var(--primary-dark-color) ${totalAiRatio * 100}%,
        transparent ${totalAiRatio * 100}%, transparent 100%)`;

}

get_user_info();
get_user_stats();

document.querySelector("button:first-of-type").addEventListener("click", () => {
    let splitURL = window.location.pathname.split("/");
    splitURL.pop();
    splitURL.push("");
    splitURL = splitURL.join("/");
    window.location.href = splitURL;
});