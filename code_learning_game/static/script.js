function goTo(language) {
    window.location.href = "/dashboard/" + language;
}
function startChallenge(language) {
    window.location.href = "/challenge/" + language;
}
function goTo(language) {
    window.location.href = `/levels/${language}`;
}
function showHint() {
    fetch(`/get-challenge/${language}/${level}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("hint-text").innerText = "💡 Hint: " + data.hint;
        });
}
