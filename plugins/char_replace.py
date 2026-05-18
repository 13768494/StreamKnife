import re

NAME = "字符替换"
CATEGORY = "文本处理"
DESC = "将指定字符替换为另一个字符"

META = {
    "params": [
        {
            "name": "old",
            "type": "input",
            "label": "匹配内容"
        },
        {
            "name": "new",
            "type": "input",
            "label": "替换为"
        },
        {
            "name": "case_sensitive",
            "type": "checkbox",
            "label": "区分大小写",
            "default": True
        }
    ]
}

def run(data: str, config: dict) -> str:
    old = config.get("old", "")
    new = config.get("new", "")
    case_sensitive = config.get("case_sensitive", True)

    if not old:
        return data

    if case_sensitive:
        return data.replace(old, new)

    # 不区分大小写 → 用正则
    pattern = re.compile(re.escape(old), re.IGNORECASE)
    return pattern.sub(new, data)