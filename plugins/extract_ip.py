import re
import ipaddress

NAME = "提取 IP 地址"
CATEGORY = "网络数据"
DESC = "从文本中提取 IPv4 地址，如：auth-fail@@!!172.16.9.200&&&retrying -> 172.16.9.200"

def run(data: str) -> str:
    return "\n".join(
        str(ipaddress.ip_address(x))
        for x in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", data)
        if int(x.split('.')[0]) <= 255
    )