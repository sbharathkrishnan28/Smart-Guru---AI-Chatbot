let historyList = [];

async function getReply() {
  const question = document.getElementById('question').value.trim();
  const lang = document.getElementById('lang').value;
  const answerBox = document.getElementById('answer');

  if (!question) {
    answerBox.textContent = lang === 'ta'
      ? "📢 தயவுசெய்து கேள்வியை உள்ளிடவும்."
      : "🧠 Please enter a question.";
    return;
  }

  answerBox.textContent = lang === 'ta' ? "🤖 பதில் எழுதப்படுகிறது..." : "🤖 Typing...";

  try {
    const response = await fetch('/get_reply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: question, lang: lang })
    });

    const data = await response.json();
    const answer = data.reply;

    setTimeout(() => {
      answerBox.textContent = (lang === 'ta' ? "📢 பதில்: " : "🧠 Answer: ") + answer;

      speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(answer);
      utter.lang = lang === 'ta' ? 'ta-IN' : 'en-US';
      speechSynthesis.speak(utter);

      updateHistory(question);
    }, 1000);

  } catch (error) {
    console.error("❌ Error getting reply:", error);
    answerBox.textContent = lang === 'ta'
      ? "மன்னிக்கவும், பதிலை பெற முடியவில்லை."
      : "Sorry, I couldn't get the answer.";
  }
}

function updateHistory(q) {
  historyList.push(q);
  const historyUl = document.getElementById("historyList");
  const li = document.createElement("li");
  li.textContent = q;
  li.onclick = () => {
    document.getElementById("question").value = q;
    getReply();
  };
  historyUl.prepend(li);
}

function clearHistory() {
  historyList = [];
  document.getElementById("historyList").innerHTML = "";
}

document.getElementById("searchBox").addEventListener("input", function () {
  const query = this.value.toLowerCase();
  const filtered = historyList.filter(q => q.toLowerCase().includes(query));

  const historyUl = document.getElementById("historyList");
  historyUl.innerHTML = "";
  filtered.forEach(q => {
    const li = document.createElement("li");
    li.textContent = q;
    li.onclick = () => {
      document.getElementById("question").value = q;
      getReply();
    };
    historyUl.appendChild(li);
  });
});

async function sendFeedback() {
  const feedback = document.getElementById("feedback").value.trim();
  const lang = document.getElementById("lang").value;

  if (!feedback) return;

  try {
    const res = await fetch('/submit_feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: feedback, lang: lang })
    });

    const result = await res.json();
    if (result.status === 'success') {
      alert(lang === 'ta' ? "உங்கள் கருத்து பதிவு செய்யப்பட்டது!" : "✅ Thank you for your feedback!");
      document.getElementById("feedback").value = '';
    }
  } catch (error) {
    console.error("❌ Error submitting feedback:", error);
  }
}

function startVoice() {
  const lang = document.getElementById('lang').value;

  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    alert(lang === 'ta'
      ? "உங்கள் உலாவி குரல் உள்ளீட்டை ஆதரிக்கவில்லை."
      : "Your browser does not support speech recognition.");
    return;
  }

  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = lang === 'ta' ? 'ta-IN' : 'en-US';
  recognition.interimResults = false;

  recognition.start();

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById('question').value = transcript;
    getReply();
    sendFeedback();
  };
}

function clearFields() {
  document.getElementById('question').value = '';
  const lang = document.getElementById('lang').value;
  document.getElementById('answer').textContent = lang === 'ta'
    ? "🤖 நான் உங்களுக்கு உதவ தயாராக இருக்கிறேன்!"
    : "🤖 I’m ready to help you!";
  document.getElementById('feedback').value = '';
}

document.getElementById("feedback").addEventListener("keydown", function (event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendFeedback();
  }
});
