#empezar a crear smart notes 
from PyQt5.QtCore import Qt
from random import shuffle
from PyQt5.QtWidgets import QApplication,QListWidget,QInputDialog,QLineEdit, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton,QPushButton, QLabel, QButtonGroup,QTextEdit
import json


#lee los datos json 
def read_notes():
    global notes
    with open('datos.json','r',encoding='utf8')as file:
        notes =json.load(file)
        
def write_notes():
    with open('datos.json','w',encoding='utf8')as file:
        json.dump(notes,file)
init_json = False

if init_json:
    notes = {"bienvenido":{"texto":"aplicacion de notas","etiquetas":["eti1","instrucciones"]}}
    write_notes()
#crea la aplicacion
app=QApplication([]) 

my_win = QWidget()
my_win.setWindowTitle('smart notes')
my_win.resize(900,600)

#lineas
layout_notes = QHBoxLayout()
col_1= QVBoxLayout()
col_2= QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()
row4 = QHBoxLayout()

field_text=QTextEdit()

col_1.addWidget(field_text)

#crea botones
Button_note_create = QPushButton('crear')
Button_note_del = QPushButton('eliminar')
Button_note_save = QPushButton('guardar')

list_tags_label=QLabel('lista de notas')
list_tags_label2=QLabel('lista de etiquetas')

list_notes = QListWidget()
list_notes2 = QListWidget()

field_tag=QLineEdit('')
field_tag.setPlaceholderText('ingresar etiqueta')
#agrega las columnascon los botones y etiquetas
col_2.addWidget(list_tags_label)

col_2.addWidget(list_notes)
row1.addWidget(Button_note_create)
row1.addWidget(Button_note_del)
row2.addWidget(Button_note_save)

button_add=QPushButton('añadir etiqueta...')
Button_del = QPushButton('eliminar etiqueta')
button_search = QPushButton('buscar por etiqueta')
row3.addWidget(button_add)
row3.addWidget(Button_del)
row4.addWidget(button_search)

col_2.addLayout(row1)
col_2.addLayout(row2)
layout_notes.addLayout(col_1,stretch=2)
layout_notes.addLayout(col_2,stretch=1)
col_2.addWidget(list_tags_label2)
col_2.addWidget(list_notes2)
col_2.addWidget(field_tag)
col_2.addLayout(row3)
col_2.addLayout(row4)

my_win.setLayout(layout_notes)



#cargar el json
notes = {}
read_notes()
print(notes)
list_notes.addItems(notes)#carga los key en la lista de notas

def show_note():
    print('hola')
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        print(key)
        field_text.setText(notes[key]['texto'])
        #cargar etiquetas
        list_notes2.clear()
        list_notes2.addItems(notes[key]['etiquetas'])
        
def save_note():
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        text = field_text.toPlainText()
        notes[key]['texto']=text
        print(notes)
        write_notes()
def create_note():
    notes_name, result = QInputDialog.getText(
        my_win, 'añadir notas ', 'nombre de nota'
    )
    print(notes_name,'gay',result)
    if result and notes_name !="":
        notes[notes_name]={'texto':'','etiquetas':[]}
        list_notes.addItem(notes_name)
        print(notes)
        write_notes()
def del_note():
    print('hola')
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_notes.addItems(notes)
        field_tag.clear()
        print(notes)
        write_notes()
        
def add_tags():
    print('añadido')
    if list_notes.selectedItems():
        key=list_notes.selectedItems()[0].text()
        tag=field_tag.text()
        if not tag in notes[key]['etiquetas'] and tag!='':
            field_tag.clear()
            notes[key]['etiquetas'].append(tag)
            list_notes2.addItem(tag)
            write_notes()
            
def del_tags():
    print('borrado')
    if list_notes.selectedItems() and list_notes2.selectedItems():
        key=list_notes.selectedItems()[0].text()
        tag=list_notes2.selectedItems()[0].text()
        notes[key]['etiquetas'].remove(tag)
        list_notes2.clear()
        list_notes2.addItems(notes[key]['etiquetas'])
        write_notes()
        
def search_tag():
    print(button_search)
    tag = field_tag.text()
    if button_search.text() == "Buscar por etiqueta" and tag != '':
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["etiquetas"]:
                notes_filtered[note]=notes[note]
            button_search.setText("Restablecer búsqueda")
            list_notes.clear()
            list_notes.clear()
            list_notes.addItems(notes_filtered)
    elif button_search.text() == "Restablecer búsqueda":
        field_tag.clear()
        list_notes.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        button_search.setText("Buscar por etiqueta")
        
    
          
#funciones eventos click
list_notes.itemClicked.connect(show_note)
Button_note_save.clicked.connect(save_note)
Button_note_create.clicked.connect(create_note)
Button_note_del.clicked.connect(del_note)

#tags
button_add.clicked.connect(add_tags)
Button_del.clicked.connect(del_tags)
button_search.clicked.connect(search_tag)

my_win.show()

app.exec()