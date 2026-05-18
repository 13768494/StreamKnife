import inspect
from core.registry import FUNCTIONS


class Dispatcher:
    def run(self, func_name, data, config=None):
        plugin = FUNCTIONS.get(func_name)

        if not plugin:
            return data

        func = plugin["func"]

        # 关键：判断函数参数个数
        sig = inspect.signature(func)

        if len(sig.parameters) == 1:
            # 旧插件
            return func(data)
        else:
            # 新插件
            return func(data, config or {})