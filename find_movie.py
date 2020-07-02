import json
from time import time
import tkinter
from tkinter import END


def GUI(movies):
    root=tkinter.Tk()
    root.title('查询豆瓣Top250电影')
    root.geometry('800x600')

    query_label=tkinter.Label(root,text='请输入查询信息',font=('微软雅黑',10))
    query_label.place(relx=0.025, rely=0.03)

    entry=tkinter.Entry(root,font=('微软雅黑',10))
    entry.place(relx=0.025, rely=0.1, height=30, relwidth=0.5)


    def find_movie():
        start=time()
        show_result.delete(1.0,END)
        query=entry.get()
        count=0
        for movie in movies:
            for value in movie.values():
                if query in value:
                    show_result.insert(END,'排名：%s，评分：%s，'%(movie["ranking"],movie["score"]))
                    name=''
                    for each in movie["name"]:
                        name+=each+'  '
                    show_result.insert(END,'电影名：%s，'%name.strip())
                    director=''
                    for each in movie["director"]:
                        director+=each+'  '
                    show_result.insert(END,'导演：%s\n'%director.strip())
                    show_result.insert(END,'剧情简介：\n%s\n'%movie["story_summary"])
                    show_result.insert(END,'URL：%s'%movie["url"])
                    show_result.insert(END,'\n')
                    show_result.insert(END,'\n')
                    count+=1
                    break
        end=time()
        cost_time=end-start
        if count!=0:
            result_str.set('共找到%d部电影，花费%f秒'%(count,cost_time))
        else:
            result_str.set('你想要找的电影不在豆瓣Top250中')
        


    button=tkinter.Button(root,text='查询',command=find_movie,font=('微软雅黑',10))
    button.place(relx=0.55, rely=0.1, height=30, relwidth=0.1)

    result_str=tkinter.StringVar()
    result_label=tkinter.Label(root,textvariable=result_str,font=('微软雅黑',10))
    result_label.place(relx=0.65,rely=0.1,height=30, relwidth=0.4)

    show_result=tkinter.Text(root,font=('微软雅黑',10))
    show_result.place(relx=0.025, rely=0.2, relheight=0.75, relwidth=0.95)

    root.mainloop()

def main():
    with open('douban_movie_top250.json','r',encoding='utf-8') as f:
        data=json.loads(f.read())
    movies=[]
    for each in data:
        movies.append(each["result"])
    GUI(movies)

if __name__ == "__main__":
    main()
