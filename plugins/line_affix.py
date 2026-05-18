NAME = "为每行添加头/尾字符串"
CATEGORY = "文本处理"
DESC = "在每一行开头或结尾添加指定字符串"

META = {
    "params": [
        {
            "name": "prefix",
            "type": "input",
            "label": "头部添加字符串"
        },
        {
            "name": "suffix",
            "type": "input",
            "label": "尾部添加字符串"
        }
    ]
}


def run(data: str, config: dict) -> str:
    prefix = config.get("prefix", "")
    suffix = config.get("suffix", "")

    result = []

    for line in data.splitlines():
        if line.strip() == "":
            result.append(line)
        else:
            result.append(f"{prefix}{line}{suffix}")

    return "\n".join(result)