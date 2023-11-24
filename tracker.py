import math


class Tracker:
    def __init__(self):
        # guardamos la posicion central de los objetos
        self.center_points = {}
        # se guardan los id y cada vez que aparesca un nuevo objeto se le asigna un nuevo id
        self.id_count = 0

# el metodo update toma la lista de rectangulos de los objetos detectados
# y luego calcula el centro de cada objeto
    def update(self, objects_rect):

        objects_bbs_ids = []

        # obtenemos el centro del objeto
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # verificamos si el objeto ya fue detectado anterior mente
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 35:
                    self.center_points[id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # si un objeto nuevo es detectado asignamos un nuevo id al objeto
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # despues de procesar los objetos en el frame se crea un nuevo diccionario
        # que contiene el centro de los objetos que estan en la pantalla
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # y se actualiza los antiguos puntos de centro con los nuevos
        self.center_points = new_center_points.copy()
        return objects_bbs_ids