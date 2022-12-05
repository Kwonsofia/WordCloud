import requests
from bs4 import BeautifulSoup
from collections import Counter
from datetime import datetime
from konlpy.tag import Twitter
from wordcloud import WordCloud
from config import NAVER_URL, NAVER_FILE_PATH, GOOGLE_URL, GOOGLE_FILE_PATH, FONT_PATH, WORDCLOUD_IMG_PATH, HEADER


def crawler(url, class_name):
    """
    Common Crawler Code
    """
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, "html.parser")
    hrefs = soup.find_all('a', attrs={'class':class_name})
    for href in hrefs:
        res = requests.get(href['href'], headers=HEADER)
        html = res.text
        soup = BeautifulSoup(html, "html.parser")
        texts = soup.find_all(['div', 'p', 'article'])
        for text in texts:
            body_list += text.get_text().strip()

    return body_list


def naver_crawler(word):
    """
    Naver News Crawler
    """
    result = ""
    for page in range(1, 21, 10):
        url = NAVER_URL + word + "&start=" + str(page)
        result += crawler(url, 'news_tit')

    with open(NAVER_FILE_PATH, 'w') as f:
        f.write(result)
    
    img_path = wordcloud(NAVER_FILE_PATH, "naver")
    return img_path
    

def google_crawler(word):
    """
    Google News Crawler
    """
    result = ""
    for page in range(0, 10, 10):
        url = GOOGLE_URL + word + "&start=" + str(page)
        result += crawler(url, 'WlydOe')

    with open(GOOGLE_FILE_PATH, 'w') as f:
        f.write(result)
    
    img_path = wordcloud(GOOGLE_FILE_PATH, "google")
    return img_path


def wordcloud(text_path, img):
    """
    Create Wordcloud Image
    """

    text = open(text_path).read() 
    twitter = Twitter()

    # twitter함수를 통해 읽어들인 내용의 형태소를 분석
    sentences_tag = []
    sentences_tag = twitter.pos(text) 
    noun_adj_list = []

    # tag가 명사이거나 형용사인 단어들만 noun_adj_list에 넣어준다.
    for word, tag in sentences_tag:
        if tag in ['Noun' , 'Adjective']: 
            noun_adj_list.append(word)

    # 가장 많이 나온 단어부터 n개를 저장한다.
    counts = Counter(noun_adj_list)
    tags = counts.most_common(100)

    # 한글을 분석하기위해 font를 한글로 지정
    wc = WordCloud(font_path=FONT_PATH, background_color="white", max_font_size=60)
    cloud = wc.generate_from_frequencies(dict(tags))  # google에서 영어만 있는 값을 전달하게 되면 tags에 어떤 값도 추가되지 않아 오류 발생

    url = f"{WORDCLOUD_IMG_PATH}{img}_{str(datetime.now().strftime('%y%m%d'))}.jpg"
    cloud.to_file(url)

    return url


if __name__ == '__main__':
    naver_crawler('hacking')
    google_crawler('해킹')
    wordcloud(NAVER_FILE_PATH, "naver")
    wordcloud(GOOGLE_FILE_PATH, "google")