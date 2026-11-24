const API_URL = "http://127.0.0.1:8000";

async function loginUser() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const statusEl = document.getElementById("auth-status");

  // FastAPI's /auth/login expects form data (username & password)
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (response.ok) {
    localStorage.setItem("token", data.access_token);
    statusEl.innerText = "Logged in successfully!";
    statusEl.style.color = "green";
  } else {
    statusEl.innerText = data.detail || "Login failed";
    statusEl.style.color = "red";
  }
}
async function askAI() {
  const prompt = document.getElementById("prompt").value;
  const replyEl = document.getElementById("ai-reply");
  const token = localStorage.getItem("token");

  if (!token) {
    replyEl.innerText = "Please login first!";
    return;
  }

  replyEl.innerText = "Thinking...";

  const response = await fetch(`${API_URL}/ai/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    },
    body: JSON.stringify({ prompt: prompt }),
  });

  const data = await response.json();

  if (response.ok) {
    replyEl.innerText = data.response;
  } else {
    replyEl.innerText = data.detail || "Something went wrong";
  }
}
async function loadHistory() {
  const token = localStorage.getItem("token");
  const listEl = document.getElementById("history-list");

  const response = await fetch(`${API_URL}/ai/history`, {
    headers: { "Authorization": `Bearer ${token}` },
  });

  const records = await response.json();
  listEl.innerHTML = "";

  records.forEach((item) => {
    const li = document.createElement("li");
    li.innerText = `${item.prompt} → ${item.response.slice(0, 60)}...`;
    listEl.appendChild(li);
  });
}
