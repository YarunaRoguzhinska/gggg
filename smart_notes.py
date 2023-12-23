from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget, QInputDialog
import json
app = QApplication([])
window = QWidget()
window.setWindowTitle('Розумні замітки')
window.move(600,300)
window.resize(900, 600)

notes = {
    "Ласкаво просимо!" : {
        "текст" : "Це найкращий додаток для заміток у світі!",
        "теги" : ["добро", "інструкція"]
    }
}
with open("notes_data.json", "w") as file:
    json.dump(notes,file)


text = QTextEdit()
text.setText("Додаток")
line_main = QHBoxLayout()
notes1 = QLabel("Список заміток")
notes2 = QLabel("Список тегів")

lineV1 = QVBoxLayout()
lineV2 = QVBoxLayout()
lineH1 = QHBoxLayout()
lineH2 = QHBoxLayout()

but1 = QPushButton("Створити замітку")
but2 = QPushButton("Видалити замітку")
but3 = QPushButton("Зберегти замітку")
but4 = QPushButton("Додати до замітки")
but5 = QPushButton("Відкріпити від замітки")
but6 = QPushButton("Шукати замітки за тегом")

items1 = QListWidget()
items2 = QListWidget()
line = QLineEdit()
line.setPlaceholderText("Введіть тег...")

lineV1.addWidget(text)
lineH1.addWidget(but1)
lineH1.addWidget(but2)
lineH2.addWidget(but4)
lineH2.addWidget(but5)

lineV2.addWidget(notes1)
lineV2.addWidget(items1)
lineV2.addLayout(lineH1)
lineV2.addWidget(but3)
lineV2.addWidget(notes2)
lineV2.addWidget(items2)
lineV2.addWidget(line)
lineV2.addLayout(lineH2)
lineV2.addWidget(but6)

line_main.addLayout(lineV1, stretch=2)
line_main.addLayout(lineV2, stretch=1)
window.setLayout(line_main)

def add_note():
    note_name, ok = QInputDialog.getText(window, "Додати замітку", "Назва замітки: ")
    if ok and note_name != "":
        notes[note_name] = {"текст" : "", "теги" : []}
        items1.addItem(note_name)
        items2.addItems(notes[note_name]["теги"])
        print(notes)

def show_note():
    key = items1.selectedItems()[0].text()
    print(key)
    text.setText(notes[key]["текст"])
    items2.clear()
    items2.addItems(notes[key]["теги"])

def save_note():
    if items1.selectedItems():
        key = items1.selectedItems()[0].text()
        notes[key]["текст"] = text.toPlainText()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для збереження не вибрана!")

def del_note():
    if items1.selectedItems():
        key = items1.selectedItems()[0].text()
        del notes[key]
        items1.clear()
        items2.clear()
        text.clear()
        items1.addItems(notes)
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Замітка для збереження не вибрана!")
def add_tag():
    if items1.selectedItems():
        key = items1.selectedItems()[0].text()
        tag = line.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            items2.addItem(tag)
            line.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("замітка для додавання тега не обрана!")
def del_tag():
    if items2.selectedItems():
        key = items1.selectedItems()[0].text()
        tag = items2.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        items2.clear()
        items2.addItems(notes[key]["теги"])
        with open("notes_data.json", "w") as file:
            json.dump(notes,file, sort_keys=True, ensure_ascii=False)
    else:
        print("Тег для вилучення не обраний!")
def search_tag():
    print(but6.text())
    tag = line.text()
    if but6.text() == "Шукати замітки за тегом" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note]=notes[note]
        but6.setText("Скинути пошук")
        items1.clear()
        items2.clear()
        items1.addItems(notes_filtered)
        print(but6.text())
    elif but6.text() == "Скинути пошук":
        line.clear()
        items1.clear()
        items2.clear()
        items1.addItems(notes)
        but6.setText("Шукати замітки за тегом")
        print(but6.text())
    else:
        pass


but1.clicked.connect(add_note)
items1.itemClicked.connect(show_note)
but2.clicked.connect(del_note)
but3.clicked.connect(save_note)
but4.clicked.connect(add_tag)
but5.clicked.connect(del_tag)
but6.clicked.connect(search_tag)
window.show()
with open("notes_data.json", "r") as file:
    notes = json.load(file)
items1.addItems(notes)
app.exec_()