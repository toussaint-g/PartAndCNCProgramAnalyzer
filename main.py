
# -*- coding: utf-8 -*-

# Librairie standard
from pathlib import Path
from datetime import datetime
import tkinter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkbootstrap import Style
import ttkbootstrap as tb 
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# Modules internes
from interpreter import Interpreter
from writer import Writer
from machine import Machine
from tool_path_viewer import ToolPathViewer
from tool_path_viewer_config_loader import ToolPathConfigLoader


# Fonction sélection de fichier
def file_select(file_type, file_ext, label, update_calculate_button):
    """ Fonction de sélection de fichier """
    file = tkinter.filedialog.askopenfilename(title="Sélectionner un fichier", filetypes=[(file_type, file_ext)])
    if file:
        label.config(text=file)
        update_calculate_button()  # Met à jour l'état du bouton "Calculer"

# Fonction sélection de dossier
def folder_select(label):
    """ Fonction de sélection de dossier """
    folder = tkinter.filedialog.askdirectory(title="Sélectionner un dossier")
    if folder:
        label.config(text=folder)

# Fonction pour nom de fichier à la date et heure du jour
def get_datetime_string():
    """Retourne la date et l'heure sous la forme YYYY-MM-DD_HH-MM-SS"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Fonction traitement G-Code
def gcode_treatment(path_gcode_file, path_export_file):

    # Charge les données de la machine
    Machine.load_config() 

    # Instanciation des classes
    obj_interpreter = Interpreter() 
    obj_writer = Writer()

    list_datas = obj_interpreter.analyze(path_gcode_file) # Récup data
    obj_writer.write_report(Path(path_export_file).with_suffix(".txt"), path_gcode_file, list_datas) # Création du rapport
    obj_writer.write_debug_file(Path(path_export_file).with_suffix(".debug"), path_gcode_file, list_datas) # Création du fichier debug

    display_results(path_export_file)

def display_results(path_export_file):
    '''Affiche la fenêtre avec le résultat de l'analyse du G Code'''

    result_window = tk.Toplevel()
    result_window.title("Part Program Analyzer: Résultat")
    result_window.state('zoomed')

    result_frame = tk.Frame(result_window)
    result_frame.pack(fill="both", expand=True, padx=10, pady=10)

    result_label = tk.Label(result_frame, text="Résultat :", font=("Segoe UI", 18, "bold"))
    result_label.pack(pady=10, anchor="w")

    # Rapport
    result_text_frame = tk.Frame(result_frame)
    result_text_frame.pack(padx=10, pady=5, fill="both", expand=True)
    result_text = tk.Text(result_text_frame, height=10, width=70, font=("Segoe UI", 12))
    result_scrollbar = tk.Scrollbar(result_text_frame, command=result_text.yview)
    result_text.config(yscrollcommand=result_scrollbar.set)
    result_text.pack(side="left", fill="both", expand=True)
    result_scrollbar.pack(side="right", fill="y")

    try:
        with open(path_export_file.with_suffix(".txt"), 'r') as file:
            result_text.insert(tk.END, file.read())
    except Exception as e:
        result_text.insert(tk.END, f"Erreur lors de la lecture du fichier : {e}")
    result_text.config(state=tk.DISABLED)

    # Debug
    separator = tk.Label(result_frame, text="Debug :", font=("Segoe UI", 18, "bold"))
    separator.pack(pady=5, anchor="w")

    debug_text_frame = tk.Frame(result_frame)
    debug_text_frame.pack(padx=10, pady=5, fill="both", expand=True)
    debug_text = tk.Text(debug_text_frame, height=10, width=70, font=("Courier", 7))
    debug_scrollbar = tk.Scrollbar(debug_text_frame, command=debug_text.yview)
    debug_text.config(yscrollcommand=debug_scrollbar.set)
    debug_text.pack(side="left", fill="both", expand=True)
    debug_scrollbar.pack(side="right", fill="y")

    try:
        with open(path_export_file.with_suffix(".debug"), 'r') as file:
            debug_text.insert(tk.END, file.read())
    except Exception as e:
        debug_text.insert(tk.END, f"Erreur lors de la lecture du fichier : {e}")
    debug_text.config(state=tk.DISABLED)

# Fonction traitement G-Code
def viewer_launch(path_gcode_file,stl_path_file):

    # Charge les config
    Machine.load_config() 
    ToolPathConfigLoader.load_config() 

    # Instanciation des classes
    obj_interpreter = Interpreter() 
    obj_toolpathviewer = ToolPathViewer()

    # Récup datas g-code
    list_datas = obj_interpreter.analyze(path_gcode_file)

    # Start viewer
    obj_toolpathviewer.open_viewer(stl_path_file, list_datas)

# Point d'entrée app
def main():
    """Point d'entrée de l'application"""

    style = Style(theme="darkly") 

    # Création form avec nom & dimension
    form = style.master
    form.title("Part Program Analyzer")
    form.state('zoomed')

    # Frame principale
    main_frame = tb.Frame(form, padding=20)
    main_frame.pack(expand=True, fill="both")

    # Logo
    logo_icon = Image.open("img/logo.png")  # Charge le logo
    logo_icon = logo_icon.resize((32, 32))
    logo_icon_tk = ImageTk.PhotoImage(logo_icon) # Conversion image en format Tkinter

    # Appliquer l'icône à la fenêtre
    form.iconphoto(True, logo_icon_tk)

    # Titre
    tb.Label(
        main_frame,
        text="Part Program Analyzer",
        font=("Segoe UI", 30, "bold"),
        bootstyle="dark",
        foreground="white"
    ).grid(column=0, row=0, columnspan=1, pady=(0, 30))

    # G-Code section
    tb.Label(main_frame, text="📂 Fichier G-Code :", font=("Segoe UI", 18)).grid(column=0, row=1, sticky="w", pady=5)
    label_gcode = tb.Label(main_frame, text="", width=50, bootstyle="secondary")
    label_gcode.grid(column=0, row=2, sticky="w")
    tb.Button(main_frame, text="Ouvrir", bootstyle="primary", command=lambda: file_select("Fichier G-Code", "*.anc;*.nc;*.txt", label_gcode, update_calculate_button)).grid(column=0, row=3, sticky="w", pady=5)

    tb.Label(main_frame, text="📁 Dossier de sortie :", font=("Segoe UI", 18)).grid(column=0, row=4, sticky="w", pady=(20, 5))
    label_output = tb.Label(main_frame, text=os.getenv('TEMP'), width=50, bootstyle="secondary")
    label_output.grid(column=0, row=5, sticky="w")
    tb.Button(main_frame, text="Choisir", bootstyle="primary", command=lambda: folder_select(label_output)).grid(column=0, row=6, sticky="w", pady=5)

    # Ligne vide
    tb.Label(main_frame, text="", font=("Segoe UI", 12)).grid(column=0, row=7, sticky="w", pady=(5, 60))

    # Fonction local pour désactiver les boutons tant que le G-Code n'est pas chargé
    def update_calculate_button():
        if label_gcode.cget("text"):  # Vérifier si un fichier G-code est sélectionné
            calculate_button.config(state="normal")  # Activer le bouton "Calculer"
            visualize_button.config(state="normal")  # Activer le bouton "Visualiser"
        else:
            calculate_button.config(state="disabled")  # Désactiver le bouton "Calculer"
            visualize_button.config(state="disabled")  # Désactiver le bouton "Visualiser"

    tb.Label(main_frame, text="⏱️ Calcul des données :", font=("Segoe UI", 18)).grid(column=0, row=8, sticky="w", pady=(20, 5))    
    
    # Bouton Calculer
    calculate_button = tb.Button(main_frame, text="Calculer", bootstyle="success", command=lambda: gcode_treatment(
        label_gcode.cget("text"),
        Path(label_output.cget("text")) / get_datetime_string()))
    calculate_button.grid(column=0, row=9, sticky="w", pady=5)
    calculate_button.config(state="disabled")  # Désactiver au début

    # STL section
    tb.Label(main_frame, text="📂 Fichier STL :", font=("Segoe UI", 18)).grid(column=1, row=1, sticky="w", padx=(40, 0), pady=5)
    label_stl = tb.Label(main_frame, text="", width=50, bootstyle="secondary")
    label_stl.grid(column=1, row=2, sticky="w", padx=(40, 0))
    tb.Button(main_frame, text="Ouvrir", bootstyle="primary", command=lambda: file_select("Fichier STL", "*.stl", label_stl, update_calculate_button)).grid(column=1, row=3, sticky="w", padx=(40, 0), pady=5)

    # Ligne vide
    tb.Label(main_frame, text="", font=("Segoe UI", 12)).grid(column=0, row=7, sticky="w", pady=(5, 60))

    tb.Label(main_frame, text="🎥 Visualiser les trajectoires :", font=("Segoe UI", 18)).grid(column=1, row=8, sticky="w", padx=(40, 0), pady=(20, 5))
    
    # Bouton Visualiser
    visualize_button = tb.Button(main_frame, text="Visualiser", bootstyle="success", command=lambda: viewer_launch(
        label_gcode.cget("text"), 
        label_stl.cget("text")))
    visualize_button.grid(column=1, row=9, sticky="w", padx=(40, 0), pady=5)
    visualize_button.config(state="disabled")  # Désactiver au début

    form.mainloop()

if __name__ == "__main__":
    main()

    



    
    
