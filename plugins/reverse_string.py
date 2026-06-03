import re

NAME = "文本逆序"
CATEGORY = "文本处理"
DESC = "将输入的字符串整个逆序输出"

def run(data: str, config: dict) -> str:
    return data[::-1]