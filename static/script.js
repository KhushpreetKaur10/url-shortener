function shorten() {
        fetch('/shorten', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            url: document.getElementById("url").value,
            alias: document.getElementById("alias").value
        })
    })
    .then(res => res.json())
    .then(data => {

        let output = "";

        if (data.message) {
            output += data.message + "\n";
        }

        if (data.short_url) {
            output += "Short URL: " + data.short_url;
        }

        document.getElementById("result").innerText = output;
    });
    }