from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

date = (input("날짜 입력 : ")) #YYYYMMDD 형태
file = open(os.path.join(os.path.expanduser('~'),'Desktop\\')+'daum_comments.txt', 'w',encoding='UTF-8')  #저장할 파일 열기 (바탕화면)
results = []
cnt = 0         # 시작 페이지
#수정필요. 마지막 페이지를 자동으로 파악할 수 있어야 함.
max_cnt = 200    # 마지막 페이지

while True:
    links=[]
    print('Page ' + str(cnt))

    if cnt > max_cnt: # 페이지 설정
        break;

    cnt = cnt + 1
    driver.get('https://news.daum.net/breakingnews/politics?page=' + str(cnt) + '&regDate=' + date)
    #driver.implicitly_wait(10)  #10초안에 웹페이지를 load 하면 바로 넘어가거나, 10초를 기다림
    sleep(1)
    
    box_etc = driver.find_element(By.CLASS_NAME, 'list_news2.list_allnews') #기사 뭉치(?) 찾기
    posts = driver.find_elements(By.CLASS_NAME, 'cont_thumb')   #기사 뭉치(?)속에서 목록 찾기
    
    for post in posts:
        links.append(post.find_element(By.CLASS_NAME, 'link_txt').get_attribute("href"))

    print(links)

    #posts의 개수만큼 실행, post 안에서 a 태그 검색
    #links = [post.find_element(By.TAG_NAME, 'a').get_attribute("href") for post in posts] 
    
    #수정 필요. count 를 사용하지 않고도 15번 실행되게 해야함. 현재 series 주소를 함께 가져와 15번 이상 실행.
    count = 0
    for link in links:  #15번 실행
        count = count+1
        if count > 15:
            break
        
        print(link)
        driver.get(link)
        #sleep(random.randrange(1,7))
        sleep(1)
        
        print("댓글수:"+driver.find_element(By.CLASS_NAME, 'num_count').text)
        if int(driver.find_element(By.CLASS_NAME, 'num_count').text) != 0:  #댓글 수가 0이 아닐 때에만 실행
            driver.find_element(By.XPATH, '//*[@id="alex-area"]/div/div/div/div[1]/button').click()
            print("댓글창 열기 완료")
            sleep(1)
        while True:
            try:    #댓글 더보기 버튼을 누를 수 있을 때까지 클릭
                driver.find_element(By.CLASS_NAME, 'link_fold').click()
                print("댓글 더보기 클릭")
                sleep(1)
            except:
                break
        box_cmt = driver.find_element(By.CLASS_NAME, 'box_cmt')
        comments = box_cmt.find_elements(By.CLASS_NAME, 'desc_txt.font_size_')
        for comment in comments:
            print(comment.text)
            results.append(comment.text)
 

# 리스트를 하나의 문자열로 변환
long_results = ' '.join([str(result) for result in results])
print("파일 쓰기")
file.write(long_results)
print(long_results)

#한글 폰트는 따로 지정해야 함
WordCloud = WordCloud(width=2000, height=1500, font_path='/content/malgun.ttf').generate(long_results)

#이미지 그리기
print("워드클라우드 생성")
plt.figure(figsize=(40,30))
plt.imshow(WordCloud)
plt.show()

file.close()