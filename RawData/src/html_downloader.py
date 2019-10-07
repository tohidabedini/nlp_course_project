import requests


def url_saver_to_html(url, name):
    response = requests.get(url)

    p1 = open('../'+name+'.html', 'w', encoding="utf-8")
    p1.write(response.text)
    p1.close()


def url_list_creator(start, stop, main_pattern, ):
    url_list = []
    for i in range(start, stop+1):
        url_list.append(main_pattern + str(i))
    return url_list


url_list_shahriar = url_list_creator(1, 160, 'https://ganjoor.net/shahriar/gozidegh/sh')
url_list_saeb = url_list_creator(1, 200, 'https://ganjoor.net/saeb/divan-saeb/ghazalkasa/sh')

# print(url_list_saeb)


def url_list_downloader(url_list, name):
    count = 1
    for url in url_list:
        url_saver_to_html(url, name+"_sh"+str(count))
        count += 1


url_list_downloader(url_list_shahriar, "shahriar")
url_list_downloader(url_list_saeb, "saeb")




