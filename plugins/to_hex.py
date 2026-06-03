import struct

NAME = "十六进制转换"
CATEGORY = "编码"
DESC = "支持字符串/数值/内存转十六进制"

META = {
    "params": [
        {
            "name": "mode",
            "type": "radio",
            "label": "转换模式",
            "options": [
                "字符串转十六进制",
                "数值转十六进制",
                "内存十六进制"
            ]
        },

        {
            "name": "string_mode",
            "type": "radio",
            "label": "字符串转换方式",
            "options": [
                "UTF-8字节流",
                "Unicode码点"
            ],
            "visible_when": {
                "mode": "字符串转十六进制"
            }
        },

        {
            "name": "add_prefix",
            "type": "checkbox",
            "label": "自动添加0x前缀",
            "default": True,
            "visible_when": {
                "mode": "字符串转十六进制"
            }
        },

        {
            "name": "space_split",
            "type": "checkbox",
            "label": "结果空格分隔",
            "default": True,
            "visible_when": {
                "mode": "字符串转十六进制"
            }
        }
    ]
}

def str_to_hex(
    data: str,
    add_prefix: bool,
    space_split: bool
) -> str:

    result = []

    for c in data:
        h = f"{ord(c):02x}"

        if add_prefix:
            h = "0x" + h

        result.append(h)

    if space_split:
        return " ".join(result)

    return "".join(result)


def int_to_hex(data: str) -> str:
    # 支持空格分隔多个数字
    items = data.strip().split()
    result = []
    for x in items:
        try:
            num = int(x, 0)  # 支持十进制或 0x 前缀
            result.append(hex(num))
        except:
            result.append(f"ERR({x})")
    return ' '.join(result)


def mem_to_hex(data: str) -> str:
    # 支持空格分隔多个 float
    items = data.strip().split()
    result = []
    for x in items:
        try:
            num = float(x)
            packed = struct.pack('<f', num)
            hex_num = '0x' + ''.join(f'{i:02x}' for i in packed[::-1])
            result.append(hex_num)
        except:
            result.append(f"ERR({x})")
    return ' '.join(result)

def utf8_to_hex(
        data: str,
        add_prefix: bool,
        space_split: bool
) -> str:

    result = []

    for b in data.encode("utf-8"):

        h = f"{b:02x}"

        if add_prefix:
            h = "0x" + h

        result.append(h)

    if space_split:
        return " ".join(result)

    return "".join(result)

def unicode_to_hex(
        data: str,
        add_prefix: bool,
        space_split: bool
) -> str:

    result = []

    for c in data:

        h = f"{ord(c):x}"

        if add_prefix:
            h = "0x" + h

        result.append(h)

    if space_split:
        return " ".join(result)

    return "".join(result)

def run(data: str, config: dict) -> str:

    mode = config.get("mode", "")

    if mode == "字符串转十六进制":

        string_mode = config.get(
            "string_mode",
            "UTF-8字节流"
        )

        add_prefix = config.get(
            "add_prefix",
            True
        )

        space_split = config.get(
            "space_split",
            True
        )

        if string_mode == "UTF-8字节流":

            return utf8_to_hex(
                data,
                add_prefix,
                space_split
            )

        else:

            return unicode_to_hex(
                data,
                add_prefix,
                space_split
            )

    elif mode == "数值转十六进制":

        return int_to_hex(data)

    elif mode == "内存十六进制":

        return mem_to_hex(data)

    return data