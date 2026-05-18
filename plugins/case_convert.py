NAME = "大小写转换"
CATEGORY = "文本处理"
DESC = "支持大小写转换（默认转大写）"

META = {
    "params": [
        {
            "name": "mode",
            "type": "radio",
            "label": "转换模式",
            "options": ["upper", "lower"]
        }
    ]
}


def run(data: str, config: dict) -> str:
    mode = config.get("mode", "upper")

    if mode == "upper":
        return data.upper()
    else:
        return data.lower()