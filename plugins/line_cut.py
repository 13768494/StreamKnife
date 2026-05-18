NAME = "按字符裁剪整行"
CATEGORY = "文本处理"
DESC = "根据指定字符裁剪每一行文本（只匹配第一次出现的目标字符），如：switch#vlan data -> vlan data"

META = {
    "params": [
        {
            "name": "char",
            "type": "input",
            "label": "分隔字符"
        },
        {
            "name": "keep",
            "type": "radio",
            "label": "保留部分",
            "options": [
                "分隔符左侧(含)",
                "分隔符左侧(不含)",
                "分隔符右侧(含)",
                "分隔符右侧(不含)"
            ]
        }
    ]
}

def run(data: str, config: dict) -> str:
    ch = config.get("char", "")
    keep = config.get("keep", "分隔符右侧(不含)")

    if not ch:
        return data

    result = []

    for line in data.splitlines():
        if ch not in line:
            result.append(line)
            continue

        idx = line.find(ch)

        if keep == "分隔符左侧(含)":
            result.append(line[:idx+1])
        elif keep == "分隔符左侧(不含)":
            result.append(line[:idx])
        elif keep == "分隔符右侧(含)":
            result.append(line[idx:])
        elif keep == "分隔符右侧(不含)":
            result.append(line[idx+1:])

    return "\n".join(result)