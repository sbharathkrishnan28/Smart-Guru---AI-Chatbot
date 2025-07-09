import sqlite3

# Connect to your existing database
conn = sqlite3.connect('questions.db')
cur = conn.cursor()

# Make sure the table exists
cur.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_en TEXT,
    answer_en TEXT,
    question_ta TEXT,
    answer_ta TEXT
)
''')

# ✅ Your bilingual Q&A entries (English + Tamil)
entries = [
    ("What is an algorithm?", "A step-by-step procedure to solve a problem.",
     "அல்காரிதம் என்றால் என்ன?", "ஒரு சிக்கலை தீர்க்க படி படியாக அமைக்கப்பட்ட நடைமுறை."),

    ("What does CPU stand for?", "Central Processing Unit",
     "CPU என்றால் என்ன?", "மத்திய செயலாக்கக் கோப்பகம்"),

    ("What is phishing?", "A cyberattack where users are tricked into giving sensitive info.",
     "Phishing என்பது என்ன?", "பயனர்களை ஏமாற்றி தரவுகளைப் பெறும் இணையதள மோசடி."),

    ("What is an IP address?", "A unique identifier for devices on a network.",
     "IP முகவரி என்றால் என்ன?", "வலைப்பின்னலிலுள்ள சாதனங்களுக்கான தனிப்பட்ட அடையாள எண்."),

    ("What is a firewall?", "A security system that monitors and controls incoming/outgoing network traffic.",
     "Firewall என்பது என்ன?", "உள்நுழையும் மற்றும் வெளியேறும் வலைப்பின்னல் போக்குவரத்தை கட்டுப்படுத்தும் பாதுகாப்பு அமைப்பு."),

    ("Define machine learning.", "A method where systems learn from data without explicit programming.",
     "Machine Learning என்றால் என்ன?", "திட்டமிட்ட நிரலாக்கமின்றி தரவுகள் மூலமாக கணினி கற்றுக்கொள்ளும் முறை."),

    ("What is two-factor authentication?", "An extra layer of security requiring two forms of verification.",
     "இரட்டை சான்றளிப்பு என்றால் என்ன?", "இரண்டு நிலை அடையாளம் உறுதிப்படுத்தும் பாதுகாப்பு முறை."),

    ("What is encryption?", "The process of converting data into a secure format.",
     "மறையாக்கம் என்றால் என்ன?", "தரவுகளை பாதுகாப்பான வடிவமாக மாற்றும் செயல்முறை."),

    ("What is a Trojan horse in cybersecurity?", "A malicious software disguised as legitimate.",
     "Trojan horse என்பது என்ன?", "சாதாரண மென்பொருளைப் போலத் தோன்றும் தீய மென்பொருள்."),

    ("What is a DDoS attack?", "Distributed Denial-of-Service; overwhelms servers with traffic.",
     "DDoS தாக்குதல் என்றால் என்ன?", "சேவையகத்தை அதிக கோரிக்கைகளால் செயல் இழக்கும் தாக்குதல்."),

    ("Thank you", "You're welcome! ",
     "நன்றி", "வரவேற்கிறேன்! ")
]

# ✅ Insert each question multiple times to simulate your full set
for i in range(5):  # Repeat 5x = 50 entries
    for j, (q_en, a_en, q_ta, a_ta) in enumerate(entries):
        entry_no = i * len(entries) + j + 1
        q_en_tagged = f"{q_en} #{entry_no}"
        q_ta_tagged = f"{q_ta} #{entry_no}"
        cur.execute("""
            INSERT INTO questions (question_en, answer_en, question_ta, answer_ta)
            VALUES (?, ?, ?, ?)
        """, (q_en_tagged, a_en, q_ta_tagged, a_ta))

# Commit and close
conn.commit()
conn.close()

print("✅ Inserted 55 bilingual questions successfully.")
