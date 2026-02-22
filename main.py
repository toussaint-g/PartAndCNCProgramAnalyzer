
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
from machines_config_loader import MachinesConfigLoader
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
def gcode_treatment(path_gcode_file, path_export_file, machine_name):










    MachinesConfigLoader.load_config()



    machine_config = MachinesConfigLoader.get_machine(machine_name)











    # Instanciation des classes
    obj_interpreter = Interpreter(machine_config) 
    obj_writer = Writer(machine_config)

    list_datas = obj_interpreter.analyze(path_gcode_file) # Récup data
    obj_writer.write_report(Path(path_export_file).with_suffix(".txt"), path_gcode_file, list_datas) # Création du rapport
    obj_writer.write_debug_file(Path(path_export_file).with_suffix(".debug"), path_gcode_file, list_datas) # Création du fichier debug

    display_results(path_export_file)

def display_results(path_export_file):
    '''Affiche la fenêtre avec le résultat de l'analyse du G Code'''

    result_window = tk.Toplevel()
    result_window.title("PartAndCNCProgramAnalyzer: Résultat")
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
def viewer_launch(path_gcode_file, stl_path_file, machine_name):

    # Charge les config
    MachinesConfigLoader.load_config()
    ToolPathConfigLoader.load_config()

    machine_config = MachinesConfigLoader.get_machine(machine_name)

    # Instanciation des classes
    obj_interpreter = Interpreter(machine_config) 
    obj_toolpathviewer = ToolPathViewer()

    # Récup datas g-code
    list_datas = obj_interpreter.analyze(path_gcode_file)

    # Start viewer
    obj_toolpathviewer.open_viewer(stl_path_file, list_datas)


# Point d'entrée app
def main():
    """Point d'entrée de l'application"""





    # Charge les config
    MachinesConfigLoader.load_config() 





    style = Style(theme="darkly") 

    # Création form avec nom & dimension
    form = style.master
    form.title("PartAndCNCProgramAnalyzer")
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
        text="PartAndCNCProgramAnalyzer",
        font=("Segoe UI", 30, "bold"),
        bootstyle="dark",
        foreground="white"
    ).grid(column=0, row=0, columnspan=1, pady=(0, 30))

    # Section code ISO
    tb.Label(main_frame, text="📂 Fichier ISO :", font=("Segoe UI", 18)).grid(column=0, row=1, sticky="w", pady=5)
    label_gcode = tb.Label(main_frame, text="", width=50, bootstyle="secondary")
    label_gcode.grid(column=0, row=2, sticky="w")
    tb.Button(main_frame, text="Ouvrir", bootstyle="primary", command=lambda: file_select("Fichier ISO", "*.anc;*.nc;*.txt", label_gcode, update_calculate_button)).grid(column=0, row=3, sticky="w", pady=5)

    # Section STL
    tb.Label(main_frame, text="📂 Fichier STL :", font=("Segoe UI", 18)).grid(column=1, row=1, sticky="w", padx=(40, 0), pady=5)
    label_stl = tb.Label(main_frame, text="", width=50, bootstyle="secondary")
    label_stl.grid(column=1, row=2, sticky="w", padx=(40, 0))
    tb.Button(main_frame, text="Ouvrir", bootstyle="primary", command=lambda: file_select("Fichier STL", "*.stl", label_stl, update_calculate_button)).grid(column=1, row=3, sticky="w", padx=(40, 0), pady=5)

    # Section dossier de sortie
    tb.Label(main_frame, text="📁 Dossier de sortie :", font=("Segoe UI", 18)).grid(column=0, row=4, sticky="w", pady=5)
    label_output = tb.Label(main_frame, text="C:\\Temp", width=50, bootstyle="secondary")
    label_output.grid(column=0, row=5, sticky="w")
    tb.Button(main_frame, text="Choisir", bootstyle="primary", command=lambda: folder_select(label_output)).grid(column=0, row=6, sticky="w", pady=5)

    # Section machine
    tb.Label(main_frame, text="🛁 Machine :", font=("Segoe UI", 18)).grid(column=0, row=8, sticky="w", pady=5)
    # Données fournies par le JSON
    machines_list = MachinesConfigLoader.get_machines_names()
    selected_machine = tk.StringVar(value=machines_list[0] if machines_list else "")
    machine_combo = tb.Combobox(
        main_frame,
        textvariable=selected_machine,
        values=machines_list,
        state="readonly",
        width=47,
        bootstyle="secondary"
    )
    machine_combo.grid(column=0, row=9, sticky="w", pady=5)

    # Section visualiser
    tb.Label(main_frame, text="🔍 Visualiser la configuration machine :", font=("Segoe UI", 18)).grid(column=1, row=8, sticky="w", padx=(40, 0), pady=(20, 5))









    # A modifier pour visualiser une image de la machine ou une page de config

    #visualize_button = tb.Button(main_frame, text="Visualiser", bootstyle="success", command=lambda: viewer_launch())
    #visualize_button.grid(column=1, row=9, sticky="w", padx=(40, 0), pady=5)









    # Section calculer
    # Fonction local pour désactiver les boutons tant que le ISO n'est pas chargé
    def update_calculate_button():
        if label_gcode.cget("text"):  # Vérifier si un fichier ISO est sélectionné
            calculate_button.config(state="normal")  # Activer le bouton "Calculer"
            visualize_button.config(state="normal")  # Activer le bouton "Visualiser"
        else:
            calculate_button.config(state="disabled")  # Désactiver le bouton "Calculer"
            visualize_button.config(state="disabled")  # Désactiver le bouton "Visualiser"

    tb.Label(main_frame, text="⏱️ Calcul des données :", font=("Segoe UI", 18)).grid(column=0, row=11, sticky="w", pady=(20, 5))    
    calculate_button = tb.Button(main_frame, text="Calculer", bootstyle="success", command=lambda: gcode_treatment(
        label_gcode.cget("text"),
        Path(label_output.cget("text")) / get_datetime_string(), machine_combo.get()))
    calculate_button.grid(column=0, row=12, sticky="w", pady=5)
    calculate_button.config(state="disabled")  # Désactiver au début
    
    # Bouton Visualiser
    tb.Label(main_frame, text="🎥 Visualiser les trajectoires :", font=("Segoe UI", 18)).grid(column=1, row=11, sticky="w", padx=(40, 0), pady=(20, 5))
    visualize_button = tb.Button(main_frame, text="Visualiser", bootstyle="success", command=lambda: viewer_launch(
        label_gcode.cget("text"), 
        label_stl.cget("text"),
        machine_combo.get()))
    visualize_button.grid(column=1, row=12, sticky="w", padx=(40, 0), pady=5)
    visualize_button.config(state="disabled")  # Désactiver au début

    form.mainloop()

if __name__ == "__main__":
    main()

    



    
    
