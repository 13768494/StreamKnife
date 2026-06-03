# 一、项目概述

StreamKnife 是一个基于 Python + PySide6 构建的桌面数据处理工具框架，采用插件化架构设计。

核心特点：

- 插件化扩展（新增功能无需修改核心代码）
- GUI 与业务逻辑完全解耦
- 支持分类 / 搜索 / 描述显示
- 可通过 PyInstaller 打包为 .exe 独立运行

> 平台：Windows 11、Python 3.12.7

---

# 二、项目目录结构说明

```
data_tool/
│
├── main.py                  # 程序入口（启动GUI + 加载插件）
│
├── core/                   # 核心调度层
│   ├── dispatcher.py       # 功能执行调度器（执行插件链）
│   ├── registry.py         # 插件自动加载与注册中心
│   └── __init__.py
│
├── ui/                     # UI界面层
│   ├── window.py           # 主窗口（分类/插件/输入输出）
│   └── __init__.py
│
├── plugins/                # 插件功能模块（核心扩展区）
│   ├── *.py                # 各种功能插件
│   └── __init__.py
│
├── utils/                  # 工具函数
│   ├── file_io.py          # 文件读写
│   ├── common.py           # 通用工具（预留）
│   └── __init__.py
│
├── config/                 # 配置目录（可扩展）
│   └── settings.json       # 插件配置/系统配置（可选）
│
├── assets/                 # UI资源（图标等，可选）
│
└── requirements.txt        # 依赖管理
```

------

# 三、核心架构说明

## 1. 架构分层

```text
UI层（window.py）
    ↓
调度层（dispatcher.py）
    ↓
注册层（registry.py）
    ↓
插件层（plugins/*.py）
```

------

## 2. 数据流

```text
用户输入
   ↓
选择插件（UI）
   ↓
dispatcher 调度
   ↓
plugin.run() 执行
   ↓
结果返回 UI
```

------

# 四、插件系统规范（重点）

## 1. 插件基本结构

每个插件必须遵循以下规范：

```python
NAME = "插件名称（UI显示）"
CATEGORY = "分类（text / network / crypto 等）"
DESC = "插件描述"

# 或 def run(data: str, config: dict) -> str:
def run(data: str) -> str:
    return data
```

------

## 2. 必须规则

- 必须包含 `run(data: str) -> str`或`def run(data: str, config: dict) -> str:`
- 必须定义 `NAME`
- 必须定义 `CATEGORY`
- 建议定义 `DESC`

------

## 3. 分类建议

| 分类    | 用途         |
| ------- | ------------ |
| text    | 文本处理     |
| network | 网络/IP/协议 |
| crypto  | 加密/哈希    |
| util    | 工具类       |
| other   | 其他         |

------

# 五、核心模块说明

------

## 1. main.py

作用：

- 程序入口
- 初始化 GUI
- 加载插件
- 注入 dispatcher

关键流程：

```text
load_plugins()
↓
创建 dispatcher
↓
初始化 UI
↓
绑定插件数据
↓
启动窗口
```

------

## 2. core/registry.py

作用：

- 自动扫描 plugins 目录
- 加载插件模块
- 构建插件注册表 FUNCTIONS

输出结构：

```python
FUNCTIONS = {
    "ip_extract": {
        "name": "提取IP",
        "category": "network",
        "desc": "...",
        "func": run
    }
}
```

------

## 3. core/dispatcher.py

作用：

- 执行插件逻辑链
- 支持多个插件顺序执行

执行模式：

```text
data → plugin1 → plugin2 → plugin3 → result
```

------

## 4. ui/window.py

作用：

- UI主界面
- 分类展示
- 插件列表展示
- 输入输出控制
- 搜索过滤

核心组件：

- category_list（分类）
- plugin_list（插件）
- input_box（输入）
- output_box（输出）
- search_box（搜索）

------

## 5. utils/file_io.py

作用：

- 输出结果保存
- 文件写入封装

------

# 六、二次开发规范（重要）

------

> 想要什么功能直接按照规范编写对应的python插件放入plugins文件夹即可使用

## 1. 插件开发规范

### 正确示例：

```python
NAME = "转大写"
CATEGORY = "text"
DESC = "将文本转换为大写"

def run(data):
    return data.upper()
```

------

## 2. 命名规范

### 文件命名：

- snake_case
- 示例：`ip_extract.py`

------

### 函数规范：

- 统一使用 `run()`
- 不允许多入口函数

------

## 3. 不允许行为

- ❌ 在 UI 中写业务逻辑
- ❌ 在插件外调用 UI
- ❌ 修改 dispatcher 做业务判断
- ❌ plugin 内部访问 UI

------

## 4. 推荐行为

