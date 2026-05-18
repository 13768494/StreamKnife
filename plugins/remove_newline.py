NAME = "取消换行"
CATEGORY = "文本处理"
DESC = "移除所有换行符，可用指定字符替代"

META = {
    "params": [
        {
            "name": "joiner",
            "type": "input",
            "label": "换行替换为（留空则直接拼接）"
        }
    ]
}

def run(data: str, config: dict) -> str:
    joiner = config.get("joiner", "")

    # 统一处理不同系统换行
    lines = data.splitlines()

    # 直接拼接 or 用指定字符拼接
    return joiner.join(lines)