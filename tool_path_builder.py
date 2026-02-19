
# -*- coding: utf-8 -*-

# Librairie standard
import vtk
import numpy as np


class ToolPathBuilder:
    """Cette classe permet construire les trajectoires"""
    
    def __init__(self):
        pass

    def create_line(self, points_vtk, lines_vtk, start_point, end_point):
        """Cette methode permet de creer les donnees pour une ligne"""
        
        # Création points VTK
        start_point_tmp = points_vtk.InsertNextPoint(start_point[0], start_point[1], start_point[2])
        end_point_tmp = points_vtk.InsertNextPoint(end_point[0], end_point[1], end_point[2])

        # Création ligne VTK
        line_toolpath = vtk.vtkLine()
        line_toolpath.GetPointIds().SetId(0, start_point_tmp)
        line_toolpath.GetPointIds().SetId(1, end_point_tmp)

        # Ajout de la courbe dans le vtkCellArray
        lines_vtk.InsertNextCell(line_toolpath)

    def create_circle(self, points_vtk, lines_vtk, start_point, end_point, radius, resolution_cercle, sens_cw):
        """Cette methode permet de creer les donnees pour un cercle"""

        # Convertir les points de départ et d’arrivée en tableaux numpy
        np_start_point = np.array(start_point, dtype=float)
        np_end_point = np.array(end_point, dtype=float)

        # Calcul de la corde (projection dans XY)
        corde = np_end_point[:2] - np_start_point[:2]
        lg_corde = np.linalg.norm(corde)
        if lg_corde == 0:
            raise ValueError("Les points de départ et d'arrivée sont identiques.")
        if lg_corde > 2 * radius:
            raise ValueError("Le rayon est trop petit pour connecter les deux points.")

        # Milieu de la corde
        midpoint = (np_start_point[:2] + np_end_point[:2]) / 2
        h = np.sqrt(radius**2 - (lg_corde / 2)**2)

        # Direction de la corde normalisée
        corde_dir = corde / lg_corde
        # Vecteur perpendiculaire dans le plan XY
        perp = np.array([-corde_dir[1], corde_dir[0]])
        # Deux centres possibles (au-dessus ou en dessous de la corde)
        center1 = midpoint + h * perp
        center2 = midpoint - h * perp

        # Fonction utilitaire : calcule l'angle entre un point et le centre
        def angle_from(center, point):
            v = point[:2] - center
            return np.arctan2(v[1], v[0])

        # Détermination du centre correct selon le sens horaire/antihoraire
        a1_1 = angle_from(center1, np_start_point)
        a2_1 = angle_from(center1, np_end_point)
        delta_1 = (a2_1 - a1_1) % (2 * np.pi)
        is_ccw = delta_1 < np.pi
        center = center1 if (is_ccw != sens_cw) else center2

        # Calcul des angles de début et de fin
        angle_start = angle_from(center, np_start_point)
        angle_end = angle_from(center, np_end_point)

        # Ajustement des angles selon le sens de parcours
        if sens_cw:
            if angle_end > angle_start:
                angle_end -= 2 * np.pi
        else:
            if angle_end < angle_start:
                angle_end += 2 * np.pi

        # Longueur de l'arc = rayon × angle
        arc_angle = abs(angle_end - angle_start)
        arc_length = radius * arc_angle

        # Nombre de segments requis selon la longueur max souhaitée
        num_segments = max(int(np.ceil(arc_length / resolution_cercle)), 1)
        # Générer les angles équidistants pour chaque point de l'arc
        angles = np.linspace(angle_start, angle_end, num_segments + 1)

        # Interpolation linéaire de la coordonnée Z
        z_start = np_start_point[2]
        z_end = np_end_point[2]
        z_step = (z_end - z_start) / num_segments

        point_ids = []
        for i, theta in enumerate(angles):
            x = center[0] + radius * np.cos(theta)
            y = center[1] + radius * np.sin(theta)
            z = z_start + i * z_step
            pid = points_vtk.InsertNextPoint(x, y, z)
            point_ids.append(pid)

        # Création polyligne VTK avec tous les points générés
        polyline = vtk.vtkPolyLine()
        polyline.GetPointIds().SetNumberOfIds(len(point_ids))
        for i, pid in enumerate(point_ids):
            polyline.GetPointIds().SetId(i, pid)

        # Ajout de la courbe dans le vtkCellArray
        lines_vtk.InsertNextCell(polyline)


