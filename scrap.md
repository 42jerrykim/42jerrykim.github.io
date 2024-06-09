https://comsmart.co.kr/cmart/shop/item.php?it_id=1644305465&num=19&ca_id2=
[https://plantuml.com/ko/link#google_vignette](https://plantuml.com/ko/link)

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from plantuml import PlantUML

class PlantUMLApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('PlantUML Sequence Diagram Generator')
        
        self.layout = QVBoxLayout()
        
        self.textEdit = QTextEdit(self)
        self.layout.addWidget(self.textEdit)
        
        self.generateButton = QPushButton('Generate Diagram', self)
        self.generateButton.clicked.connect(self.generate_diagram)
        self.layout.addWidget(self.generateButton)
        
        self.imageLabel = QLabel(self)
        self.layout.addWidget(self.imageLabel)
        
        self.setLayout(self.layout)
        self.show()
        
    def generate_diagram(self):
        plantuml_text = self.textEdit.toPlainText()
        
        # Save the PlantUML text to a temporary file
        temp_file = 'temp_diagram.puml'
        with open(temp_file, 'w') as file:
            file.write(plantuml_text)
        
        # Generate the diagram using PlantUML
        plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
        diagram_file = 'diagram.png'
        plantuml.processes_file(temp_file, outfile=diagram_file)
        
        # Display the diagram
        pixmap = QPixmap(diagram_file)
        self.imageLabel.setPixmap(pixmap)
        
        # Clean up the temporary file
        os.remove(temp_file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlantUMLApp()
    sys.exit(app.exec_())


buffalo_l
min detection score  0.5
max recog distance 0.3
min recog faces: 2
