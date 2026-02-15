function runCode() {
    let code = document.getElementById("codeInput").value;

    fetch("/run_code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("outputBox").innerText = data.output;
        document.getElementById("pointDisplay").innerText = "Points Earned: " + data.points;
    });
}

function getHint() {
    alert("Hint: Use print('Hello, Bhavana')");
}
