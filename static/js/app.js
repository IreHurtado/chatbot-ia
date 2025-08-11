const form = document.getElementById("form");
const input = document.getElementById("input");
const chat = document.getElementById("chat");
const typing = document.getElementById("typing");
const sendBtn = document.getElementById("send");
const usageEl = document.getElementById("usage");
const resetBtn = document.getElementById("reset");

function addMessage(role, content) {
  const wrap = document.createElement("div");
  wrap.className = `msg ${role}`;
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = content;
  wrap.appendChild(bubble);
  chat.appendChild(wrap);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";
  sendBtn.disabled = true;
  typing.classList.remove("hidden");

  try {
    const res = await fetch("/api/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector('input[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Error en la API");

    addMessage("assistant", data.reply || "(respuesta vacía)");

    if (data.usage) {
      const { prompt_tokens, completion_tokens, total_tokens } = data.usage;
      usageEl.textContent = `Tokens — entrada: ${prompt_tokens ?? "–"}, salida: ${completion_tokens ?? "–"}, total: ${total_tokens ?? "–"}`;
    }
  } catch (err) {
    addMessage("assistant", `⚠️ Error: ${err.message}`);
  } finally {
    typing.classList.add("hidden");
    sendBtn.disabled = false;
  }
});

resetBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("/api/reset/", {
      method: "POST",
      headers: { "X-CSRFToken": document.querySelector('input[name=csrfmiddlewaretoken]').value }
    });
    await res.json();
    location.reload();
  } catch (e) {
    console.error(e);
  }
});
