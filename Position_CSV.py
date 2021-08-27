import requests
import re
import csv


def addrTo(addr):
    res = requests.get(
        "http://api.map.com.tw/net/GraphicsXY.aspx?",
        data={
            'search_class': 'address',
            'searchkey': 'abc',
            'fun': 'funB',
            'SearchWord': addr
        },
        headers={
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
            'Connection': 'close',
            'Host': 'api.map.com.tw',
            'Referer': 'http://api.map.com.tw/API_Sample/Sample/GetAddressCoordinates.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        }
    )
    return res.text


if __name__ == "__main__":

    with open('output.csv', 'w', encoding='UTF-8', newline='') as write_file:
        writer = csv.writer(write_file)
        writer.writerow(['地址', 'Lat緯度', 'Lng經度'])
        count = 1

        with open('台鐵.csv', 'r', newline='', encoding="utf-8") as csvfile:
            # 讀取 CSV 檔案內容
            rows = csv.reader(csvfile)
            for row in rows:
                # 捕捉到地址(看第幾欄)
                addr = row[2]

                # 透過捕捉到地址放入函式中取得json資料
                json_data = addrTo(addr)
                # print(json)
                # time.sleep(0)

                # 利用正則來擷取我們所需的經緯度資料
                # \d+\.?\d* 小數點形式的數字
                try:
                    m_Lat = re.search(r'(?<=lat":").*?(\d+\.?\d*)', json_data)
                    m_Lng = re.search(r'(?<=lng":").*?(\d+\.?\d*)', json_data)
                    print(addr)
                    print(m_Lat.group())
                    print(m_Lng.group())
                    print(count)
                    count += 1
                    writer.writerow([addr, m_Lat.group(), m_Lng.group()])
                except Exception as e:
                    print(json_data)
                    print(e)