# Alumno : Alejandro Olaf López Flores
# Codigo : 201922773

# librerias
import cv2
import pandas as pd
from ultralytics import YOLO
from tracker import *
import cvzone
# creamos la instancia del modelo yolov8s
model = YOLO('yolov8s.pt')

# codigo para mostrar el mouse
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)
cap = cv2.VideoCapture('video trabajo final.mp4') # cargamos el video que tenemos
# cargamos las clases de los objetos detectados por el modelo
my_file = open("clases.txt", "r")
data = my_file.read()
class_list = data.split("\n")
# inicializamos las variables y el bucle inicial
count = 0
tracker = Tracker()
counter = 0
# se lee los frames del video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    if count % 3 != 0:
        continue
    frame = cv2.resize(frame, (1020, 500))
# se realiza las predicciones de objetos utilizando el modelo
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    list = []
# filtrado de detecciones para objeto "persona-person"
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])

        c = class_list[d]
        if 'person' in c:
            list.append([x1, y1, x2, y2])
# seguimiento de objetos y dibujo en el frame
    bbox_id = tracker.update(list)
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = int(x3 + x4) // 2
        cy = int(y3 + y4) // 2
        cv2.circle(frame, (cx, cy), 4, (255, 0, 255), -1)
        cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)

# Contar personas y mostrar el contador en la ventana
    counter = len(bbox_id)
    cv2.putText(frame, f'Personas: {counter}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
# mostrar el frame en la ventana y con 'esc' puedes cerrar el programa
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
