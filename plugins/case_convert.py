NAME = "大小写转换"
CATEGORY = "文本处理"
DESC = "支持大小写转换（默认转大写）"

META = {
    "params": [
        {
            "name": "mode",
            "type": "radio",
            "label": "转换模式",
            "options": ["转大写", "转小写"]
        }
    ]
}


def run(data: str, config: dict) -> str:
    mode = config.get("mode", "转大写")

    if mode == "转大写":
        return data.upper()
    else:
        return data.lower()