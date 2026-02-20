
# -*- coding: utf-8 -*-

import math
import re
from machine import Machine
from enum import Enum

class Interpreter:
    """Classe qui permet d'analyser et comprendre le GCode"""

    def __init__(self):
        try:
            self.rapid_move_code = Machine.data["gcode"]["rapidmove"]
            self.linear_move_code = Machine.data["gcode"]["linearmove"]
            self.circular_move_CW_code = Machine.data["gcode"]["circularmoveCW"]
            self.circular_move_CWW_code = Machine.data["gcode"]["circularmoveCCW"]
            self.rapidfeedrate = Machine.data["machine"]["rapidfeedrate"]
            self.change_tool_time = Machine.data["machine"]["changetooltime"]
        except KeyError:
            raise ValueError("MachineConfigError: une clé est absente dans le fichier JSON")

    def analyze(self, path):
        """Cette méthode vient extraire les données utiles de chaque ligne du GCode et les stocker dans une liste d'objet"""

        # Liste pour stocker les objets Line
        lines = []

        obj_modal = Modal()
        obj_mathematical_functions = MathematicalFunctions()

        with open(path, 'r') as gcode_file:
            
            # Les Regex ont été obtenues à partir de ChatGPT
            # On récupère la valeur après la lettre
            # Si élément pas trouvé, ça retourne None
            pattern_x = re.compile(r'X(-?\d*\.?\d+)')
            pattern_y = re.compile(r'Y(-?\d*\.?\d+)')
            pattern_z = re.compile(r'Z(-?\d*\.?\d+)')
            pattern_radius = re.compile(r'R(-?\d*\.?\d+)')
            pattern_i = re.compile(r'I(-?\d*\.?\d+)')
            pattern_j = re.compile(r'J(-?\d*\.?\d+)')
            pattern_feedrate = re.compile(r'F(-?\d*\.?\d+)')
            pattern_tool = re.compile(r'T(-?\d*\.?\d+)')
            pattern_move = re.compile(r'\bG0?([0-3])(?=\D|$)')
            pattern_mode = re.compile(r'G(90|91)')
            pattern_m6 = re.compile(r'\bM6\b')

            for line in gcode_file:

                line = re.sub(r'\(.*?\)', '', line).strip() #Suppression du contenu des commentaires

                # Recherche des correspondances dans la ligne
                match_x = pattern_x.search(line)
                match_y = pattern_y.search(line)
                match_z = pattern_z.search(line)
                match_radius = pattern_radius.search(line)
                match_i = pattern_i.search(line)
                match_j = pattern_j.search(line)
                match_feedrate = pattern_feedrate.search(line)
                match_tool = pattern_tool.search(line)
                match_move = pattern_move.search(line)
                match_mode = pattern_mode.search(line)
                match_m6 = pattern_m6.search(line)

                if match_x:
                    if Machine.data["machine"]["xdiameter"]:
                        position_x = float(match_x.group(1))/2  #Si X est présent dans la ligne je le mémorise en convertissant en rayon si usinage en diamètre
                    else:
                        position_x = float(match_x.group(1))    #Si X est présent dans la ligne je le mémorise
                else:
                    position_x = obj_modal.position_x       #Si pas de nouveau X dans la ligne je récupère la valeur de la ligne précédente

                if match_y:
                    position_y = float(match_y.group(1)) 
                else:
                    position_y = obj_modal.position_y

                if match_z:
                    position_z = float(match_z.group(1)) 
                else:
                    position_z = obj_modal.position_z

                if match_radius:
                    radius = float(match_radius.group(1)) 
                else:
                    radius = obj_modal.radius






                #TODO: traitement IJ à vérifier
                if match_i and match_j:
                    
                    #center_x = obj_modal.position_x + float(match_i.group(1))
                    #center_y = obj_modal.position_y + float(match_j.group(1))
                    # Calcul du rayon à partir des valeurs I et J
                    radius = math.sqrt((float(match_i.group(1))) ** 2 + (float(match_j.group(1))) ** 2)











                if match_feedrate:
                    feedrate = float(match_feedrate.group(1)) 
                else:
                    feedrate = obj_modal.feedrate

                if match_tool:
                    tool = int(match_tool.group(1)) 
                else:
                    tool = obj_modal.tool_number

                if match_move:
                    move = f'G{match_move.group(1)}'
                else:
                    move = obj_modal.gcode_group01

                if match_mode:
                    mode = f'G{match_mode.group(1)}'
                else:
                    mode = obj_modal.gcode_group02

                if move == self.rapid_move_code :
                    distance = obj_mathematical_functions.linear_distance_3D(obj_modal.position_x, obj_modal.position_y, obj_modal.position_z, position_x, position_y, position_z)
                    distance_in_material = 0.0
                    move_type = MoveType.RAPID_MOVE
                elif move == self.linear_move_code:
                    distance = obj_mathematical_functions.linear_distance_3D(obj_modal.position_x, obj_modal.position_y, obj_modal.position_z, position_x, position_y, position_z)
                    distance_in_material = distance
                    move_type = MoveType.LINEAR_MOVE
                else:
                    distance = obj_mathematical_functions.circular_distance_3D(obj_modal.position_x, obj_modal.position_y, obj_modal.position_z, position_x, position_y, position_z, radius)
                    distance_in_material = distance
                    if move == self.circular_move_CW_code:
                        move_type = MoveType.CIRCULAR_MOVE_CW
                    else:
                        move_type = MoveType.CIRCULAR_MOVE_CCW
                        
                if move == self.rapid_move_code:
                    time = obj_mathematical_functions.mouvement_time(distance, self.rapidfeedrate)
                    productive_time = 0.0
                else: 
                    time = obj_mathematical_functions.mouvement_time(distance, feedrate)
                    productive_time = time

                if match_m6:
                    time = time + (self.change_tool_time/60)
                    
                obj_line = Line(line, tool, distance, distance_in_material, time, productive_time, move_type, radius, feedrate, position_x, position_y, position_z) # Instanciation de l'objet
                lines.append(obj_line) # Ajout de l'objet à la liste

                #Mise à jour de l'objet Modal pour prochaine itération
                obj_modal.position_x = position_x       
                obj_modal.position_y = position_y 
                obj_modal.position_z = position_z
                obj_modal.radius = radius
                obj_modal.feedrate = feedrate
                obj_modal.tool_number = tool
                obj_modal.gcode_group01 = move
                obj_modal.gcode_group02 = mode

        return lines

