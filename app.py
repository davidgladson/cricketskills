from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# Workshop data with consistent icon names
workshops = [
    {
        "title": "3 Day Cricket Content Workshop by DugOut",
        "icon": "users",  # Feather icon name
        "duration": "3 Days",
        "category": "Training",
        "spots": "Limited spots available",
        "is_active": True,
        "schedule": [
            "Day 1: Thursday 27th Feb 7 PM - 8 PM, Intro Session",
            "Day 2: Friday 28th Feb, Recorded Sessions & Short Contest Announcement",
            "Day 3: Saturday 1st Mar, 11 AM - 12:30 PM, Live Webinar"
        ],
        "whatsapp_link": "https://chat.whatsapp.com/BXxnlunDBoM3J8CHFVbzN4"
    },
    {
        "title": "3 Day Fantasy Cricket Workshop by Fantasy Experts",
        "icon": "award",  # Changed from trophy to award (available in Feather)
        "duration": "3 Days",
        "category": "Strategy",
        "spots": "Batch starting soon",
        "is_active": True,
        "features": [
            "Advanced fantasy strategies",
            "Live analysis sessions",
            "Exclusive team selections",
            "Tournament-specific insights"
        ],
        "whatsapp_link": "https://chat.whatsapp.com/HSg8Vya3kn226xHlJ1BoAK"
    },
    {
        "title": "BCCI Cricket Umpiring Certification",
        "icon": "book",  # Changed from book-open to book
        "duration": "90 mins",
        "category": "Certification",
        "spots": "Coming Soon",
        "is_active": False
    },
    {
        "title": "Cricket Commentary Workshop",
        "icon": "mic",  # This one was correct
        "duration": "90 mins",
        "category": "Media",
        "spots": "Coming Soon",
        "is_active": False
    },
    {
        "title": "Sports Photography Excellence",
        "icon": "camera",  # This one was correct
        "duration": "90 mins",
        "category": "Media",
        "spots": "Coming Soon",
        "is_active": False
    }
]

@app.route('/')
def home():
    current_year = datetime.now().year
    return render_template('index.html', workshops=workshops, current_year=current_year)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)