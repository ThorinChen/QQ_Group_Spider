
import tkinter.messagebox as msgbox
import webbrowser
import tkinter as tk
from selenium.webdriver import Chrome
import time
import csv
import re
from selenium.webdriver.common.keys import Keys

# pyinstaller -w qq_reotile.py
class Reptile:
    def __init__(self,width=500,height=300):
        self.w = width
        self.h = height
        self.title =  "qq群批量收集"
        self.root = tk.Tk(className=self.title)

        # 地址变量
        self.url = tk.StringVar()
        self.file = tk.StringVar()
        self.v = tk.StringVar()
        self.v.set("20") # 默认是20

        # 小型框架
        frame_1 = tk.Frame(self.root)
        lable = tk.Label(frame_1,text="qq群地址：")
        self.entry = tk.Entry(frame_1,textvariable=self.url,width=35) # 输入框
        play = tk.Button(frame_1, text="开始爬取", font=('楷体', 12), fg='black', width=5, height=1, command=self.merge)

        lable1 = tk.Label(frame_1, text="文件名：")
        self.entry1 = tk.Entry(frame_1, textvariable=self.file, width=35)  # 输入框

        # 单选按钮
        choice1 = tk.Radiobutton(frame_1,text="小群",value="20",variable=self.v)
        choice2 = tk.Radiobutton(frame_1,text="中等群",value="30",variable=self.v)
        choice3 = tk.Radiobutton(frame_1,text="大群",value="40",variable=self.v)

        frame_1.pack()
        lable.grid(row=0,column=0)
        self.entry.grid(row=0,column=1)
        play.grid(row=0,column=2,ipadx=10,ipady=10)
        lable1.grid(row=1,column=0)
        self.entry1.grid(row=1,column=1)
        choice1.grid(row=2,column=0)
        choice2.grid(row=2,column=1)
        choice3.grid(row=2,column=2)

    def merge(self):
       ips = self.url.get()
       file = self.file.get()
       sum  = self.v.get()
       if not ips or not file or not sum:
           msgbox.showerror(title="地址或文件名未输入", message='大哥你倒是填地址呀！！！')
       elif not re.match("(http|https)://[^\s]+", ips):
           msgbox.showerror(title="输入错误", message='地址搞错了！！！')
           self.entry.delete(0, 'end')
           self.entry1.delete(0, 'end')
       else:
           print(ips,file,sum)
           # 调用爬虫函数
           self.main(ips,file,sum)


    def main(self,ips,file,sum):
        url = ips
        sum = int(sum)
        chrome = Chrome()
        # "https://qun.qq.com/member.html#gid=230690127"
        chrome.get(url)
        time.sleep(5)
        chrome.maximize_window()
        # 页面下滑
        for i in range(0, sum):
            chrome.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(0.5)
        time.sleep(3)

        trs = chrome.find_elements_by_xpath('//*[@id="groupMember"]/tbody[@class="list"]')
        # qun_name = chrome.find_element_by_xpath('//*[@id="groupTit"]')
        qun_name = file
        print('群名字：%s', qun_name)
        print(trs)

        csv_path = '../'+qun_name + '.csv'
        header = ('序号',  'QQ昵称',  'QQ群名称',  'qq号',  '性别',  'Q龄',  '入群时间',  '群等级',  '最后发言时间',  '邮箱')
        with open(csv_path, 'a', newline="", encoding='gbk', errors="ignore") as f:
            writer = csv.writer(f)
            writer.writerow(header)

        s = 0
        for i in trs:
            cc = i.find_elements_by_xpath('./tr')
            for c in cc:
                try:
                    
                    #QQ号
                    qq = c.find_element_by_xpath("./td[5]").text
                    #性别
                    sex = c.find_element_by_xpath("./td[6]").text
                    #昵称
                    nick_name = c.find_element_by_xpath('./td[3]/span').text
                    if not nick_name:
                        nick_name = "[空]"
                    #群名称
                    qq_name = c.find_element_by_xpath('./td[4]/span').text
                    if not qq_name:
                        qq_name = "[空]"
                    #Q龄
                    qq_age =  c.find_element_by_xpath("./td[7]").text
                    #入群时间
                    join_time =  c.find_element_by_xpath("./td[8]").text
                    #群等级
                    qq_level =  c.find_element_by_xpath("./td[9]").text
                    #最后发言时间
                    last_word_time =  c.find_element_by_xpath("./td[10]").text
                    #邮箱
                    qq_mail = qq+"@qq.com"
                    
                except:
                    pass
                    # if not name:
                #     name = "空"
                s += 1

                with open(csv_path, 'a', newline="", encoding='gbk', errors="ignore") as f:
                    csvs = csv.writer(f, delimiter=",")
                    csvs.writerow([s, nick_name,qq_name, qq, sex,qq_age,join_time,qq_level,last_word_time,qq_mail])

                print("序号：%s  --昵称：%s, --QQ群名称：%s, --qq号：%s, 性别：%s ,--Q龄：%s ,--入群时间：%s ,--群等级：%s ,--最后发言时间：%s,--邮箱：%s " % (s, nick_name,qq_name, qq, sex,qq_age,join_time,qq_level,last_word_time,qq_mail))

        msgbox.showerror(title="成功爬完", message='爬虫结束,已保存')
        chrome.quit()
        # 爬虫结束
        # 清楚输入框
        self.entry.delete(0,'end')
        self.entry1.delete(0,'end')

    def loop(self):
        self.root.resizable(True,True)
        self.root.mainloop()

if __name__ == '__main__':
    rep = Reptile()
    rep.loop()