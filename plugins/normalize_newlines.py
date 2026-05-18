NAME = "去除多余空行"
CATEGORY = "文本处理"
DESC = "去除多余换行，仅保留文本之间的换行"

def run(data: str) -> str:
    lines = data.splitlines()

    result = []

    for line in lines:
        # 保留非空行
        if line.strip() != "":
            result.append(line.strip())

    return "\n".join(result)