import os
import subprocess
import requests
from flask import Flask, request, render_template_string
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
import time
import re

app = Flask(__name__)

# ✅ Start Tor automatically (no local Tor path needed)
USE_VPS_TOR = False  # ⚠️ False = Local Tor, True = VPS Tor Proxy
VPS_TOR_PROXY = "socks5h://your-vps-ip:9050"  # Update VPS Tor proxy if needed

# ✅ Start Tor (If using local)
def start_tor():
    if USE_VPS_TOR:
        print("🌍 Using VPS-based Tor proxy...")
        return
    try:
        subprocess.Popen(["tor"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(10)  # Wait for Tor to start
        print("✅ Tor started successfully!")
    except Exception as e:
        print(f"❌ Error starting Tor: {e}")

# ✅ Restart Tor (If using local)
def restart_tor():
    if USE_VPS_TOR:
        return
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
        print("🔄 Tor identity changed.")
    except Exception as e:
        print(f"❌ Failed to restart Tor: {e}")

# ✅ Connect to Tor (Local or VPS)
def connect_to_tor():
    session = requests.Session()
    tor_proxy = VPS_TOR_PROXY if USE_VPS_TOR else "socks5h://127.0.0.1:9050"
    session.proxies = {"http": tor_proxy, "https": tor_proxy}
    return session

# ✅ Extract valid .onion links
def extract_onion_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()

    for a_tag in soup.find_all('a', href=True):
        url = a_tag['href']
        if ".onion" in url and url.startswith("http"):
            links.add(url)

    # Regular expression to extract .onion links more reliably
    onion_pattern = re.compile(r"https?://[a-zA-Z0-9]+\.onion")
    raw_links = onion_pattern.findall(html)
    links.update(raw_links)

    return list(links)

# ✅ Search Dark Web
def perform_search(query):
    search_engines = [
        f"https://ahmia.fi/search/?q={query}",
        f"https://onionlandsearchengine.com/search?q={query}",
        f"http://msydqstlz2kzerdg.onion/search?q={query}",  # Ahmia (Tor)
        f"http://hss3uro2hsxfogfq.onion/search?q={query}",  # Not Evil (Tor)
        f"http://gram3rfapflvkwri.onion/search?q={query}"  # Torch (Tor)
    ]

    onion_links = set()
    session = connect_to_tor()

    for url in search_engines:
        try:
            print(f"🔍 Searching: {url}")
            response = session.get(url, timeout=15)
            if response.status_code == 200:
                new_links = extract_onion_links(response.text)
                onion_links.update(new_links)
                print(f"✅ Found {len(new_links)} links from {url}")
            else:
                print(f"⚠ Search failed: {url} (Status {response.status_code})")
        except Exception as e:
            print(f"❌ Error searching {url}: {e}")

    return list(onion_links)

# ✅ Flask Route for Search
@app.route("/", methods=["GET", "POST"])
def index():
    onion_links = []
    query = ""

    if request.method == "POST":
        query = request.form["query"]
        onion_links = perform_search(query)

    return render_template_string(HTML_TEMPLATE, query=query, onion_links=onion_links)

# ✅ Enhanced HTML with Copy Button and Updated Styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShadowNet - Dark Web Search Engines</title>
    <style>
        body {
            background-color: #1a1a1a;
            color: #00FF00;
            font-family: 'Courier New', Courier, monospace;
            text-align: center;
            padding: 20px;
        }

        h1 {
            font-size: 40px;
            margin-top: 20px;
        }

        input[type="text"] {
            background-color: #222;
            color: #00FF00;
            border: 2px solid #00FF00;
            padding: 12px;
            font-size: 18px;
            width: 50%;
            max-width: 400px;
            margin-top: 20px;
        }

        button {
            background-color: #222;
            color: #00FF00;
            border: 2px solid #00FF00;
            padding: 12px 24px;
            font-size: 18px;
            cursor: pointer;
            margin-top: 10px;
        }

        button:hover {
            background-color: #00FF00;
            color: #121212;
        }

        .results {
            text-align: left;
            max-width: 80%;
            margin: auto;
            margin-top: 20px;
            font-size: 14px;
            padding: 10px;
            background-color: #333;
            border-radius: 5px;
            box-shadow: 0 0 10px #00FF00;
            max-height: 400px;
            overflow-y: scroll;
        }

        .results a {
            color: #00FF00;
            text-decoration: none;
        }

        .results a:hover {
            color: #FF0000;
        }

        .copy-btn {
            margin-left: 10px;
            background-color: #222;
            color: #00FF00;
            border: 1px solid #00FF00;
            padding: 5px;
            font-size: 14px;
            cursor: pointer;
        }

        .copy-btn:hover {
            background-color: #00FF00;
            color: #121212;
        }

        footer {
            margin-top: 40px;
            color: #555;
            font-size: 12px;
        }

        footer a {
            color: #00FF00;
        }

        @media (max-width: 768px) {
            input[type="text"] {
                width: 80%;
            }

            .results {
                width: 90%;
            }
        }
    </style>
</head>
<body>
    <h1>ShadowNet</h1>
    <p>Search the Dark Web with the power of Tor</p>
    <form method="POST">
        <input type="text" name="query" placeholder="Search .onion sites" required>
        <button type="submit">Search</button>
    </form>

    {% if onion_links %}
        <h2>Results for "{{ query }}"</h2>
        <div class="results">
            {% for link in onion_links %}
                <div>
                    <a href="{{ link }}" target="_blank">{{ link }}</a>
                    <button class="copy-btn" onclick="copyToClipboard('{{ link }}')">Copy</button>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <p>No results found. Try another search.</p>
    {% endif %}

    <footer>
        <p>ShadowNet is a private service for exploring the Dark Web. All rights reserved.</p>
        <p><a href="#">About</a> | <a href="#">Privacy Policy</a></p>
    </footer>

    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert("Copied: " + text);
            }).catch(err => {
                console.error("Failed to copy: ", err);
            });
        }
    </script>
</body>
</html>
'''

# ✅ Start Tor & Run Flask App
if __name__ == "__main__":
    start_tor()
    app.run(debug=True, host="0.0.0.0", port=5000)
