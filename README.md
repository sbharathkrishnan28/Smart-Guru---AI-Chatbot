# 🤖 Smart Guru – AI Chatbot

Smart Guru is a bilingual, voice-enabled AI chatbot designed to work both online and offline using lightweight AI models. It helps users in rural and semi-urban areas get intelligent, real-time responses to their questions — even without internet access.

## 🚀 Features

- 🗣️ Bilingual Support (English + Regional Languages)
- 🎤 Voice Input and Output (Web Speech API / Whisper)
- 🔌 Offline Capability with Ollama and local LLMs
- ⚡ Real-Time Q&A with context-aware AI
- 🌐 Lightweight Flask + JavaScript Web Interface
- 🌍 Language Detection using LangDetect

---

## 🧱 Tech Stack

- **Frontend**: HTML, CSS, JavaScript (Fetch API + Web Speech API)
- **Backend**: Python (Flask, LangDetect, dotenv)
- **AI Models**: OpenAI API (online) OR Ollama + LLaMA2 (offline)
- **Voice**: Whisper (offline) / Web Speech API (online browsers)

---

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/smart-guru.git
   cd smart-guru
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **(Optional) Add OpenAI API Key**
   Create a `.env` file:
   ```
   OPENAI_API_KEY=your_key_here
   ```

---

## 🚀 Run the App

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🧠 Using Offline AI (Ollama)

1. **Install Ollama**: https://ollama.com
2. **Run a local model**:
   ```bash
   ollama run llama2
   ```
3. Smart Guru will connect via API at `http://localhost:11434`.

---

## 🎤 Voice Support

- Enable microphone access in your browser.
- Use speech-to-text and text-to-speech directly via browser or Whisper (if offline).

---

## 📌 Use Cases

- Rural education assistant  
- Offline village helpdesk  
- Voice assistant for elderly or differently abled  
- General chatbot for schools, kiosks, or libraries

---

## 🙌 Contributing

Pull requests welcome! For major changes, please open an issue first to discuss.

---

## 📄 License

[MIT License](LICENSE)
