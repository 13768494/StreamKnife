NAME = "按字符插入换行"
CATEGORY = "文本处理"
DESC = "在指定字符位置插入换行，可选择是否保留该字符"

META = {
    "params": [
        {
            "name": "char",
            "type": "input",
            "label": "目标字符"
        },
        {
            "name": "mode",
            "type": "radio",
            "label": "处理方式",
            "options": ["替换为换行", "保留字符并在其前换行", "保留字符并在其后换行"]
        }
    ]
}

def run(data: str, config: dict) -> str:
    ch = config.get("char", "")
    mode = config.get("mode", "保留字符并在其后换行")

    if not ch:
        return data

    if mode == "替换为换行":
        # 直接把字符变为换行
        return data.replace(ch, "\n")
    elif mode == "保留字符并在其前换行":
        return data.replace(ch, "\n" + ch)

    # 保留字符，并在其后插入换行
    return data.replace(ch, ch + "\n")