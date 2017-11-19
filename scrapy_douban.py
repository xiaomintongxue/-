import re
import urllib
import urllib.request
import random
#from scipy.misc import imread
from bs4 import BeautifulSoup
import xlwt
#import jieba
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
import matplotlib.pylab as plt
#from lxml import etree
stars=[]   ##星级
authors=[] ## 作者
comments=[]## 评论内容
titles=[] ## 推荐程度
comment_times=[] ## 评论时间
votes=[] ## 点赞数
douban_films=[]##
#headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3159.5 Safari/537.36'}

my_headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"]

randdom_header={'User-Agent':random.choice(my_headers)}
#print(randdom_header)
for n in range(10):
    url='https://movie.douban.com/subject/1292052/comments?start='+str(n*20)+'&limit=20&sort=new_score&status=P&percent_type='
    request=urllib.request.Request(url,headers=randdom_header)
    response=urllib.request.urlopen(request)
    content=response.read()
    soup=BeautifulSoup(content,'html.parser',from_encoding='utf-8')

    #comment_votes=soup.find_all('span',attrs={'class':'votes'})##提取点赞“有用”数量
    get_star=soup.find_all('span',attrs={'class':re.compile('^allstar')})##提取评论给出的星级
    comment_time=soup.find_all('span',attrs={'class':'comment-time'})##评论时间
    comment_authors=soup.find_all('div',attrs={'class':'avatar'})
    comments_txt=soup.find_all('div',attrs={'class':'comment'})

    ###提取作者昵称
    for author in comment_authors:
        aut=re.findall(r'title="(.*)"',str(author))##正则匹配作者昵称
        authors.extend(aut)
    ###提取评论文本
    for comment in comments_txt:
        com=re.findall(r'<p class="">(.*)\n',str(comment))##提取评论文本，其中涉及对换行符的处理，可以用[\s\S]
        comments.extend(com)
    ###提取点赞数
    ##获取评论赞同数
###提取评论的点赞数，这里可以使用get_text()，但是需要注意，由于select获得的是list，因此需要后面加上[i]，使用soup.select('span[class="votes"]')[i]
    #vote=soup.select('span[class="votes"]')[i].text


    '''
    comments=soup.find_all('div',attrs={'class':'comment'})##提取评论
    for comment in comments:
        print(comment.p.text)
    '''
    comment_times.extend(re.compile(r'title="(.*)"').findall(str(comment_time)))
    stars.extend(re.compile(r'allstar(\d+)').findall(str(get_star)))##正则匹配星级
    titles.extend(re.compile(r'title="(\S+)"').findall(str(get_star)))##正则匹配推荐程度
    votes.extend(soup.select('span[class="votes"]'))
    ##按照格式输出爬取得内容


###打印内容
file=open('肖申克的救赎豆瓣评论.txt','w',encoding='utf-8')
for i in range(len(stars)):
    #print(authors[i]+' '+titles[i]+':'+str(int(stars[i])//10)+'星'+'\n')##输出形如【xxx 力荐：5星】格式文本
    #print(comments[i]+'\n')
    #print('----------'+'点赞数:'+' 时间：'+comment_times[i]+'\n')
    file.write(comments[i])
    file.write('\n')
    douban_films.append([authors[i],str(int(stars[i])//10)+'❤',titles[i],votes[i].text,comments[i],comment_times[i]])
    #text.extend(comments[i].replace(' ','').replace('，','').replace('。','').replace('！','').replace('？','')
    #            .replace('《','').replace('》','').replace('-','').replace('：','').replace(string.punctuation,''))
    #text.extend(comments[i].replace(string.punctuation,'').replace(string.whitespace,''))
file.close()

###内容存储到Excel
table_title=[u'作者',u'星级',u'推荐程度',u'点赞数',u'评论内容',u'评论时间']
workshop=xlwt.Workbook(encoding='utf-8')
worksheet=workshop.add_sheet('《肖申克的救赎》评论汇总')
for i in range(len(table_title)):
    worksheet.write(0,i,table_title[i])
for j in range(len(douban_films)):
    for k in range(len(douban_films[0])):
        worksheet.write(j+1,k,douban_films[j][k])
workshop.save('豆瓣肖申克的救赎评论.xls')

#bg_picture=imread('C:\\Users\\Administrator\\Desktop\\scrapy\\test.jpg')
wc=WordCloud(background_color="white",
                    max_words=2000,width=2048,height=1024,margin=2,
                    ##可选用自体STXINWEI.TTF,STKAITI.TTF,SIMYOU.TTF
                    ##需要指定字体，不然乱码
                    random_state=60,
                    font_path="C:\\Windows\\Fonts\\SIMYOU.TTF",
                    max_font_size=200).generate(''.join(comments))
WordCloud()
#image=ImageColorGenerator(bg_picture)
plt.figure()
plt.imshow(wc)
#plt.imshow(wc.recolor(color_func=image))
plt.axis('off')
plt.show()


