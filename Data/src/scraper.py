from bs4 import BeautifulSoup


def file_downloader(name, start, stop, dest):
    file = open(dest, "w", encoding="utf-8")
    for i in range(start, stop+1):
        with open("../../RawData/"+name+str(i)+".html", encoding="utf-8")as html_file:
            soup = BeautifulSoup(html_file, 'lxml')

        for j in soup.find_all('div', class_=["m1", "m2"]):
            file.write(j.p.text+"\n")
    file.close()


file_downloader("shahriar_sh", 1, 160, "../label1.txt")
file_downloader("saeb_sh", 1, 200, "../label2.txt")

