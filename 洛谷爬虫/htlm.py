import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import os

app = Flask(__name__)

def scrape_luogu(difficulty, keywords):
    # 构造URL
    url = f"https://www.luogu.com.cn/problem/list?difficulty={difficulty}&keyword={keywords}"

    # 发送HTTP请求并获取页面内容
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 解析页面内容，获取题目和题解
    problems = soup.find_all("div", class_="lg-content-item")

    # 创建目录
    directory = f"{difficulty}{keywords}"
    os.makedirs(directory, exist_ok=True)

    # 写入文件
    for problem in problems:
        problem_title = problem.find("a").text.strip()
        problem_number = problem.find("span", class_="lg-right").text.strip()
        problem_url = "https://www.luogu.com.cn" + problem.find("a")["href"]

        # 写入题目
        problem_content = f"# {problem_number} - {problem_title}\n\n题目链接：[{problem_title}]({problem_url})\n"
        problem_filename = f"{problem_number}-{problem_title}.md"
        with open(os.path.join(directory, problem_filename), "w", encoding="utf-8") as f:
            f.write(problem_content)

        # 写入题解
        problem_solution = f"# {problem_number} - {problem_title} 题解\n\n题目链接：[{problem_title}]({problem_url})\n"
        solution_filename = f"{problem_number}-{problem_title}-题解.md"
        with open(os.path.join(directory, solution_filename), "w", encoding="utf-8") as f:
            f.write(problem_solution)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        difficulty = request.form.get("difficulty")
        keywords = request.form.get("keywords")
        scrape_luogu(difficulty, keywords)
        return "爬取完成！"

    return render_template("index.html")

if __name__ == "__main__":
    app.run()
    import re
    import urllib.request, urllib.error
    import bs4

    baseUrl = "https://www.luogu.com.cn/problem/P"
    savePath = "D:\编程练习\洛谷爬虫\problems//"
    minn = 1995
    maxn = 2000  # 最大题号


    def main():
        print("计划爬取到P{}".format(maxn))
        for i in range(minn, maxn + 1):
            print("正在爬取P{}...".format(i), end="")
            html = getHTML(baseUrl + str(i))
            if html == "error":
                print("爬取失败，可能是不存在该题或无权查看")
            else:
                problemMD = getMD(html)
                print("爬取成功！正在保存...", end="")
                saveData(problemMD, "P" + str(i) + ".md")
                print("保存成功!")
        print("爬取完毕")


    def getHTML(url):
        headers = {
            "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 85.0.4183.121 Safari / 537.36"
        }
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        if str(html).find("Exception") == -1:  # 洛谷中没找到该题目或无权查看的提示网页中会有该字样
            return html
        else:
            return "error"


    def getMD(html):
        bs = bs4.BeautifulSoup(html, "html.parser")
        core = bs.select("article")[0]
        md = str(core)
        md = re.sub("<h1>", "# ", md)
        md = re.sub("<h2>", "## ", md)
        md = re.sub("<h3>", "#### ", md)
        md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
        return md


    def saveData(data, filename):
        cfilename = savePath + filename
        file = open(cfilename, "w", encoding="utf-8")
        for d in data:
            file.writelines(d)
        file.close()


    if __name__ == '__main__':
        main()