- ✔ 所有逻辑写入 plugins
- ✔ UI 只负责展示与交互
- ✔ dispatcher 只做调度
- ✔ registry 只做注册

------

## 5. 扩展插件方式

新增功能：

```text
plugins/new_feature.py
```

无需修改任何核心代码。

------

# 七、UI交互说明（使用方式）

------

## 1. 基本流程

1. 输入数据
2. 选择左上方分类
3. 选择对应插件（鼠标悬停有提示）
4. 点击“执行”
5. 查看输出结果

------

## 2. 搜索功能

- 输入关键字自动过滤插件
- 支持名称模糊匹配

------

## 3. 分类功能

- 点击左上方分类
- 自动刷新右侧插件列表

------

## 4. 多插件执行（还在做）

- 支持多选插件
- 按选择顺序依次执行

------

# 八、打包说明（exe生成）

使用 PyInstaller 可以把你当前这个 PySide6 插件化项目直接打包为可双击运行的 `.exe`，下面按可直接成功的步骤给出。

---

## 1、安装依赖

在项目根目录执行：

```bash
pip install pyinstaller
```

---

## 2、必须先确认项目能正常运行

```bash
python main.py
```

无报错再进行打包。

---

## 3、关键点（非常重要）

项目有两个特性：

* 动态加载 `plugins/`（importlib）
* 使用 PySide6

这两点都会导致 **默认打包失败**，所以必须加参数。

---

## 4、第一次生成 spec 文件（推荐做法）

在项目根目录执行：

```bash
pyi-makespec -F -w main.py
```

会生成：

```
main.spec
```

---

## 5、修改 `main.spec`（关键步骤）

打开 `main.spec`，找到 `Analysis` 部分，修改为：

```python
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('plugins', 'plugins'),
        ('config', 'config'),
        ('assets', 'assets')
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
```

###### 解释

| 项            | 作用                      |
| ------------- | ------------------------- |
| datas         | 把插件目录一并打包进去    |
| hiddenimports | 解决 PySide6 打包缺失问题 |

---

## 6、正式打包

```bash
pyinstaller main.py --hidden-import=json --hidden-import=importlib --hidden-import=plugins --collect-submodules=plugins --add-data "plugins;plugins"
```

完成后生成：

```
dist/main.exe
```

---

## 7、测试 exe

双击 `dist/main.exe`，应可直接运行，插件仍然可以被动态加载。

---

## 8、后期每次更新打包

以后只需要执行：

```bash
pyinstaller main.spec
```

无需再写参数。

> 不想打包直接命令行调用python运行main.py也可以使用，现阶段运行.exe会有黑窗口

----

# 九、性能与结构建议

------

## 1. 插件数量增长建议

当插件 > 30：

- 增加分页
- 或搜索优先模式

------

## 2. UI优化方向

- Tab分区（输入 / 输出 / 日志）
- 插件启用/禁用
- 插件排序

------

## 3. 架构升级方向

未来可扩展为：

- 工作流编排系统（pipeline UI）
- 插件市场机制（动态加载zip）
- 多线程处理框架
- REST API接口化

------

# 十、总结

StreamKnife 当前已具备：

✔ 插件化架构
✔ UI与逻辑解耦
✔ 可扩展功能系统
✔ 分类/搜索/描述支持
✔ 可打包独立运行

属于标准“轻量级桌面插件框架”。

# *测试数据

```
GET /api/login 200
GET /api/login 200
GET /api/login 200
GET /api/login 200
POST /api/login 401
GET /dashboard 302
GET /assets/logo.png 200
POST /api/user/update 500
POST /api/user/update 500
POST /api/user/update 500
POST /api/user/update 500
DELETE /api/user/42 403
GET /api/user/42 200
PUT /api/user/42 200
GET /reports/weekly 500
GET /reports/weekly 200
GET /reports/weekly 200
GET /reports/weekly 200
POST /upload 413
GET /health 200
GET /api/search?q=test 200
POST /api/search 400
GET /admin 403
GET /admin 200
PATCH /api/user/42 204
PATCH /api/user/42 204
PATCH /api/user/42 204
GET /metrics 200
POST /api/login 200
GET /unknown/path 404
```

