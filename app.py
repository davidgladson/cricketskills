import feedparser
import time
import re
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://davidgladsonin:bt2kzPEugHRTa1q6@predictions.otwe6.mongodb.net/cricket"
mongo = PyMongo(app)

# Workshop data with consistent icon names
workshops = [
    {
        "title": "BCCI Video Analyst Workshop",
        "icon": "book",  
        "duration": "2 Days",
        "category": "Certification",
        "spots": "Last 09 slots remaining",
        "is_active": True,
        "schedule": [
            "Day 1: Introductory Session",
            "Day 2: Live Webinar with BCCI Video Analyst",
            "Certificate: Yes! workshop completion certificate will be provided."
        ],
        "whatsapp_link": "https://pages.razorpay.com/video-analyst#view-1"
    },
    {
        "title": "3 Day Cricket Content Workshop by DugOut",
        "icon": "users",  # Feather icon name
        "duration": "3 Days",
        "category": "Training",
        "spots": "Batch Full - Registration Closed",
        "is_active": False,
        "schedule": [
            "Day 1: Thursday 27th Feb 7 PM - 8 PM, Intro Session",
            "Day 2: Friday 28th Feb, Recorded Sessions & Short Contest Announcement",
            "Day 3: Saturday 1st Mar, 11 AM - 12:30 PM, Live Webinar"
        ],
        "whatsapp_link": "https://chat.whatsapp.com/BXxnlunDBoM3J8CHFVbzN4"
    },
    # {
    #     "title": "3 Day Fantasy Cricket Workshop by Fantasy Experts",
    #     "icon": "award",  # Changed from trophy to award (available in Feather)
    #     "duration": "3 Days",
    #     "category": "Strategy",
    #     "spots": "Batch starting soon",
    #     "is_active": True,
    #     "features": [
    #         "Advanced fantasy strategies",
    #         "Live analysis sessions",
    #         "Exclusive team selections",
    #         "Tournament-specific insights"
    #     ],
    #     "whatsapp_link": "https://www.cricketskills.in/fantasy-workshop"
    # },
    {
        "title": "BCCI Cricket Umpiring Certification",
        "icon": "book",  # Changed from book-open to book
        "duration": "90 mins",
        "category": "Certification",
        "spots": "Coming Soon",
        "is_active": False
    },
    {
        "title": "BCCI Level 1 Coaching Certification",
        "icon": "users",  # Changed from book-open to book
        "duration": "90 mins",
        "category": "Certification",
        "spots": "Coming Soon",
        "is_active": False
    },
    {
        "title": "Strength & Conditioning Workshop by NCA",
        "icon": "book",  # Changed from activity to dumbbell
        "duration": "90 mins",
        "category": "Training",
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
    },
    {
        "title": "Sports Psychology Workshop",
        "icon": "users",  # This one was correct
        "duration": "90 mins",
        "category": "Strategy",
        "spots": "Coming Soon",
        "is_active": False
    }
]

# Sample blog data with multiple sources
blogs = [
    {
        "medium_url": "https://crickomaniablog.wordpress.com/2025/02/23/how-did-kohlis-masterclass-propel-india-to-a-commanding-victory-over-pakistan/",
        "title": "How Did Kohli's Masterclass Propel India to a Commanding Victory Over Pakistan?",
        "author": "Abhisek Gupta",
        "slug": "kohlis-masterclass-propel-india-to-victory-over-pakistan",
        "views": 0,
        "image_url": "",  # Will be populated
        "description": "An analysis of Virat Kohli's exceptional innings that led India to victory against Pakistan.",
        "published_date": datetime.strptime("2025-02-23", "%Y-%m-%d"),
        "source": "wordpress"
    },
    {
        "medium_url": "https://medium.com/@gladson47/100-python-pandas-commands-for-eda-tips-tricks-c63a9949bc6b",
        "title": "100 Python Pandas Commands for EDA: Tips & Tricks",
        "author": "Gladson Dsouza",
        "slug": "100-python-pandas-commands-for-eda",
        "views": 0,
        "image_url": "",  # Will be populated from Medium
        "description": "",  # Will be populated from Medium
        "published_date": datetime.now(),
        "source": "medium"
    },
    {
        "medium_url": "https://medium.com/@gladson47/100-python-matplotlib-commands-for-eda-tips-tricks-6c22939d8017",
        "title": "100 Python Matplotlib Commands for EDA: Tips & Tricks",
        "author": "Gladson Dsouza",
        "slug": "100-python-matplotlib-commands-for-eda",
        "views": 0,
        "image_url": "",  # Will be populated from Medium
        "description": "",  # Will be populated from Medium
        "published_date": datetime.now(),
        "source": "medium"
    }
]

