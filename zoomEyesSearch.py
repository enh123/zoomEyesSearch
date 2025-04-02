#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import argparse
import sys
import json

requests.packages.urllib3.disable_warnings()


class ZoomEyeSubdomianSearch:
    def __init__(self, domain, line, proxy, output_file_name):
        self.domain = domain if domain else None
        self.proxy = {"http": proxy, "https": proxy} if proxy else None
        self.output_file_name = output_file_name if output_file_name else None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        }
        self.line = line if line else 500
        self.apikey = ""

    def search(self):
        if self.apikey == "":
            sys.exit("请先在ZoomEyeSubdomianSearch.py的__init__函数中添加apikey")
        url = f"https://api.zoomeye.org/domain/search?q={self.domain}&type=1&page=1&s={self.line}"
        self.headers["API-KEY"] = self.apikey;
        print("正在查询请稍等...")
        response = requests.get(url=url, headers=self.headers, proxies=self.proxy, verify=False)
        if "login_required" in response.text:
            sys.exit("API-KEY 错误请重新填写")
        if "403" in response.text and "not aviliable in your area":
            sys.exit("你的ip或你所在的地区无法使用zoomEyes查询,请使用中国大陆的ip")

        data = json.loads(response.text)

        if not data["list"]:
            sys.exit("未查询到任何子域名")
        domain_list = [item["name"] for item in data["list"]]
        if "-o" in sys.argv or "--output" in sys.argv:
            with open(f"{self.output_file_name}", 'a', encoding='utf-8') as file:
                for domain in domain_list:
                    file.write(domain + '\n')

        for domain in domain_list:
            print(domain)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain", dest="domain", help="指定一个域名", required=True)
    parser.add_argument("-l", "--line", dest="line", help="要查询多少条域名,默认查询500条", required=False)
    parser.add_argument("-p", "--proxy", "-proxy", dest="proxy", help="设置代理,例如:--proxy=http://127.0.0.1:8080",
                        required=False)
    parser.add_argument("-o", "--output", dest="output_file_name", help="输出到一个指定文件", required=False)
    args = parser.parse_args()
    subdomain_search = ZoomEyeSubdomianSearch(args.domain, args.line, args.proxy, args.output_file_name)
    subdomain_search.search()


if __name__ == "__main__":
    main()

