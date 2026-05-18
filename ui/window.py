from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QListWidget,
    QLabel, QLineEdit,QRadioButton, QButtonGroup,
    QCheckBox
)

from utils.file_io import save_text


class MainWindow(QWidget):
    def __init__(self, dispatcher):
        super().__init__()

        self.dispatcher = dispatcher

        self.setWindowTitle("StreamKnife by 帅成马")

        # ===== 参数框 =====
        self.param_box = QVBoxLayout()
        self.param_widget = QWidget()
        self.param_widget.setLayout(self.param_box)

        # ===== 输入输出 =====
        self.input_box = QTextEdit()
        self.output_box = QTextEdit()

        # ===== 分类 + 插件 =====
        self.category_list = QListWidget()
        self.plugin_list = QListWidget()

        # ===== 搜索框 =====
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索插件...")

        # ===== 按钮 =====
        self.run_btn = QPushButton("执行")
        self.save_btn = QPushButton("保存")


        # ===== 布局 =====
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.category_list)
        top_layout.addWidget(self.plugin_list)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("搜索"))
        layout.addWidget(self.search_box)
        layout.addLayout(top_layout)
        layout.addWidget(QLabel("参数配置"))
        layout.addWidget(self.param_widget)
        layout.addWidget(QLabel("输入"))
        layout.addWidget(self.input_box)
        layout.addWidget(self.run_btn)
        layout.addWidget(QLabel("输出"))
        layout.addWidget(self.output_box)
        layout.addWidget(self.save_btn)


        self.setLayout(layout)

        # ===== 绑定 =====
        self.run_btn.clicked.connect(self.run)
        self.save_btn.clicked.connect(self.save)
        self.search_box.textChanged.connect(self.filter_plugins)

    # 注入数据
    def set_functions(self, functions):
        self.functions = functions
        self.func_map = {}

        self.category_list.clear()
        self.plugin_list.clear()

        categories = set()

        for key, meta in functions.items():
            categories.add(meta["category"])

        for c in sorted(categories):
            self.category_list.addItem(c)

        self.category_list.itemClicked.connect(self.load_plugins)

        self.all_plugins = functions

    # 加载某分类插件
    def load_plugins(self, item):
        category = item.text()

        self.plugin_list.clear()
        self.func_map = {}

        for key, meta in self.all_plugins.items():
            if meta["category"] == category:
                self._add_plugin(key, meta)

    # 添加插件
    def _add_plugin(self, key, meta):
        self.func_map[meta["name"]] = key

        item = self.plugin_list.addItem(meta["name"])
        self.plugin_list.item(self.plugin_list.count() - 1).setToolTip(meta["desc"])

        # 点击插件时生成参数UI
        self.plugin_list.itemClicked.connect(self.render_params)

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

            elif item.layout():
                self.clear_layout(item.layout())

    def render_params(self, item):
        name = item.text()
        key = self.func_map[name]
        meta = self.all_plugins[key]

        self.clear_layout(self.param_box)
        self.param_values = {}

        for p in meta.get("meta", {}).get("params", []):

            label = QLabel(p["label"])
            self.param_box.addWidget(label)

            # ===== radio =====
            if p["type"] == "radio":
                group = QButtonGroup(self)
                hbox = QHBoxLayout()

                for opt in p["options"]:
                    rb = QRadioButton(opt)
                    hbox.addWidget(rb)
                    group.addButton(rb)

                self.param_box.addLayout(hbox)
                self.param_values[p["name"]] = group

            # ===== input =====
            elif p["type"] == "input":
                line = QLineEdit()
                self.param_box.addWidget(line)
                self.param_values[p["name"]] = line

            # ===== checkbox =====
            elif p["type"] == "checkbox":
                cb = QCheckBox(p["label"])
                cb.setChecked(p.get("default", False))
                self.param_box.addWidget(cb)
                self.param_values[p["name"]] = cb


    # 搜索过滤
    def filter_plugins(self, text):
        self.plugin_list.clear()
        self.func_map = {}

        for key, meta in self.all_plugins.items():

            if text.lower() in meta["name"].lower():

                self._add_plugin(key, meta)

    # 执行
    def run(self):
        data = self.input_box.toPlainText()

        selected = [i.text() for i in self.plugin_list.selectedItems()]
        keys = [self.func_map[name] for name in selected]

        config = {}

        for key in keys:
            meta = self.all_plugins[key]

            for p in meta.get("meta", {}).get("params", []):
                widget = self.param_values.get(p["name"])

                if not widget:
                    continue

                # radio
                if p["type"] == "radio":
                    for btn in widget.buttons():
                        if btn.isChecked():
                            config[p["name"]] = btn.text()

                # input
                elif p["type"] == "input":
                    config[p["name"]] = widget.text()

                # checkbox
                elif p["type"] == "checkbox":
                    config[p["name"]] = widget.isChecked()

        result = self.dispatcher.run(keys[0], data, config)
        self.output_box.setPlainText(result)

    # 保存
    def save(self):
        save_text("result.txt", self.output_box.toPlainText())