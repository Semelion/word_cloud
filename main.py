import re
import pandas as pd
from profanity_filter import Filter
from wordcloud import WordCloud
from PIL import Image
import time
import cv2
import numpy
# import matplotlib.pyplot as plt

def convert_google_sheet_url(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)

    return new_url

# Replace with your modified URL

url = input("Ссылка на таблицу: ")
question = input("Как звучит нужный вопрос: ")
# url = 'https://docs.google.com/spreadsheets/d/1E8Hm1gXt1NfNoYLMB-RZCuFtACHSz3Mg3TG5J98PVMg/edit?usp=sharing'

new_url = convert_google_sheet_url(url)

# print(new_url)
print("start")
while True:
    df = pd.read_csv(new_url)
    # print(df.head())
    big_list = ""
    for uni in df[question]:
        list = uni.split(",")
        if " " in list:
            list.remove(" ")
        for i in range(len(list)):
            f = Filter(list[i], clean_word='')
            list[i] = f.clean()
            if(list[i][0] == ' '):
                list[i] = list[i][1:]
            list[i] = " ".join(list[i].split(" "))
            if list[i] != '':
                big_list +=list[i].replace(" ", "_") + " "
    # print(big_list)

    # Генерируем облако слов
    wordcloud = WordCloud(width = 3000,
                          height = 1500,
                          random_state=1,
                          background_color='black',
                          margin=20,
                          colormap='Set2',
                          max_font_size=300,
                          collocations=False).generate(big_list)


    # cv2.imshow("test", wordcloud.to_image())
    # print(wordcloud.to_image())

    im = wordcloud.to_image()
    im = im.convert('RGB')

    open_cv_image = numpy.array(im)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    cv2.imshow("ss", open_cv_image)
    time.sleep(5)
    if(cv2.waitKey(33) == 27):
        break


# wordcloud.to_file('hp_cloud_simple.png')
