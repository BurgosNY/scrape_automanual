from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def initiate_browser(chromedriver_path=''):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=chromedriver_path)
    return driver


def selenium_scrape_page(chromedriver_path='', url=''):
    browser = initiate_browser(chromedriver_path)
    browser.get(url)
    soup = bs(browser.page_source, "html.parser")
    return soup


def decode_facebook(url, driver):
    soup = bs(driver.page_source, "html.parser")
    # Funciona se o IP estiver no Brasil:
    index = soup.text.find('curtiram')
    text = soup.text[index-20:index]
    # Sim, isso poderia ser feito com Regex. :)
    try:
        likes = int(''.join(i for i in text if i.isdigit()))
    # Se não achar likes, significa que não é uma página, mas um post
    except ValueError:
        return None

    verified = False
    if 'Figura pública' in soup.text:
        verified = True
    return {"facebook_url": url,
            "likes": likes,
            "verified": verified}


def decode_twitter(chromedriver_path, twitter_handle):
    url = f'https://twitter.com/{twitter_handle}'
    soup = selenium_scrape_page(chromedriver_path, url)
    verified = False
    if soup.find("span", {"class": "ProfileHeaderCard-badges"}):
        verified = True
    f = soup.find("li", {"class": "ProfileNav-item--followers"})
    # Se não achar número de seguidores, é pq isso é um status
    if not f:
        return None
    followers = int(''.join(i for i in f.a['title'] if i.isdigit()))
    f2 = soup.find("li", {"class": "ProfileNav-item--following"})
    following = int(''.join(i for i in f2.a['title'] if i.isdigit()))
    bio = soup.find("p", {"class": "ProfileHeaderCard-bio"}).text
    avatar = soup.find("img", {"class": "ProfileAvatar-image"})['src']
    return {"twitter_url": url,
            "twitter_handle": twitter_handle,
            "verified": verified,
            "followers": followers,
            "following": following,
            "bio": bio,
            "avatar": avatar}
