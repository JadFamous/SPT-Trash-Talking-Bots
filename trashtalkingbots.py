import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QTextEdit, QTabWidget, QWidget, QLabel, QLineEdit, QMenuBar, QAction, QStyleFactory, QMenu
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from datetime import datetime

class JsonFileReader(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the theme preference from settings or default to Light Theme
        self.theme_preference = self.load_theme_preference()

        self.version = "beta 0.0.1"

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Trash Talk PMCs')
        self.setGeometry(100, 100, 800, 600)

        self.create_menu_bar()  # Create the menu bar

        # Create the main container layout
        main_layout = QVBoxLayout(self)

        # Open File button moved to the Settings menu
        self.open_action = QAction('Open File', self)
        self.open_action.triggered.connect(self.open_file)
        self.settings_menu.addAction(self.open_action)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.text_edit = QTextEdit(self)
        self.tabs.addTab(self.text_edit, 'File Content')

        self.victim_tab = QWidget()
        self.victim_layout = QVBoxLayout(self.victim_tab)

        self.tabs.addTab(self.victim_tab, 'You kill NPC PMC')

        # PMC Victim Description label
        self.pmc_victim_description_label = QLabel("Description: These values are for how the NPC PMC responds to you killing them")
        self.victim_layout.addWidget(self.pmc_victim_description_label)

        # Response chance label with tooltip
        self.response_chance_label = QLabel("Response chance %: ")
        self.response_chance_label.setToolTip("<i> % Chance that the PMC that you killed will send you an in-game message <i>")
        self.response_chance_edit = QLineEdit(self)
        self.victim_layout.addWidget(self.response_chance_label)
        self.victim_layout.addWidget(self.response_chance_edit)

        # Other labels and edits
        self.positive_label = QLabel("Positive response %: ")
        self.positive_label.setToolTip("<i> % Chance that the message the PMC you killed will be a positive message <i>")
        self.positive_edit = QLineEdit(self)
        self.victim_layout.addWidget(self.positive_label)
        self.victim_layout.addWidget(self.positive_edit)

        self.negative_label = QLabel("Negative response %: ")
        self.negative_label.setToolTip("<i> % Chance that the message the PMC you killed will be a negative message <i>")
        self.negative_edit = QLineEdit(self)
        self.victim_layout.addWidget(self.negative_label)
        self.victim_layout.addWidget(self.negative_edit)

        self.plead_label = QLabel("Pleading response %: ")
        self.plead_label.setToolTip("<i> % Chance that the message the PMC you killed will be a pleading message <i>")
        self.plead_edit = QLineEdit(self)
        self.victim_layout.addWidget(self.plead_label)
        self.victim_layout.addWidget(self.plead_edit)

        self.strip_cap_label = QLabel("No capitalization chance %: ")
        self.strip_cap_label.setToolTip("<i> % chance that the message that the PMC you killed sends you will have no capitalization <i>")
        self.strip_cap_edit = QLineEdit(self)
        self.victim_layout.addWidget(self.strip_cap_label)
        self.victim_layout.addWidget(self.strip_cap_edit)

        self.all_caps_label = QLabel("MESSAGE IS IN ALL CAPS CHANCE %: ")
        self.all_caps_label.setToolTip("<i> % CHANCE THAT THE MESSAGE THAT THE PMC YOU KILLED SENDS YOU WILL HAVE ALL CAPITALIZATION <i>")
        self.all_caps_edit = QLineEdit(self)
        self.victim_layout.addWidget(self.all_caps_label)
        self.victim_layout.addWidget(self.all_caps_edit)

        self.append_bro_label = QLabel("Append 'bro' to end of message chance %: ")
        self.append_bro_label.setToolTip("<i> % Chance that the message that the PMC you killed sends you will have a bro at the end of the message bro <i>")
        self.append_bro_edit = QLineEdit(self)
        self.victim_layout.addWidget(self.append_bro_label)
        self.victim_layout.addWidget(self.append_bro_edit)

        self.save_button = QPushButton('Save Changes', self)
        self.save_button.clicked.connect(self.save_changes)
        self.victim_layout.addWidget(self.save_button)

        # PMC is Killer tab
        self.killer_tab = QWidget()
        self.killer_layout = QVBoxLayout(self.killer_tab)

        self.tabs.addTab(self.killer_tab, 'NPC PMC kills You')

        # PMC Killer Description label
        self.pmc_killer_description_label = QLabel("Description: These values are for how the NPC PMC responds to killing you")
        self.killer_layout.addWidget(self.pmc_killer_description_label)

        # Response chance label for PMC is Killer
        self.response_chance_killer_label = QLabel("Response chance %: ")
        self.response_chance_killer_label.setToolTip("<i> % Chance that the PMC that killed you will send you an in-game message <i>")
        self.killer_layout.addWidget(self.response_chance_killer_label)
        self.response_chance_killer_edit = QLineEdit(self)
        self.killer_layout.addWidget(self.response_chance_killer_edit)

        # Other labels and edits for PMC is Killer
        self.positive_killer_label = QLabel("Positive response %: ")
        self.positive_killer_label.setToolTip("<i> % Chance that the message from the PMC that killed you will be positive <i>")
        self.killer_layout.addWidget(self.positive_killer_label)
        self.positive_killer_edit = QLineEdit(self)
        self.killer_layout.addWidget(self.positive_killer_edit)

        self.negative_killer_label = QLabel("Negative response %: ")
        self.negative_killer_label.setToolTip("<i> % Chance that the message from the PMC that killed you will be negative <i>")
        self.killer_layout.addWidget(self.negative_killer_label)
        self.negative_killer_edit = QLineEdit(self)
        self.killer_layout.addWidget(self.negative_killer_edit)

        self.plead_killer_label = QLabel("Toxic response %: ")
        self.plead_killer_label.setToolTip("<i> % Chance that the message from the PMC that killed you will be toxic <i>")
        self.killer_layout.addWidget(self.plead_killer_label)
        self.plead_killer_edit = QLineEdit(self)
        self.killer_layout.addWidget(self.plead_killer_edit)

        self.strip_cap_killer_label = QLabel("No capitalization chance %: ")
        self.strip_cap_killer_label.setToolTip("<i> % chance that the message from the PMC that killed you will be in all lowercase <i>")
        self.killer_layout.addWidget(self.strip_cap_killer_label)
        self.strip_cap_killer_edit = QLineEdit(self)
        self.killer_layout.addWidget(self.strip_cap_killer_edit)

        self.all_caps_killer_label = QLabel("MESSAGE IS IN ALL CAPS CHANCE %: ")
        self.all_caps_killer_label.setToolTip("<i> % CHANCE THAT THE MESSAGE FROM THE PMC THAT KILLED YOU WILL BE IN ALL CAPS <i>")
        self.killer_layout.addWidget(self.all_caps_killer_label)
        self.all_caps_killer_edit = QLineEdit(self)
        self.killer_layout.addWidget(self.all_caps_killer_edit)

        self.append_bro_killer_label = QLabel("Append 'bro' to end of message chance %: ")
        self.append_bro_killer_label.setToolTip("<i> % Chance message from the PMC that killed you will have bro added to the end of the message bro <i>")
        self.killer_layout.addWidget(self.append_bro_killer_label)
        self.append_bro_killer_edit = QLineEdit(self)
        self.killer_layout.addWidget(self.append_bro_killer_edit)

        self.save_button_killer = QPushButton('Save Changes', self)
        self.save_button_killer.clicked.connect(self.save_changes_killer)
        self.killer_layout.addWidget(self.save_button_killer)

        # Restore Defaults tab
        self.restore_defaults_tab = QWidget()
        self.restore_defaults_layout = QVBoxLayout(self.restore_defaults_tab)

        self.tabs.addTab(self.restore_defaults_tab, 'Restore Defaults')

        # Restore Defaults button
        self.restore_defaults_button = QPushButton('Restore original pmcchatresponse.json file', self)
        self.restore_defaults_button.clicked.connect(self.restore_defaults)
        self.restore_defaults_layout.addWidget(self.restore_defaults_button)

        if not self.layout():
            central_widget = QWidget()
            central_widget.setLayout(main_layout)
            self.setCentralWidget(central_widget)

        # Apply the theme preference
        self.apply_theme()

    def create_menu_bar(self):
        # Create Settings menu and menu bar
        self.menu_bar = self.menuBar()
        self.settings_menu = self.menu_bar.addMenu('Settings')

        # Settings Menu button
        self.settings_action = QAction('Settings', self)  # Create QAction
        self.settings_action.triggered.connect(self.show_settings_menu)
        self.settings_menu.addAction(self.settings_action)  # Add QAction to menu

        # Create Themes menu
        self.themes_menu = QMenu('Themes', self)

        # Light Theme option
        self.light_theme_action = QAction('Light Theme', self)
        self.light_theme_action.triggered.connect(self.set_light_theme)
        self.themes_menu.addAction(self.light_theme_action)

        # Dark Theme option
        self.dark_theme_action = QAction('Dark Theme', self)
        self.dark_theme_action.triggered.connect(self.set_dark_theme)
        self.themes_menu.addAction(self.dark_theme_action)

        # Add Themes menu to the menu bar
        self.menu_bar.addMenu(self.themes_menu)

        # Create Version menu
        self.create_version_menu()

    def create_version_menu(self):
        version_action = QAction(f'Version: {self.version}', self)
        version_action.setEnabled(False)  # Disable the version menu item
        self.menu_bar.addAction(version_action)

    def set_light_theme(self):
        self.theme_preference = 'Light'
        self.save_theme_preference()
        self.apply_theme()

    def set_dark_theme(self):
        self.theme_preference = 'Dark'
        self.save_theme_preference()
        self.apply_theme()

    def apply_theme(self):
        if self.theme_preference == 'Dark':
            self.set_theme(QStyleFactory.create('Fusion'))
            self.setStyleSheet("QMainWindow { background-color: #2E2E2E; color: #FFFFFF; }")
            self.text_edit.setStyleSheet("QTextEdit { background-color: #424242; color: #FFFFFF; }")
        else:
            self.set_theme(QStyleFactory.create('Windows'))
            self.setStyleSheet("")
            self.text_edit.setStyleSheet("")

    def set_theme(self, style):
        QApplication.setStyle(style)
        self.changePalette()

    def changePalette(self):
        palette = QPalette()
        if self.theme_preference == 'Dark':
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
        else:
            palette.setColor(QPalette.Window, QColor(255, 255, 255))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, QColor(240, 240, 240))
            palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(255, 255, 255))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(0, 122, 204))
            palette.setColor(QPalette.Highlight, QColor(0, 122, 204))
            palette.setColor(QPalette.HighlightedText, Qt.white)

        QApplication.setPalette(palette)

    def save_theme_preference(self):
        # Save the theme preference to a file or a settings mechanism of your choice
        with open("theme_preference.txt", "w") as f:
            f.write(self.theme_preference)

    def load_theme_preference(self):
        # Load the theme preference from a file or a settings mechanism of your choice
        try:
            with open("theme_preference.txt", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return 'Light'

    def show_settings_menu(self):
        # Show the settings menu when the Settings button is clicked
        self.settings_menu.exec_(self.menu_bar.mapToGlobal(self.settings_menu.actionGeometry(self.settings_action).bottomLeft()))

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        self.file_path, _ = QFileDialog.getOpenFileName(self, 'Open JSON File', '', 'JSON files (*.json);;All Files (*)', options=options)

        if self.file_path:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                formatted_data = json.dumps(data, indent=4)

                self.text_edit.clear()
                self.text_edit.insertPlainText(formatted_data)

                if "victim" in data:
                    victim_data = data["victim"]

                    self.response_chance_edit.setText(str(victim_data.get('responseChancePercent', '')))
                    self.positive_edit.setText(str(victim_data.get('responseTypeWeights', {}).get('positive', '')))
                    self.negative_edit.setText(str(victim_data.get('responseTypeWeights', {}).get('negative', '')))
                    self.plead_edit.setText(str(victim_data.get('responseTypeWeights', {}).get('plead', '')))

                    self.strip_cap_edit.setText(str(victim_data.get('stripCapitalisationChancePercent', '')))
                    self.all_caps_edit.setText(str(victim_data.get('allCapsChancePercent', '')))
                    self.append_bro_edit.setText(str(victim_data.get('appendBroToMessageEndChancePercent', '')))

                if "killer" in data:
                    killer_data = data["killer"]

                    self.response_chance_killer_edit.setText(str(killer_data.get('responseChancePercent', '')))
                    self.positive_killer_edit.setText(str(killer_data.get('responseTypeWeights', {}).get('positive', '')))
                    self.negative_killer_edit.setText(str(killer_data.get('responseTypeWeights', {}).get('negative', '')))
                    self.plead_killer_edit.setText(str(killer_data.get('responseTypeWeights', {}).get('plead', '')))

                    self.strip_cap_killer_edit.setText(str(killer_data.get('stripCapitalisationChancePercent', '')))
                    self.all_caps_killer_edit.setText(str(killer_data.get('allCapsChancePercent', '')))
                    self.append_bro_killer_edit.setText(str(killer_data.get('appendBroToMessageEndChancePercent', '')))

    def save_changes(self):
        # Update values in the JSON data structure
        if hasattr(self, 'response_chance_edit'):
            response_chance_value = int(self.response_chance_edit.text()) if self.response_chance_edit.text().isdigit() else None
            positive_value = int(self.positive_edit.text()) if self.positive_edit.text().isdigit() else None
            negative_value = int(self.negative_edit.text()) if self.negative_edit.text().isdigit() else None
            plead_value = int(self.plead_edit.text()) if self.plead_edit.text().isdigit() else None
            strip_cap_value = int(self.strip_cap_edit.text()) if self.strip_cap_edit.text().isdigit() else None
            all_caps_value = int(self.all_caps_edit.text()) if self.all_caps_edit.text().isdigit() else None
            append_bro_value = int(self.append_bro_edit.text()) if self.append_bro_edit.text().isdigit() else None

            # Open original file and load data
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            # Backup original file
            backup_filename = f"pmcchatresponse_OLD{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_filepath = os.path.join(os.path.dirname(self.file_path), backup_filename)
            os.rename(self.file_path, backup_filepath)

            # Update data with new values
            if 'victim' not in data:
                data['victim'] = {}

            data['victim']['responseChancePercent'] = response_chance_value
            data['victim']['responseTypeWeights'] = {
                'positive': positive_value,
                'negative': negative_value,
                'plead': plead_value
            }
            data['victim']['stripCapitalisationChancePercent'] = strip_cap_value
            data['victim']['allCapsChancePercent'] = all_caps_value
            data['victim']['appendBroToMessageEndChancePercent'] = append_bro_value

            # Save changes to the new file
            new_filename = "pmcchatresponse.json"
            new_filepath = os.path.join(os.path.dirname(self.file_path), new_filename)
            with open(new_filepath, 'w') as file:
                json.dump(data, file, indent=4)

            self.open_file()  # Refresh the displayed content

    def save_changes_killer(self):
        # Update values in the JSON data structure for PMC is Killer
        if hasattr(self, 'response_chance_killer_edit'):
            response_chance_killer_value = int(self.response_chance_killer_edit.text()) if self.response_chance_killer_edit.text().isdigit() else None
            positive_killer_value = int(self.positive_killer_edit.text()) if self.positive_killer_edit.text().isdigit() else None
            negative_killer_value = int(self.negative_killer_edit.text()) if self.negative_killer_edit.text().isdigit() else None
            plead_killer_value = int(self.plead_killer_edit.text()) if self.plead_killer_edit.text().isdigit() else None
            strip_cap_killer_value = int(self.strip_cap_killer_edit.text()) if self.strip_cap_killer_edit.text().isdigit() else None
            all_caps_killer_value = int(self.all_caps_killer_edit.text()) if self.all_caps_killer_edit.text().isdigit() else None
            append_bro_killer_value = int(self.append_bro_killer_edit.text()) if self.append_bro_killer_edit.text().isdigit() else None

            # Open original file and load data
            with open(self.file_path, 'r') as file:
                data = json.load(file)

            # Backup original file
            backup_filename = f"pmcchatresponse_OLD{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            backup_filepath = os.path.join(os.path.dirname(self.file_path), backup_filename)
            os.rename(self.file_path, backup_filepath)

            # Update data with new values
            if 'killer' not in data:
                data['killer'] = {}

            data['killer']['responseChancePercent'] = response_chance_killer_value
            data['killer']['responseTypeWeights'] = {
                'positive': positive_killer_value,
                'negative': negative_killer_value,
                'plead': plead_killer_value
            }
            data['killer']['stripCapitalisationChancePercent'] = strip_cap_killer_value
            data['killer']['allCapsChancePercent'] = all_caps_killer_value
            data['killer']['appendBroToMessageEndChancePercent'] = append_bro_killer_value

            # Save changes to the new file
            new_filename = "pmcchatresponse.json"
            new_filepath = os.path.join(os.path.dirname(self.file_path), new_filename)
            with open(new_filepath, 'w') as file:
                json.dump(data, file, indent=4)

            self.open_file()  # Refresh the displayed content

    def restore_defaults(self):
        if not self.file_path:
            return  # No file opened, nothing to restore

        # Create default data
        default_data = {
            "victim": {
                "responseChancePercent": 50,
                "responseTypeWeights": {
                    "positive": 7,
                    "negative": 2,
                    "plead": 2
                },
                "stripCapitalisationChancePercent": 20,
                "allCapsChancePercent": 20,
                "appendBroToMessageEndChancePercent": 35
            },
            "killer": {
                "responseChancePercent": 50,
                "responseTypeWeights": {
                    "positive": 5,
                    "negative": 2,
                    "plead": 2
                },
                "stripCapitalisationChancePercent": 20,
                "allCapsChancePercent": 15,
                "appendBroToMessageEndChancePercent": 15
            }
        }

        # Save default data to the new file
        new_filename = "pmcchatresponse.json"
        new_filepath = os.path.join(os.path.dirname(self.file_path), new_filename)
        with open(new_filepath, 'w') as file:
            json.dump(default_data, file, indent=4)

        # Switch back to the "File Content" tab
        self.tabs.setCurrentIndex(0)
        self.open_file()  # Refresh the displayed content

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JsonFileReader()
    window.setWindowTitle('Trash Talk PMCs')
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
