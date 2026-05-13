async function sendMessage() {

    const input =
        document.getElementById("user-input");

    const chatBox =
        document.getElementById("chat-box");

    const message =
        input.value;

    if (!message) return;

    addMessage(message, "user");

    input.value = "";

    const response =
        await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

    const data =
        await response.json();

    addMessage(
        data.response,
        "cloudy"
    );
}


function addMessage(text, sender) {

    const chatBox =
        document.getElementById("chat-box");

    const div =
        document.createElement("div");

    div.classList.add(
        "message",
        sender
    );

    div.innerText = text;

    chatBox.appendChild(div);

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


document
    .getElementById("user-input")
    .addEventListener(
        "keypress",
        function(e) {

            if (e.key === "Enter") {

                sendMessage();
            }
        }
    );


const starsContainer =
    document.getElementById("stars");

for (let i = 0; i < 150; i++) {

    const star =
        document.createElement("div");

    star.classList.add("star");

    star.style.left =
        Math.random() * 100 + "%";

    star.style.top =
        Math.random() * 100 + "%";

    star.style.animationDuration =
        2 + Math.random() * 5 + "s";

    star.style.opacity =
        Math.random();

    starsContainer.appendChild(star);
}
