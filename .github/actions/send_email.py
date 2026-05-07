import sys
import json
import base64
import yagmail

def format_trending_email(data):
    html = "<h1>🔥 Tech Trending Daily</h1>"
    
    # GitHub Trending
    if 'githubTrending' in data:
        html += "<h2>📦 GitHub Trending</h2>"
        for lang, repos in data['githubTrending'].items():
            html += f"<h3>{lang.upper() if lang else 'All Languages'}</h3><ul>"
            for repo in repos[:5]:
                html += f'''<li>
                    <a href="https://github.com{repo['link']}">{repo['title']}</a>
                    ⭐ {repo['stars']} | {repo['todayStars']}
                    <br><small>{repo['description'][:100]}...</small>
                </li>'''
            html += "</ul>"
    
    # HuggingFace Models
    if data.get('huggingFaceModels'):
        html += "<h2>🤖 HuggingFace Trending Models</h2><ul>"
        for model in data['huggingFaceModels'][:5]:
            html += f'''<li>
                <a href="{model['link']}">{model['modelId']}</a>
                📥 {model['downloads']:,} | ❤️ {model['likes']}
            </li>'''
        html += "</ul>"
    
    # Hacker News
    if data.get('hackerNewsStories'):
        html += "<h2>📰 Hacker News Top Stories</h2><ul>"
        for story in data['hackerNewsStories'][:5]:
            html += f'''<li>
                <a href="{story['link']}">{story['title']}</a>
                🔺 {story['score']} points | 💬 {story['descendants']} comments
            </li>'''
        html += "</ul>"
    
    # AI Papers
    if data.get('aiPapers'):
        html += "<h2>📄 Latest AI Papers</h2><ul>"
        for paper in data['aiPapers'][:5]:
            authors = ', '.join(paper['authors'][:3])
            html += f'''<li>
                <a href="{paper['url']}">{paper['title']}</a>
                <br><small>👤 {authors}</small>
            </li>'''
        html += "</ul>"
    
    # Indie Hackers
    if data.get('indieHackerReports'):
        html += "<h2>💰 Indie Hackers Revenue</h2><ul>"
        for report in data['indieHackerReports'][:5]:
            html += f'''<li>
                <a href="{report['url']}">{report['productName']}</a>
                💵 ${report['mrr']:,.0f}/mo
            </li>'''
        html += "</ul>"
    
    return html

def main():
    username = sys.argv[1]
    password = sys.argv[2]
    to_email = sys.argv[3]
    subject = sys.argv[4]
    data_base64 = sys.argv[5]
    
    # Decode base64 data
    data = json.loads(base64.b64decode(data_base64).decode('utf-8'))
    
    # Format email content
    html_content = format_trending_email(data)
    
    # Send email
    yag = yagmail.SMTP(username, password)
    yag.send(to_email, subject, html_content)
    print("Email sent successfully!")

if __name__ == "__main__":
    main()
