async function shorten() {
    const url = document.getElementById("url").value.trim();
    const alias = document.getElementById("alias").value.trim();
    try {
        const response = await fetch("/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                url,
                alias
            })
        });

        const data = await response.json();
        let html = "";
        if (data.message) {
            html += `<p>${data.message}</p>`;
        }

        if (data.short_url) {
            html += `
                <p>
                    <a href="${data.short_url}" target="_blank">
                        ${data.short_url}
                    </a>
                </p>
            `;
        }

        if (data.qr_url) {
            html += `
                <img
                    src="${data.qr_url}"
                    width="150"
                    alt="QR Code"
                />
            `;
        }
        document.getElementById("result").innerHTML = html;
    } catch (error) {
        document.getElementById("result").innerHTML =
            "<p>Server Error</p>";
    }
}