# Function to manually add an external blog
def add_external_blog(url, title, author, description, date_str, source_name="external"):
    """
    Manually add an external blog to the database
    
    Args:
        url: The URL to the external blog post
        title: The title of the blog post
        author: The author's name
        description: A short description/excerpt
        date_str: Date string in format "YYYY-MM-DD"
        source_name: Name of the source (e.g., "wordpress", "substack", etc.)
    
    Returns:
        The inserted blog document ID
    """
    # Create slug from title
    slug = title.lower().replace(" ", "-")
    slug = re.sub(r'[^\w\-]', '', slug)
    
    # Try to fetch image and additional info
    image_url = ""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_img = soup.find('meta', property='og:image')
            if meta_img:
                image_url = meta_img['content']
    except Exception as e:
        print(f"Error fetching image from {url}: {e}")
    
    # Create blog document
    new_blog = {
        "medium_url": url,  # we keep the same field name for consistency
        "title": title,
        "author": author,
        "slug": slug,
        "views": 0,
        "image_url": image_url,
        "description": description,
        "published_date": datetime.strptime(date_str, "%Y-%m-%d"),
        "source": source_name
    }
    
    # Insert into database
    result = mongo.db.blogs.insert_one(new_blog)
    return result.inserted_id

# Function to add the WordPress article about Kohli
def add_wordpress_kohli_article():
    """Add the specific WordPress article about Kohli to the database"""
    url = "https://crickomaniablog.wordpress.com/2025/02/23/how-did-kohlis-masterclass-propel-india-to-a-commanding-victory-over-pakistan/"
    title = "How Did Kohli's Masterclass Propel India to a Commanding Victory Over Pakistan?"
    author = "Abhisek Gupta"
    description = "An analysis of Virat Kohli's exceptional innings that led India to victory against Pakistan."
    date_str = "2025-02-23"
    
    # Check if this blog already exists
    existing = mongo.db.blogs.find_one({"medium_url": url})
    if not existing:
        add_external_blog(url, title, author, description, date_str, "wordpress")
        print("Added WordPress article about Kohli's masterclass")
    else:
        print("WordPress article about Kohli already exists in database")

# Enhanced function to handle multiple sources
def initialize_blogs():
    # Check if blogs collection exists and has entries
    if mongo.db.blogs.count_documents({}) == 0:
        # Insert sample blogs
        for blog in blogs:
            # Fetch additional data based on source
            try:
                response = requests.get(blog["medium_url"])
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract meta description if not already provided
                    if not blog["description"]:
                        meta_desc = soup.find('meta', property='og:description')
                        if meta_desc:
                            blog["description"] = meta_desc['content']
                    
                    # Extract featured image if not already provided
                    if not blog["image_url"]:
                        meta_img = soup.find('meta', property='og:image')
                        if meta_img:
                            blog["image_url"] = meta_img['content']
                        
            except Exception as e:
                print(f"Error fetching blog data: {e}")
                
            mongo.db.blogs.insert_one(blog)
        print("Blog collection initialized with multiple sources")

# Function to fetch WordPress blog posts
def fetch_wordpress_posts(site_url="https://crickomaniablog.wordpress.com", max_posts=5):
    feed_url = f"{site_url}/feed/"
    try:
        feed = feedparser.parse(feed_url)
        posts = []
        
        for entry in feed.entries[:max_posts]:
            # Extract first image from content if available
            content = entry.content[0].value if 'content' in entry else entry.summary
            soup = BeautifulSoup(content, 'html.parser')
            img_tag = soup.find('img')
            image_url = img_tag['src'] if img_tag else ""
            
            # Create summary by stripping HTML and truncating
            text_content = re.sub('<.*?>', '', content)
            summary = text_content[:200] + "..." if len(text_content) > 200 else text_content
            
            post = {
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "image_url": image_url,
                "summary": summary,
                "author": entry.author if 'author' in entry else "Crickomaniac"
            }
            posts.append(post)
        return posts
    except Exception as e:
        print(f"Error fetching WordPress RSS feed: {e}")
        return []

# Function to get blogs from Medium RSS feed
def fetch_medium_posts(username="@gladson47", max_posts=10):
    feed_url = f"https://medium.com/feed/{username}"
    try:
        feed = feedparser.parse(feed_url)
        posts = []
        
        for entry in feed.entries[:max_posts]:
            # Extract first image from content if available
            content = entry.content[0].value
            soup = BeautifulSoup(content, 'html.parser')
            img_tag = soup.find('img')
            image_url = img_tag['src'] if img_tag else ""
            
            # Create summary by stripping HTML and truncating
            text_content = re.sub('<.*?>', '', content)
            summary = text_content[:200] + "..." if len(text_content) > 200 else text_content
            
            post = {
                "title": entry.title,
                "link": entry.link,
                "published": entry.published,
                "image_url": image_url,
                "summary": summary,
                "author": entry.author
            }
            posts.append(post)
        return posts
    except Exception as e:
        print(f"Error fetching Medium RSS feed: {e}")
        return []

# Function to initialize app (called explicitly)
def initialize_app():
    initialize_blogs()

# Create a separate route for initialization that can be called manually
@app.route('/admin/initialize')
def admin_initialize():
    initialize_blogs()
    return "Blog database initialized successfully!"