class MathematicalFunctions:
    """Classe qui permet d'analyser et comprendre le GCode"""

    def __init__(self):
        pass
        
    def linear_distance_3D(self, start_point_x, start_point_y, start_point_z, end_point_x, end_point_y, end_point_z):
        """Cette métthode retourne la distance entre les points"""

        # Formule tirée de https://fr.wikipedia.org/wiki/Distance_euclidienne
        return math.sqrt((end_point_x - start_point_x)**2 + (end_point_y - start_point_y)**2 + (end_point_z - start_point_z)**2)

        
    def circular_distance_3D(self, start_point_x, start_point_y, start_point_z, end_point_x, end_point_y, end_point_z, radius):
        """Classe qui permet de calculer la longueur d'un arc. Il tient également compte d'un éventuel mouvement sur le 3ème axe (3d)"""
        # Pour la partie mathématique de cette fonction, je me suis appuyé sur ChatGPT
        
        # Milieu du segment reliant start et end
        mx = (start_point_x + end_point_x) / 2
        my = (start_point_y + end_point_y) / 2
        
        # Distance entre start et end
        d = math.dist((start_point_x, start_point_y), (end_point_x, end_point_y))
        
        if d > 2 * radius:
            raise ValueError("Le rayon est trop petit pour passer par les deux points !!")
        
        # Distance entre le milieu et le centre du cercle
        h = math.sqrt(radius**2 - (d / 2) ** 2)
        
        # Calcul du vecteur perpendiculaire au segment start-end
        dx, dy = end_point_x - start_point_x, end_point_y - start_point_y
        perp_dx, perp_dy = -dy, dx
        
        # Normalisation du vecteur
        norm = math.sqrt(perp_dx**2 + perp_dy**2)

        if norm != 0:
            perp_dx, perp_dy = perp_dx / norm, perp_dy / norm
        
        # Deux solutions pour le centre du cercle
        cx1, cy1 = mx + h * perp_dx, my + h * perp_dy # cercle 1
        #cx2, cy2 = mx - h * perp_dx, my - h * perp_dy # cercle 2 --> #TODO gérer les cas avec programmation IJ
        
        # Choisir le bon cercle
        cx, cy = cx1, cy1
        
        # Calcul de l'angle entre start et end en passant par le centre
        angle1 = math.atan2(start_point_y - cy, start_point_x - cx)
        angle2 = math.atan2(end_point_y - cy, end_point_x - cx)
        angle = abs(angle2 - angle1)
        
        # Si l'angle dépasse 180°, on prend l'arc  le plus court --> on peut traité comme ça car arc programmé sans IJ ne doit pas excéder 180°
        if angle > math.pi:
            angle = 2 * math.pi - angle 
        
        # Calcul de la longueur de l'arc
        arc_length = radius * angle

        # Calcul distance 3d si hélicoidal
        arc_length_3d = math.sqrt((arc_length **2) + (abs(end_point_z - start_point_z) **2))
    
        return arc_length_3d

    def mouvement_time(self, distance, feedrate):
        """Cette méthode retourne la durée pour parcourir une certaine distance"""
        try:
            return distance/feedrate # feedrate est en principe en mm/min donc retourne la valeur en minutes
        except ZeroDivisionError:
            print("Error: Dision par 0 !!")
            return 0

class Modal:
    """Classe qui permet de mémoriser les fonctions modales du GCode"""

    def __init__(self):

        try:
            self.gcode_group01 = Machine.data["gcode"]["rapidmove"]
            self.gcode_group02 = Machine.data["machine"]["defaultmovetype"] 
            self.feedrate = Machine.data["machine"]["rapidfeedrate"]
            self.position_x = Machine.data["machine"]["refx"]
            self.position_y = Machine.data["machine"]["refy"]
            self.position_z = Machine.data["machine"]["refz"]
        except KeyError:
            raise ValueError("MachineConfigError: une clé est absente dans le fichier JSON")
        
        self.tool_number = 0
        self.radius = 0.0

class Line:
    """Classe qui permet de mémoriser le contenu utile au rapport des lignes du G-Code"""

    def __init__(self, g_code_line, tool_number, distance, distance_in_material, time, productive_time, move_type, radius, feedrate, endpoint_x, endpoint_y, endpoint_z):
        self.g_code_line = g_code_line
        self.tool_number = tool_number
        self.distance = distance
        self.distance_in_material = distance_in_material
        self.time = time
        self.productive_time = productive_time
        self.move_type = move_type
        self.radius = radius
        self.feedrate = feedrate
        self.endpoint_x = endpoint_x
        self.endpoint_y = endpoint_y
        self.endpoint_z = endpoint_z

class MoveType(Enum):
    """Enum pour mémoriser les types de mouvement par ligne"""
    ANY = -1
    RAPID_MOVE = 0
    LINEAR_MOVE = 1
    CIRCULAR_MOVE_CW = 2 # Sens horaire
    CIRCULAR_MOVE_CCW = 3 # Sens anti-horaire

