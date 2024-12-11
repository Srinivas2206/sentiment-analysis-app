document
  .getElementById("analysis-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const text = document.querySelector("textarea[name='text']").value;
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: `text=${encodeURIComponent(text)}`,
    });

    const result = await response.json();
    const resultDiv = document.getElementById("result");

    if (result.error) {
      resultDiv.textContent = "Error: " + result.error;
    } else {
      resultDiv.innerHTML = `
            <p><strong>Text:</strong> ${result.text}</p>
            <p><strong>Sentiment:</strong> ${result.sentiment}</p>
            <p><strong>Score:</strong> ${result.score}</p>
        `;
    }
  });
