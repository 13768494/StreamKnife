NAME = "按字符串筛选整行"
CATEGORY = "文本处理"
DESC = "筛选包含指定字符串的整行文本"

META = {
    "params": [
        {
            "name": "keyword",
            "type": "input",
            "label": "匹配字符串"
        },
        {
            "name": "case_sensitive",
            "type": "checkbox",
            "label": "区分大小写",
            "default": False
        }
    ]
}


def run(data: str, config: dict) -> str:
    keyword = config.get("keyword", "")
    case_sensitive = config.get("case_sensitive", False)

    if not keyword:
        return data

    result = []

    for line in data.splitlines():
        src = line if case_sensitive else line.lower()
        kw = keyword if case_sensitive else keyword.lower()

        if kw in src:
            result.append(line)

    return "\n".join(result)