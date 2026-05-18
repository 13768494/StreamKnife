NAME = "去除重复行"
CATEGORY = "文本处理"
DESC = "删除重复行，仅保留第一次出现的行，保持原始顺序"

def run(data: str) -> str:
    lines = data.splitlines()

    seen = set()
    result = []

    for line in lines:
        clean_line = line.strip()

        if clean_line not in seen:
            seen.add(clean_line)
            result.append(clean_line)

    return "\n".join(result)