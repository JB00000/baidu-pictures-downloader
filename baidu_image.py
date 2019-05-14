# -*- coding: UTF-8 -*-
import requests
from requests import codes
import os
from hashlib import md5
import json
from requests.exceptions import ConnectionError
import re

headers = {
        'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'Connection': 'keep-alive',
        'Cookie': 'BDqhfp=%E6%A1%A5%E6%9C%AC%E7%8E%AF%E5%A5%88%26%26NaN-1undefined%26%260%26%261; BAIDUID=CC5FFA3351D43761DE6044995E054938:FG=1; BIDUPSID=CC5FFA3351D43761DE6044995E054938; PSTM=1539496117; __cfduid=d0cdbe29aa3683ef5f9da23a272300b701542000309; BDUSS=B3c0o1amNyOXRtOU9RcUd2UG5vb3oxdFNCV3pMeXpNRWhQLU1naGhITVBqQ0JjQVFBQUFBJCQAAAAAAAAAAAEAAABYjoVTvnzso97GxNq0~ZVy73cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA~~-FsP~~hbcT; pgv_pvi=7188965376; indexPageSugList=%5B%22%E7%8E%8B%E7%A5%96%E8%B4%A4%22%2C%22%E6%A1%A5%E6%9C%AC%E7%8E%AF%E5%A5%88%22%2C%22%E6%96%AF%E5%98%89%E4%B8%BD%E7%BA%A6%E7%BF%B0%E9%80%8A%22%2C%22%E4%BD%90%E4%BD%90%E6%9C%A8%E5%B8%8C%22%2C%22%E7%9F%B3%E5%8E%9F%E9%87%8C%E7%BE%8E%22%2C%22%E4%BD%A0%E6%9C%80%E6%83%B3%E7%9F%A5%E9%81%93%E7%9A%84%E7%A7%91%E5%AD%A6%22%2C%22%E7%94%B5%E8%84%91%E8%BE%90%E5%B0%84%22%5D; locale=zh; BDRCVFR[pNjdDcNFITf]=mk3SLVN4HKm; delPer=0; PSINO=3; H_PS_PSSID=1457_21100_28607_28585_28519_20719; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; userFrom=www.baidu.com'
    }

def get_page(pn, url, keyword):
    params = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'ct': '201326592', 
        'is': '',
        'fp': 'result',
        'queryWord': keyword,
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'adpicid': '',
        'st': '',
        'z': '',
        'ic': '',
        'hd': '',
        'latest': '',
        'copyright': '',
        'word': keyword,
        's': '',
        'se': '',
        'tab': '',
        'width': '',
        'height': '',
        'face': '',
        'istype': '',
        'qc': '',
        'nc': 1,
        'fr': '',
        'expermode': '',
        'force': '',
        'cg': 'star',
        'pn': pn,
        'rn': '30',
        'gsm': str(hex(pn)),
        '1550462139279': ''
    }

    try:
        resp = requests.get(url, params=params, headers=headers)
        if resp.status_code == 200:
            resp = json.loads(resp.text.replace("'", '"'))
            return resp
    except ConnectionError as e:
        print('Error Occurred', e.args)
        return None

def parse_image(json):
    if json.get('data'):
        data = json.get('data')
        print(data)
        for item in data:
            title = item.get('fromPageTitleEnc')
            image = item.get('thumbURL')
            yield{
                'title': title,
                'image': image
            }
            print(image)

def save_image(item, keyword):
    img_path = keyword
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    try:
        resp = requests.get(item.get('image'), headers=headers)
        if codes.ok == resp.status_code:
            file_path = img_path + os.path.sep + '{file_name}.{file_suffix}'.format(
                file_name=md5(resp.content).hexdigest(),
                file_suffix='jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(resp.content)
                print('Downloaded img path is %s' % file_path)
            else:
                print('Already downloaded.', file_path)
    except requests.ConnectionError:
        print("Failed to Save image, item %s" % item)

def main(pn):
    json = get_page(pn, url=url, keyword=keyword)
    for item in parse_image(json):
        if not item.get('title') == None:
            save_image(item, keyword=keyword)

if __name__ == '__main__':
    url = input('请输入url:')
    keyword = input('请输入图片总名称:')
    for i in range(30, 300, 30):
        main(i)
