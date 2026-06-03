import re

NAME = "提取 hex"
CATEGORY = "IDA"
DESC = "适用从IDA栈中提取 hex 内容，如：Stack[000067F0]:000000000060FD00 db  66h ; f -> 0x66h"

def run(data: str) -> str:
    # 只匹配：66h / FFh / 0Ah 这种形式
    matches = re.findall(r'\b([0-9A-Fa-f]{1,2})h\b', data)

    result = [f"0x{m.upper()}" for m in matches]

    return "\n".join(result)