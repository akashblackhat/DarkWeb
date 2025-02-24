# ShadowNet - Dark Web Search Tool

  ![Screenshot_2025-02-22_07-53-00](https://github.com/user-attachments/assets/6ac9855f-ba83-4e85-b48a-e3504f278bcf)

  A powerful tool to search the dark web using Tor. ShadowNet allows you to search .onion websites with the help of various search engines, all while keeping your identity private and secure. Built with Python, 
  Flask, and Tor for an anonymous search experience.


  # Features
   🌐 Search Dark Web (.onion) sites using Tor for anonymity.
   
   🔍 Multiple search engines for efficient results.
   
   💻 Flask-based web interface to enter queries and view results.
   
   📋 Copy button for easy copying of .onion links.
   
   🔄 Restart Tor connection for fresh IPs.
   
   🎨 Custom dark-themed interface.
# Installation
   Clone this repository
   First, clone the repository to your local machine
   

       git clone https://github.com/akashblackhat/ShadowNet.git
   
       cd ShadowNet
   # 2. Install Dependencies
   ShadowNet requires Python and a few dependencies. You can install them using pip.
        pip install -r requirements.txt
   The required libraries include:

    Flask for the web framework.
    requests for HTTP requests to search engines.
    stem for Tor control (starting/restarting Tor).
    beautifulsoup4 for HTML parsing.
    re for regular expression processing.
   # 3. Tor 🧅 Installation
   Local Installation (Recommended):   
   You need to have Tor installed locally for ShadowNet to function properly.
         sudo apt install tor
# Start🧅 Tor on your local machine:
         tor
# Usage
Run the Application:
After installation and setting up 🧅Tor, you can run the app with:
       python darkweb.py
# Search for .onion Sites:
Open your browser and go to http://localhost:5000. Enter your query in the search bar, and ShadowNet will find relevant .onion links.

# Copy Links:
You can easily copy any .onion link by clicking the "Copy" button next to the result.

# Troubleshooting

🧅Tor Not Starting: Ensure that you have Tor installed and running on your local machine. If you're using a VPS-based proxy, make sure the proxy address is correct.

No Results Found: Try different search queries or check if Tor is properly connected. If needed, restart 🧅Tor using the restart option in the app.

# Security Warning
Please be cautious when browsing the dark web. Avoid interacting with suspicious or illegal sites. ShadowNet is provided for educational purposes only. Your safety and privacy are your responsibility.

# Contributing
Feel free to contribute to the project! You can help by:

Submitting bug reports or feature requests.

Improving the code.

Enhancing the documentation. 
