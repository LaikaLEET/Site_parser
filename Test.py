import requests
from bs4 import BeautifulSoup
import re
def data(url):
    url_general = 'https://www.rusprofile.ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    regex_num = re.compile(r'/id/\d+')
    regex_cap = re.compile(r'Уставный капитал\d*')
    named = []
    ogrnd = []
    okpod = []
    statusd = []
    dated = []
    capitald = []
    for i in soup.find_all('a'):
        rehref = regex_num.findall(i.get('href'))
        if rehref:
            href = i.get('href')
            url_company = url_general+href
            response_company = requests.get(url_company)
            soup_company = BeautifulSoup(response_company.text, 'lxml')
            name = soup_company.find_all('div', class_='company-name')
            named.append(name[0].text)
            ogrn = soup_company.find_all('span', class_='copy_target')[0]
            ogrnd.append(ogrn.text)
            okpo = soup_company.find(id='clip_okpo')
            if okpo:
                okpod.append(okpo.text)
            else:
                okpod.append('None')
            status = soup_company.find_all('div', class_='company-status')
            statusd.append(status[0].text)
            date = soup_company.find(itemprop="foundingDate")
            dated.append(date.text)
            capi = soup_company.find_all('dl', class_='company-col')
            cap = ''
            for j in range(len(capi)):
                cap1 = regex_cap.findall(capi[j].text)
                if cap1:
                    capital = capi[j].text
                    capital = capital.split('\n')
                    capitald.append(capital[3])
    dictionary = {'name': named, 'ogrn': ogrnd, 'okpo': okpod, 'status': statusd, 'date': dated, 'capital': capitald}
    return dictionary
if __name__ == "__main__":
    url_first = 'https://www.rusprofile.ru/codes/89220'
    url_second = 'https://www.rusprofile.ru/codes/429110'
    first_dict = data(url_first)
    second_dict = data(url_second)
