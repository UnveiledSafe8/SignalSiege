async function get_user_stats() {
    const token = window.localStorage.getItem("token");
    if (!token) {
        return;
    }

    const res = await fetch("/get-player-stats", {
        method: "GET",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` }
    });
    const newData = await res.json();
    console.log(newData);
}

get_user_stats();