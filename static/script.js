const log = document.getElementById('log');
const form = document.getElementById('composerForm');
const input = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');

function scrollToBottom() {
  log.scrollTop = log.scrollHeight;
}

function addMessage(role, text) {
  const row = document.createElement('div');
  row.className = `row ${role}`;
  const note = document.createElement('div');
  note.className = 'note';
  const p = document.createElement('p');
  p.textContent = text;
  note.appendChild(p);
  row.appendChild(note);
  log.appendChild(row);
  scrollToBottom();
}

function showTyping() {
  const row = document.createElement('div');
  row.className = 'row bot typing';
  row.id = 'typingRow';
  row.innerHTML = `<div class="note"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>`;
  log.appendChild(row);
  scrollToBottom();
}

function removeTyping() {
  const row = document.getElementById('typingRow');
  if (row) row.remove();
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  addMessage('user', message);
  input.value = '';
  sendBtn.disabled = true;
  showTyping();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    removeTyping();

    if (!res.ok || data.error) {
      addMessage('error', data.error || 'Something went wrong.');
    } else {
      addMessage('bot', data.reply);
    }
  } catch (err) {
    removeTyping();
    addMessage('error', 'Could not reach the server. Is it running?');
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
});

resetBtn.addEventListener('click', async () => {
  try {
    await fetch('/api/reset', { method: 'POST' });
  } catch (err) {
    // ignore network errors on reset, still clear the visible log
  }
  log.innerHTML = `
    <div class="row bot">
      <div class="note"><p>Hi — I'm your AI assistant. Ask me anything.</p></div>
    </div>`;
  input.focus();
});

input.focus();
