# import re

# # Original URL
# url = "//static-files.cricket-australia.pulselive.com/headshots/440/placeholder.png"

# # Replace 'placeholder.png' with 'camedia.png' using regex
# updated_url = re.sub(r'placeholder\.png$', '591-camedia.png', url)

# print(updated_url)


from bs4 import BeautifulSoup

# Sample HTML
html = '''
<h1 id="tab-title" class="w-player-header__player-name">
    Pat<span class="w-player-header__player-name--last">Cummins</span>
</h1>
'''

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Scrape the text "Pat"
# first_name = soup.find('h1', {'id': 'tab-title'}).contents[0].strip()


last_name = soup.find('h1').find('span').text
print(last_name)