```
Stack[000067F0]:000000000060FD00 db  66h ; f
Stack[000067F0]:000000000060FD01 db  6Ch ; l
Stack[000067F0]:000000000060FD02 db  61h ; a
Stack[000067F0]:000000000060FD03 db  67h ; g
Stack[000067F0]:000000000060FD04 db  7Bh ; {
Stack[000067F0]:000000000060FD05 db  30h ; 0
Stack[000067F0]:000000000060FD06 db  66h ; f
Stack[000067F0]:000000000060FD07 db  61h ; a
Stack[000067F0]:000000000060FD08 db  38h ; 8
Stack[000067F0]:000000000060FD09 db  33h ; 3
Stack[000067F0]:000000000060FD0A db  30h ; 0
Stack[000067F0]:000000000060FD0B db  65h ; e
Stack[000067F0]:000000000060FD0C db  37h ; 7
Stack[000067F0]:000000000060FD0D db  2Dh ; -
Stack[000067F0]:000000000060FD0E db  62h ; b
Stack[000067F0]:000000000060FD0F db  36h ; 6
Stack[000067F0]:000000000060FD10 db  39h ; 9
Stack[000067F0]:000000000060FD11 db  39h ; 9
Stack[000067F0]:000000000060FD12 db  2Dh ; -
Stack[000067F0]:000000000060FD13 db  34h ; 4
Stack[000067F0]:000000000060FD14 db  35h ; 5
Stack[000067F0]:000000000060FD15 db  31h ; 1
Stack[000067F0]:000000000060FD16 db  33h ; 3
Stack[000067F0]:000000000060FD17 db  2Dh ; -
Stack[000067F0]:000000000060FD18 db  38h ; 8
Stack[000067F0]:000000000060FD19 db  65h ; e
Stack[000067F0]:000000000060FD1A db  30h ; 0
Stack[000067F0]:000000000060FD1B db  31h ; 1
Stack[000067F0]:000000000060FD1C db  2Dh ; -
Stack[000067F0]:000000000060FD1D db  35h ; 5
Stack[000067F0]:000000000060FD1E db  31h ; 1
Stack[000067F0]:000000000060FD1F db  66h ; f
Stack[000067F0]:000000000060FD20 db  33h ; 3
Stack[000067F0]:000000000060FD21 db  35h ; 5
Stack[000067F0]:000000000060FD22 db  62h ; b
Stack[000067F0]:000000000060FD23 db  30h ; 0
Stack[000067F0]:000000000060FD24 db  66h ; f
Stack[000067F0]:000000000060FD25 db  33h ; 3
Stack[000067F0]:000000000060FD26 db  32h ; 2
Stack[000067F0]:000000000060FD27 db  39h ; 9
Stack[000067F0]:000000000060FD28 db  33h ; 3
Stack[000067F0]:000000000060FD29 db  7Dh ; }
```

```
0x66
0x6C
0x61
0x67
0x7B
0x30
0x66
0x61
0x38
0x33
0x30
0x65
0x37
0x2D
0x62
0x36
0x39
0x39
0x2D
0x34
0x35
0x31
0x33
0x2D
0x38
0x65
0x30
0x31
0x2D
0x35
0x31
0x66
0x33
0x35
0x62
0x30
0x66
0x33
0x32
0x39
0x33
0x7D
```

```
0x66 0x6C 0x61 0x67 0x7B 0x30 0x66 0x61 0x38 0x33 0x30 0x65 0x37 0x2D 0x62 0x36 0x39 0x39 0x2D 0x34 0x35 0x31 0x33 0x2D 0x38 0x65 0x30 0x31 0x2D 0x35 0x31 0x66 0x33 0x35 0x62 0x30 0x66 0x33 0x32 0x39 0x33 0x7D
```

```
666C61677B306661
```

```
aaa]bbb]ccc
```

```
[FW]firewall zone trust 
[FW-zone-trust]add interface g1/0/0
[FW-zone-trust]firewall zone untrust
[FW-zone-trust]add interface g1/0/1
[FW-zone-trust]quit
[FW]int g1/0/0
[FW-GigabitEthernet1/0/0]service-manage ping permit 
[FW-GigabitEthernet1/0/0]int g1/0/1
[FW-GigabitEthernet1/0/1]service-manage ping permit 
```

```
switch>enable #进入特权模式
switch#vlan data #进入VLAN配置模式
switch(vlan)#vlan 10 name IT #划分VLAN 10，名称为IT
switch(vlan)#vlan 20 name HR #划分VLAN20，名称为HR
switch(vlan)#vlan 30 name FIN #划分VLAN30，名称为FIN
switch(vlan)#vlan 40 name LOG #划分VLAN40，名称为LOG
switch(vlan)#exit
```

```
as9d8a7s6d!@#$$%^fg乱码zzxcv0912lkjhgfdqweoiuxxYYzz!!??__++==--随机文本混杂qwertyping??:://??192.168.3.45>>abcd*&^%$#@!乱码数据流>>>><<<>>>>><<><>0xDEADBEEFserver_log%%%%10.0.77.128###响应超时###hjkl;;''..,,//~~``混入字符流auth-fail@@!!172.16.9.200&&&retrying...$$$$$%%%%^^^^&&&&****((((随机噪声))))packet>>>><<<src=8.34.91.201>>>dst=??乱码??zzzzxxxxccccvvvvbbbbnnnnmmmm异常片段###@@@!!!~~~255.255.255.0掩码?kjsdhf9834yr9834y98r34y98r34数据尾部>>>>><<<<<>>>>乱码结束
```

