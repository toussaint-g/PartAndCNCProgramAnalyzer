# -*- coding: utf-8 -*-

# Librairie standard
import vtk

# Modules internes
from interpreter import MoveType
from tool_path_builder import ToolPathBuilder


class ToolPathInterpreter:
    """Classe qui permet d'interpeter les datas"""

    def __init__(self):
        pass

    def analyze(self, list_datas, resolution_cercle):
        """Cette methode recupere les donnees utiles a la construction des trajectoires"""
        
        # Instanciation des classes
        obj_tool_path_builder = ToolPathBuilder()

        # Def structures points et lignes
        points_rapid_feedrate = vtk.vtkPoints()
        points_work_feedrate = vtk.vtkPoints()
        vertex_rapid_feedrate = vtk.vtkCellArray()
        vertex_work_feedrate = vtk.vtkCellArray()

        # Outil courant
        current_tool = 0

        # Acteurs
        actors = {"work": [], "rapid": []}
        obj_vtk_functions = VtkFunctions()

        # Initialisation du point precedent
        previous_point = [0, 0, 0]

        # Lecture datas
        for current_line in list_datas:

            # Si num outil de la ligne courante <> 0 et le courant = 0
            if current_line.tool_number != 0 and current_tool == 0:

                # Val outil courant
                current_tool = current_line.tool_number

                # Def structures points et lignes
                points_rapid_feedrate = vtk.vtkPoints()
                points_work_feedrate = vtk.vtkPoints()
                vertex_rapid_feedrate = vtk.vtkCellArray()
                vertex_work_feedrate = vtk.vtkCellArray()

            # Si nouvel outil
            if current_line.tool_number != current_tool and current_line.tool_number != 0:

                # Def poly_datas
                poly_data_rapid_feedrate = vtk.vtkPolyData()
                poly_data_work_feedrate = vtk.vtkPolyData()
                poly_data_rapid_feedrate.SetPoints(points_rapid_feedrate)
                poly_data_work_feedrate.SetPoints(points_work_feedrate)
                poly_data_rapid_feedrate.SetLines(vertex_rapid_feedrate)
                poly_data_work_feedrate.SetLines(vertex_work_feedrate)
                
                # Ajout des acteurs
                actors = obj_vtk_functions.create_actors(poly_data_rapid_feedrate, poly_data_work_feedrate, actors, current_tool)

                # Redef structures points et lignes
                points_rapid_feedrate = vtk.vtkPoints()
                points_work_feedrate = vtk.vtkPoints()
                vertex_rapid_feedrate = vtk.vtkCellArray()
                vertex_work_feedrate = vtk.vtkCellArray()

                # Val outil courant
                current_tool = current_line.tool_number

            # Si distance parcourue
            if current_line.distance != 0.0 or current_line.distance_in_material != 0.0 and current_line.tool_number != 0:

                # Point courant
                current_point = [current_line.endpoint_x, current_line.endpoint_y, current_line.endpoint_z]

                # Si ligne en avance rapide
                if current_line.move_type == MoveType.RAPID_MOVE:

                    # Contructeur ligne
                    obj_tool_path_builder.create_line(points_rapid_feedrate, vertex_rapid_feedrate, previous_point, current_point)

                # Si ligne en avance travail
                elif current_line.move_type == MoveType.LINEAR_MOVE:

                    # Contructeur ligne
                    obj_tool_path_builder.create_line(points_work_feedrate, vertex_work_feedrate, previous_point, current_point)

                # Si cercle CCW
                elif current_line.move_type == MoveType.CIRCULAR_MOVE_CW:
                    
                    # Contructeur cercle
                    obj_tool_path_builder.create_circle(points_work_feedrate, vertex_work_feedrate, previous_point, current_point, current_line.radius, resolution_cercle, True)

                # Si cercle CW
                elif current_line.move_type == MoveType.CIRCULAR_MOVE_CCW:

                    # Contructeur cercle
                    obj_tool_path_builder.create_circle(points_work_feedrate, vertex_work_feedrate, previous_point, current_point, current_line.radius, resolution_cercle, False)

                # Recup pt precedent
                previous_point = current_point

        # Def poly_datas
        poly_data_rapid_feedrate = vtk.vtkPolyData()
        poly_data_work_feedrate = vtk.vtkPolyData()
        poly_data_rapid_feedrate.SetPoints(points_rapid_feedrate)
        poly_data_work_feedrate.SetPoints(points_work_feedrate)
        poly_data_rapid_feedrate.SetLines(vertex_rapid_feedrate)
        poly_data_work_feedrate.SetLines(vertex_work_feedrate)           
        
        # Ajout des acteurs
        actors = obj_vtk_functions.create_actors(poly_data_rapid_feedrate, poly_data_work_feedrate, actors, current_tool)
        return actors


class VtkFunctions:
    """Classe qui regroupe des fonctions pour vtk"""

    def __init__(self):
        pass
        
    def create_actors(self, datas_rapid_feedrate, datas_work_feedrate, list_actors, current_tool):
        """Cette methode sert a creer les acteurs pour les trajectoires"""

        # Mapper
        mapper_rapid_feedrate = vtk.vtkPolyDataMapper()
        mapper_work_feedrate = vtk.vtkPolyDataMapper()
        mapper_rapid_feedrate.SetInputData(datas_rapid_feedrate)
        mapper_work_feedrate.SetInputData(datas_work_feedrate)

        # Actors
        actor_rapid_feedrate = vtk.vtkActor()
        actor_work_feedrate = vtk.vtkActor()
        actor_rapid_feedrate.SetMapper(mapper_rapid_feedrate)
        actor_work_feedrate.SetMapper(mapper_work_feedrate)

        # Tag pour récup num outil
        actor_rapid_feedrate.tag = current_tool
        actor_work_feedrate.tag = current_tool

        # Ajout dans structure 2 niveaux
        list_actors["work"].append(actor_work_feedrate)   # work index 0
        list_actors["rapid"].append(actor_rapid_feedrate)  # rapid index 1

        return list_actors
