const chatWindow = document.getElementById("chatWindow");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const resetBtn = document.getElementById("resetBtn");

function addMessage(text, role) {
  const wrapper = document.createElement("div");
  wrapper.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  wrapper.appendChild(bubble);
  chatWindow.appendChild(wrapper);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage(message) {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  return res.json();
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  addMessage(message, "user");
  messageInput.value = "";
  sendBtn.disabled = true;

  addMessage("Thinking...", "assistant");
  const thinkingBubble = chatWindow.lastChild;

  try {
    const data = await sendMessage(message);
    thinkingBubble.remove();

    if (data.error) {
      addMessage(data.error, "error");
    } else {
      addMessage(data.reply, "assistant");
    }
  } catch (err) {
    thinkingBubble.remove();
    addMessage("Network error: could not reach the server.", "error");
  } finally {
    sendBtn.disabled = false;
    messageInput.focus();
  }
});

resetBtn.addEventListener("click", async () => {
  await fetch("/api/reset", { method: "POST" });
  chatWindow.innerHTML = "";
  addMessage("New conversation started. How can I help?", "assistant");
});