# Enhanced route to update blogs from multiple sources
@app.route('/admin/update-blogs')
def update_blogs_from_sources():
    # This would typically be password protected
    
    # Fetch from Medium
    medium_posts = fetch_medium_posts()
    
    for post in medium_posts:
        # Check if blog already exists by URL
        existing = mongo.db.blogs.find_one({"medium_url": post["link"]})
        if not existing:
            # Create a slug from title
            slug = post["title"].lower().replace(" ", "-")
            slug = re.sub(r'[^\w\-]', '', slug)
            
            new_blog = {
                "medium_url": post["link"],
                "title": post["title"],
                "author": post["author"],
                "slug": slug,
                "views": 0,
                "image_url": post["image_url"],
                "description": post["summary"],
                "published_date": datetime.strptime(post["published"], "%a, %d %b %Y %H:%M:%S %z"),
                "source": "medium"
            }
            mongo.db.blogs.insert_one(new_blog)
    
    # Fetch from WordPress
    wordpress_posts = fetch_wordpress_posts()
    
    for post in wordpress_posts:
        # Check if blog already exists by URL
        existing = mongo.db.blogs.find_one({"medium_url": post["link"]})
        if not existing:
            # Create a slug from title
            slug = post["title"].lower().replace(" ", "-")
            slug = re.sub(r'[^\w\-]', '', slug)
            
            new_blog = {
                "medium_url": post["link"],
                "title": post["title"],
                "author": post["author"],
                "slug": slug,
                "views": 0,
                "image_url": post["image_url"],
                "description": post["summary"],
                "published_date": datetime.strptime(post["published"], "%a, %d %b %Y %H:%M:%S %z"),
                "source": "wordpress"
            }
            mongo.db.blogs.insert_one(new_blog)
    
    return redirect(url_for('blog_list'))

# Route for manual blog entry
@app.route('/admin/add-blog', methods=['GET', 'POST'])
def admin_add_blog():
    # This would typically be password protected
    if request.method == 'POST':
        url = request.form.get('url')
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        date_str = request.form.get('published_date')
        source = request.form.get('source', 'external')
        
        add_external_blog(url, title, author, description, date_str, source)
        return redirect(url_for('blog_list'))
    
    return render_template('add_blog.html', current_year=datetime.now().year)

# Call initialize on startup
with app.app_context():
    try:
        initialize_app()
        add_wordpress_kohli_article()  # Add WordPress article
        print("Blog collection initialized on startup")
    except Exception as e:
        print(f"Error during initialization: {e}")

# Routes for other pages
@app.route('/careers')
def careers():
    current_year = datetime.now().year
    return render_template('careers.html', current_year=current_year)

@app.route('/community')
def community():
    current_year = datetime.now().year
    return render_template('community.html', current_year=current_year)

@app.route('/privacy')
def privacy():
    current_year = datetime.now().year
    return render_template('privacy.html', current_year=current_year)

@app.route('/terms')
def terms():
    current_year = datetime.now().year
    return render_template('terms.html', current_year=current_year)

@app.route('/refund')
def refund():
    current_year = datetime.now().year
    return render_template('refund.html', current_year=current_year)

@app.route('/about')
def about():
    current_year = datetime.now().year
    return render_template('about.html', current_year=current_year)

@app.route('/fantasy-workshop')
def fantasy_workshop():
    """
    Route for the Fantasy Cricket Workshop page.
    """
    current_year = datetime.now().year
    
    # Get the Fantasy Workshop details from your workshops list
    fantasy_workshop = None
    for workshop in workshops:
        if workshop["title"] == "3 Day Fantasy Cricket Workshop by Fantasy Experts":
            fantasy_workshop = workshop
            break
    
    return render_template('fantasy_workshop.html', workshop=fantasy_workshop, current_year=current_year)

# Update the blog_list route to sort by publication date in descending order
@app.route('/blog')
def blog_list():
    current_year = datetime.now().year
    blogs = list(mongo.db.blogs.find().sort('published_date', -1))  # Sort by date, newest first
    return render_template('blog_list.html', blogs=blogs, current_year=current_year)

# Individual blog view route
@app.route('/blog/<slug>')
def blog_detail(slug):
    current_year = datetime.now().year
    # Find the blog by slug
    blog = mongo.db.blogs.find_one({"slug": slug})
    
    if blog:
        # Increment the view count
        mongo.db.blogs.update_one(
            {"_id": blog["_id"]},
            {"$inc": {"views": 1}}
        )
        
        # Redirect to the Medium article
        return redirect(blog["medium_url"])
    else:
        # If blog not found, redirect to blog list
        return redirect(url_for('blog_list'))

# Home route
@app.route('/')
def home():
    current_year = datetime.now().year
    
    # Get recent blog posts
    blogs = list(mongo.db.blogs.find().sort('published_date', 1).limit(6))
    
    return render_template('index.html', workshops=workshops, blogs=blogs, current_year=current_year)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)