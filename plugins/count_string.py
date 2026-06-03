import re

NAME = "文本统计"
CATEGORY = "文本处理"
DESC = "统计文本长度、字符出现次数、行数等信息"

META = {
    "params": [
        {
            "name": "target_char",
            "type": "input",
            "label": "统计指定字符（留空则不统计）"
        },
        {
            "name": "count_total",
            "type": "checkbox",
            "label": "统计总长度",
            "default": True
        },
        {
            "name": "count_no_space",
            "type": "checkbox",
            "label": "统计去空白后的长度",
            "default": False
        },
        {
            "name": "count_lines",
            "type": "checkbox",
            "label": "统计行数",
            "default": True
        },
        {
            "name": "count_target",
            "type": "checkbox",
            "label": "统计指定字符出现次数",
            "default": True
        }
    ]
}


def run(data: str, config: dict) -> str:
    result = []

    target_char = config.get("target_char", "")

    if config.get("count_total", False):
        result.append(f"总长度: {len(data)}")

    if config.get("count_no_space", False):
        no_space = re.sub(r"\s+", "", data)
        result.append(f"去空格/回车后总长度: {len(no_space)}")

    if config.get("count_lines", False):
        line_count = len(data.splitlines())
        result.append(f"总行数: {line_count}")

    if (
        config.get("count_target", False)
        and target_char
    ):
        count = data.count(target_char)
        result.append(
            f"字符 '{target_char}' 出现次数: {count}"
        )

    if not result:
        return "未选择任何统计项目"

    return "\n".join(result)