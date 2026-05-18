NAME = "去除行首尾无用字符"
CATEGORY = "文本处理"
DESC = "去除每一行开头和结尾的指定字符（默认去除空格）"

META = {
    "params": [
        {
            "name": "char_type",
            "type": "radio",
            "label": "需要去除的字符",
            "options": ["空格", "Tab", "逗号", "分号", "双引号", "单引号", "反引号"]
        }
    ]
}


def run(data: str, config: dict) -> str:
    char_type = config.get("char_type", "空格")

    char_map = {
        "空格": " ",
        "Tab": "\t",
        "逗号": ",",
        "分号": ";",
        "双引号": '"',
        "单引号": "'",
        "反引号": "`",
    }

    ch = char_map.get(char_type, " ")

    result = []

    for line in data.splitlines():
        # 只去除首尾，不影响中间
        trimmed = line.strip(ch)
        result.append(trimmed)

    return "\n".join(result)