```
{
  "timestamp": "2026-05-18T12:40:12Z",
  "service": "auth-gateway",
  "host": "node-01",
  "request": {
    "method": "GET",
    "path": "/api/user/42",
    "client_ip": "10.0.5.77",
    "user_agent": "curl/8.0"
  },
  "response": {
    "status": 200,
    "duration_ms": 34,
    "bytes": 1024
  },
  "user": {
    "id": "u_20421",
    "role": "user"
  },
  "flags": {
    "retry": false,
    "cached": true,
    "rate_limited": false
  },
  "meta": {
    "trace_id": "a1b2c3d4e5f60718",
    "env": "prod"
  }
}
{
  "timestamp": "2026-05-18T12:41:03Z",
  "service": "reporting",
  "host": "node-07",
  "request": {
    "method": "POST",
    "path": "/reports/weekly",
    "client_ip": "172.16.2.19",
    "user_agent": "Mozilla/5.0"
  },
  "response": {
    "status": 500,
    "duration_ms": 243,
    "bytes": 2048
  },
  "user": {
    "id": "u_88901",
    "role": "analyst"
  },
  "flags": {
    "retry": true,
    "cached": false,
    "rate_limited": false
  },
  "meta": {
    "trace_id": "b7c8d9e0f1a22334",
    "env": "staging"
  }
}
{
  "timestamp": "2026-05-18T12:42:27Z",
  "service": "file-service",
  "host": "node-05",
  "request": {
    "method": "PUT",
    "path": "/upload",
    "client_ip": "192.168.1.88",
    "user_agent": "PostmanRuntime/7.32"
  },
  "response": {
    "status": 413,
    "duration_ms": 12,
    "bytes": 128
  },
  "user": {
    "id": "u_55312",
    "role": "editor"
  },
  "flags": {
    "retry": false,
    "cached": false,
    "rate_limited": true
  },
  "meta": {
    "trace_id": "c3d4e5f6a7b89012",
    "env": "prod"
  }
}
{
  "timestamp": "2026-05-18T12:43:55Z",
  "service": "metrics",
  "host": "node-02",
  "request": {
    "method": "GET",
    "path": "/metrics",
    "client_ip": "8.34.91.201",
    "user_agent": "Prometheus/2.45"
  },
  "response": {
    "status": 200,
    "duration_ms": 5,
    "bytes": 4096
  },
  "user": {
    "id": "system",
    "role": "service"
  },
  "flags": {
    "retry": false,
    "cached": true,
    "rate_limited": false
  },
  "meta": {
    "trace_id": "d4e5f6a7b8c90123",
    "env": "prod"
  }
}
{
  "timestamp": "2026-05-18T12:45:10Z",
  "service": "admin-panel",
  "host": "node-09",
  "request": {
    "method": "DELETE",
    "path": "/api/user/77",
    "client_ip": "203.55.19.73",
    "user_agent": "Mozilla/5.0"
  },
  "response": {
    "status": 403,
    "duration_ms": 66,
    "bytes": 256
  },
  "user": {
    "id": "u_77777",
    "role": "guest"
  },
  "flags": {
    "retry": false,
    "cached": false,
    "rate_limited": false
  },
  "meta": {
    "trace_id": "e5f6a7b8c9d01234",
    "env": "prod"
  }
}
```

```
    method: GET
    method: POST
    method: PUT
    method: GET
    method: DELETE
```

```
a9F$kL2!zP0xvQ~mN##12asD http://alpha-node.example.com/api/v1/status ??xY7zz_19Qwe!!plm*(&^ https://secure-gateway.example.org/login RST%90100xAFeeLk__++==randomTEXT https://cdn.example.net/assets/img/logo.png @@!!~pP09__-==Nnmm,,..// http://intranet.local/dashboard?id=42 **(()))!LKJ09asdl!!@@##$$ https://updates.example.com/check?ver=1.2.3 &&&xyzqweZXCasd0987!!~~ http://logs.example.org/view/2026/05/18 :::???MN_bb77%%$$## https://auth.example.net/oauth2/authorize?client_id=abc123 ***trrPLK098__++ http://mirror.example.com/downloads/toolkit.zip -=-=-=-=YYuuii7788!!@@ https://status.example.org/healthcheck ###$$$noiseDATA___+++/// http://backup.example.net:8080/archive.tar.gz %%^^&&
```

```
hello world
https://example.com/test?a=1&b=2
```

