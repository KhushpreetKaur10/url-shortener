async function shorten() {

    const url = document.getElementById("url").value;
    const alias = document.getElementById("alias").value;

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

        if (!response.ok) {

            document.getElementById("result").innerText =
                data.error || "Error";

            return;
        }

        let output = "";

        if (data.message) {
            output += data.message + "\n\n";
        }

        if (data.short_url) {
            output += "Short URL: " + data.short_url;
        }

        document.getElementById("result").innerHTML = output + "<br><img src='" + data.qr_url + "' width='150'/>";
    }

    catch (error) {

        document.getElementById("result").innerText =
            "Server Error";
    }
}
