from flask import Flask, render_template, request, jsonify
import logging
import os
import re
from dotenv import load_dotenv
from langdetect import detect, LangDetectException
from groq import Groq, APIConnectionError, RateLimitError, APIStatusError
import sqlite3

# Load .env file for GROQ_API_KEY
load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Feedback database path
FEEDBACK_DB = 'feedbacks.db'

# ✅ Initialize Groq Client
try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY not found in .env")
    client = Groq(api_key=groq_api_key)
except Exception as e:
    app.logger.error(f"GROQ Init Error: {e}")
    client = None

# ✅ Helpers to detect language mix
def contains_english(text):
    return bool(re.search(r'[a-zA-Z]', text))

def contains_tamil(text):
    return bool(re.search(r'[\u0B80-\u0BFF]', text))

# ✅ Get answer from Groq only
def get_groq_answer(text, lang):
    if client is None:
        return "API key issue. Check setup." if lang == 'en' else "API அமைப்புப் பிழை. தயவுசெய்து சரிபார்க்கவும்."

    prompt = f"Answer this in {('Tamil' if lang == 'ta' else 'English')} only: {text}"

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            max_tokens=250,
            temperature=0.7
        )

        answer = response.choices[0].message.content.strip()

        if not answer:
            return "Sorry, no answer available." if lang == 'en' else "மன்னிக்கவும்! பதில் இல்லை."

        # Language purity check
        try:
            detected = detect(answer)
            if lang == 'ta' and (detected not in ['ta', 'hi', 'ml'] or contains_english(answer)):
                return "மன்னிக்கவும்! பதில் தமிழில் மட்டும் இருக்க வேண்டும்."
            elif lang == 'en' and (detected != 'en' or contains_tamil(answer)):
                return "Sorry! The answer must be in English only."
        except LangDetectException:
            return "Couldn't detect language." if lang == 'en' else "மொழி கண்டறிய முடியவில்லை."

        return answer

    except RateLimitError:
        return "Too many requests. Try again later." if lang == 'en' else "அதிக கோரிக்கைகள். பின்னர் முயற்சிக்கவும்."
    except APIStatusError as e:
        if e.status_code == 401:
            return "Invalid API key." if lang == 'en' else "தவறான API திறவுக்கோல்."
        elif e.status_code >= 500:
            return "Server error." if lang == 'en' else "சேவையக பிழை."
        else:
            return "API error." if lang == 'en' else "API பிழை."
    except APIConnectionError:
        return "Connection error." if lang == 'en' else "இணைப்பு பிழை."
    except Exception as e:
        app.logger.error(f"Groq error: {e}")
        return "Unexpected error." if lang == 'en' else "எதிர்பாராத பிழை."

# ✅ Flask Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_reply', methods=['POST'])
def reply():
    data = request.get_json()
    text = data.get('text', '').strip()
    lang = data.get('lang', 'en')
    return jsonify({'reply': get_groq_answer(text, lang)})

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    text = data.get('text', '').strip()
    lang = data.get('lang', 'en')

    if text:
        try:
            conn = sqlite3.connect(FEEDBACK_DB)
            cur = conn.cursor()
            cur.execute("INSERT INTO feedback (text, lang) VALUES (?, ?)", (text, lang))
            conn.commit()
            conn.close()
            return jsonify({"status": "success"})
        except Exception as e:
            app.logger.error(f"Feedback DB Error: {e}")
            return jsonify({"status": "error"})
    return jsonify({"status": "empty"})

# ✅ Start App
if __name__ == '__main__':
    app.run(debug=True)
