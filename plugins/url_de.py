from urllib.parse import quote, unquote

NAME = "URL编码/解码"
CATEGORY = "编码"
DESC = "对输入内容进行URL编码或解码"

META = {
    "params": [
        {
            "name": "mode",
            "type": "radio",
            "label": "处理模式",
            "options": [
                "URL编码",
                "URL解码"
            ]
        }
    ]
}

def run(data: str, config: dict) -> str:
    mode = config.get("mode", "URL编码")
    result = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            if mode == "URL解码":
                result.append(unquote(line))
            else:
                result.append(quote(line, safe=""))

        except Exception:
            result.append(line)

    return "\n".join(result)