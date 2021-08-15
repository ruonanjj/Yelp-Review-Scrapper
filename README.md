<h1>Yelp review scraper</h1>
<p>A project that can be used to scraped review from yelp.com</p>
<h4>Installation</h4>
<ol>
<li>Python3 is required</li>
<li>Install Selenium Package: https://selenium-python.readthedocs.io/</li>
<li>Remember to setup web driver for <a href="https://chromedriver.chromium.org/downloads">Chrome</a> or <a href="https://github.com/mozilla/geckodriver/releases">Firefox</a>. depends on what browser you installed.</li>
</ol>

<h4>How to use</h4>
<p>Run python main.py, the program will start automatically, after it's done, three files will be outputted: </p>
<ul>
<li><b>reviews.text:</b> All comments in text.</li>
<li><b>reviews.cvs:</b> Review csv file separated into business_name, review text, and rating.</li>
<li><b>reviews_filtered.txt:</b> All review text filed the useless word in English.</li>
</ul>

<h4>Changed Search Key Term and Location</h4>
<li>Open main.py, change parameter values for scrape_yelp_comment(search_term, location).</li>