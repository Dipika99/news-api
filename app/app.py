# import libraries
from flask import Flask, render_template, request
from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

# init flask app
app = Flask(__name__)

# Init news api 
load_dotenv()
newsapi = NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))

# format the content
def get_sources_and_domains():
    all_sources = newsapi.get_sources()['sources']
    sources = domains = []

    for source in all_sources:
        id = source['id']
        domain = source['url'].replace("http://", "")
        domain = domain.replace("https://", "")
        domain = domain.replace("www.", "")
        slash = domain.find('/')

        if slash != -1:
            domain = domain[:slash]
        sources.append(id)
        domains.append(domain)

    sources = ", ".join(sources)
    domains = ", ".join(domains)
    return sources, domains

def get_articles(keyword = None, sources = None, domains = None, country = None, language = 'en', sort_by = 'relevency', max_result = 10):

    if keyword:
        response = newsapi.get_everything(
            q=keyword,
            sources=sources,
            domains=domains,
            language=language,
            sort_by=sort_by)
    elif country:
        response = newsapi.get_top_headlines(
            country=country,
            language=language)
    else:
        return []

    total_results = min(response.get('totalResults', 0), max_result)
    articles = response.get('articles', [])[:total_results]

    return articles

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        keyword = request.form.get("keyword", "")
        sources, domains = get_sources_and_domains()  # Assumes this function exists and is implemented.

        all_articles = get_articles(
            keyword=keyword,
            sources=sources,
            domains=domains
        )

        return render_template("home.html", all_articles=all_articles, keyword=keyword)

    else:
        all_headlines = get_articles(country="us")

        return render_template("home.html", all_headlines=all_headlines)

if __name__ == "__main__":
    app.run(debug = True)

