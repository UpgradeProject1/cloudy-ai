const input = document.getElementById("user-input");

let currentChatId = null;


/* =========================
   DAY / NIGHT SYSTEM
========================= */

function updateSkyMode() {

    const hour = new Date().getHours();

    document.body.classList.remove(
        "day-mode",
        "sunset-mode",
        "night-mode"
    );

    if (hour >= 7 && hour < 18) {

        document.body.classList.add("day-mode");

    } else if (hour >= 18 && hour < 21) {

        document.body.classList.add("sunset-mode");

    } else {

        document.body.classList.add("night-mode");
    }
}

updateSkyMode();


/* =========================
   LOAD FIRST CLOUD
========================= */

window.onload = async function() {

    updateSkyMode();

    const firstConversation =
        document.querySelector(".conversation-item");

    if (firstConversation) {

        firstConversation.classList.add("active-cloud");

        const onclickValue =
            firstConversation
            .querySelector("span")
            .getAttribute("onclick");

        const chatId =
            onclickValue.match(/'([^']+)'/)[1];

        await loadChat(chatId);
    }
};


/* =========================
   ENTER KEY
========================= */

input.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {

        sendMessage();
    }
});


/* =========================
   FORMAT LINKS
========================= */

function formatResponse(text) {

    text = text.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank">$1</a>'
    );

    text = text.replace(/\n/g, "<br>");

    return text;
}


/* =========================
   TIME
========================= */

function getTime() {

    const now = new Date();

    return now.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit'
    });
}


/* =========================
   CREATE CLOUD
========================= */

async function createChat() {

    const response = await fetch("/new_chat");

    const data = await response.json();

    currentChatId = data.chat_id;

    location.reload();
}


/* =========================
   LOAD CLOUD
========================= */

async function loadChat(chatId) {

    currentChatId = chatId;

    document
        .querySelectorAll(".conversation-item")
        .forEach(cloud => {

            cloud.classList.remove("active-cloud");
        });

    const cloudElements =
        document.querySelectorAll(".conversation-item");

    cloudElements.forEach(cloud => {

        if (
            cloud.innerHTML.includes(chatId)
        ) {

            cloud.classList.add("active-cloud");
        }
    });

    const response =
        await fetch(`/load_chat/${chatId}`);

    const history = await response.json();

    const chatBox =
        document.getElementById("chat-box");

    chatBox.innerHTML = "";

    history.forEach(chat => {

        chatBox.innerHTML += `
            <div class="user-message">

                <div class="message-header">
                    <b>Toi</b>
                </div>

                <div>
                    ${chat.user}
                </div>

            </div>

            <div class="bot-message">

                <div class="message-header">
                    <b>Cloudy</b>
                </div>

                <div>
                    ${formatResponse(chat.nova)}
                </div>

            </div>
        `;
    });

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


/* =========================
   SEND MESSAGE
========================= */

async function sendMessage() {

    if (!currentChatId) {

        alert("Aucun cloud sélectionné ☁️");

        return;
    }

    const chatBox =
        document.getElementById("chat-box");

    const message = input.value;

    if (!message) return;

    document.body.classList.add("storm-mode");

    chatBox.innerHTML += `
        <div class="user-message">

            <div class="message-header">
                <b>Toi</b>
                <span>${getTime()}</span>
            </div>

            <div>
                ${message}
            </div>

        </div>
    `;

    input.value = "";

    const botId = "bot-" + Date.now();

    chatBox.innerHTML += `
        <div class="bot-message" id="${botId}">

            <div class="message-header">
                <b>Cloudy</b>
                <span>${getTime()}</span>
            </div>

            <div class="bot-text">
                🌩️ Cloudy réfléchit...
            </div>

        </div>
    `;

    chatBox.scrollTop =
        chatBox.scrollHeight;

    const response = await fetch("/chat", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message,
            chat_id: currentChatId
        })

    });

    const reader = response.body.getReader();

    const decoder = new TextDecoder();

    let fullText = "";

    while (true) {

        const { done, value } =
            await reader.read();

        if (done) break;

        const chunk =
            decoder.decode(value);

        fullText += chunk;

        document.querySelector(
            `#${botId} .bot-text`
        ).innerHTML =
            formatResponse(fullText);

        chatBox.scrollTop =
            chatBox.scrollHeight;
    }

    document.body.classList.remove("storm-mode");
}


/* =========================
   DELETE CLOUD
========================= */

async function deleteChat(chatId) {

    await fetch(`/delete_chat/${chatId}`);

    location.reload();
}
