import cv2
import mediapipe as mp  
import time
import pyaudio
import os

#Parmak sayısını kontrol eden fonksiyon
def parmaksayisi(lst):
    cnt = 0
    
    thresh = (lst.landmark[9].y*100 - lst.landmark[12].y*100)

    if (lst.landmark[8].y*100 - lst.landmark[5].y*100) > thresh:
        cnt += 1
    
    if (lst.landmark[12].y*100 - lst.landmark[9].y*100) > thresh:
        cnt += 1

    if (lst.landmark[16].y*100 - lst.landmark[13].y*100) > thresh:
        cnt += 1

    if (lst.landmark[20].y*100 - lst.landmark[17].y*100) > thresh:
        cnt += 1

    return cnt





#Görüntüyü al
cap = cv2.VideoCapture(0)


#mediapipe kütüphanesi ile el algılama
mpHand= mp.solutions.hands

#mediapipe el algılama modelini başlat ve maksimum el sayısını 1 olarak ayarla
hands= mpHand.Hands(max_num_hands=1)

#mediapipe el çizim kütüphanesini başlat
mpDraw= mp.solutions.drawing_utils

#Time modülü ile FPS hesaplama için parametreler
pTime = 0
cTime = 0  

#Programın sürekliliği için sonsuz döngü
while True:
    #Kameradan görüntü al
    succcess,img = cap.read()
    if not succcess:
        break
    
    #cv2.cvtColor() fonksiyonu ile görüntüyü RGB formatına çevir
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
    #hands.process() fonksiyonu ile el algılama modelini uygula
    results =  hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    #FPS hesaplama
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    #
    if results.multi_hand_landmarks:

        hand_keypoints = results.multi_hand_landmarks[0]

        print(parmaksayisi(hand_keypoints))

        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img,handLms,mpHand.HAND_CONNECTIONS,)



            for id,lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                cv2.circle(img,(cx,cy),5,(255,0,255),cv2.FILLED)

                if id == 0:
                    cv2.putText(img,f'FPS:{int(fps)}',(cx,cy),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

            if len(handLms.landmark) > 8:  # Yeterli Sayıda nokta varsa
                # Baş ve işaret parmağının ucununn koordinatlarını al 
                x1, y1 = int(handLms.landmark[4].x * w), int(handLms.landmark[4].y * h)  # Başparmak ucu
                
                x2, y2 = int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)  # İşaret parmağı

                # İki nokta arasındaki mesafeyi hesapla
                distance = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                print(distance)
                # Mesafe Değiştikçe Çemberin boyutunu ayarla
                radius = max(min(300, distance-20), 10)  # Adjust radius to shrink as distance decreases
                # Çemberi çiz
                cv2.circle(img, ((x1+100 + x2+100) // 2, (y1 + y2) // 2), radius, (255, 0, 0), 2)
                # Mesafeyi göster
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f'{distance}px', (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                
                
                x3,y3 = int(handLms.landmark[9].x*w), int(handLms.landmark[9].y*h)
                x4,y4 = int(handLms.landmark[0].x*w), int(handLms.landmark[0].y*h)
                #Medya kontrolu uyarısında kullanılacak koordinatlar
                medya_distance = int(((x3-x4)**2 + (y3-y4)**2) ** 0.5)
        if parmaksayisi(handLms) == 3:

            # Ses kontrolü için distance değerini kullan
            max_volume = 50  # Maksimum ses seviyesi
            min_volume = 0    # Minimum ses seviyesi
            volume = max(min_volume, min(max_volume, int((distance / 300) * max_volume)))  # Mesafeye göre ses seviyesi
            os.system(f"osascript -e 'set volume output volume {volume}'")  # macOS için ses kontrolü

            cv2.putText(img, "Ses Kontrolu ACIK", (40,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0 , 255 , 0), 5)
            cv2.putText(img, f"Ses Duzeyi: {volume}", (40,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (178 , 255 , 102), 5)
            

        else:
            max_volume = 0  # Maksimum ses seviyesi
            min_volume = 0    # Minimum ses seviyesi
            volume = max(min_volume, min(max_volume, int((distance / 300) * max_volume)))  # Mesafeye göre ses seviyesi

            cv2.putText(img, f"Ses Duzeyi: {volume}", (40,150), cv2.FONT_HERSHEY_SIMPLEX, 2, (178 , 255 , 102), 5)

            cv2.putText(img, "Ses Kontrolu KAPALI", (40,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0 , 0 , 255), 5)    






    cv2.imshow("Image",img)




    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
# Dört parmak aşağı indiği zaman açılır/kapanır
#baş ve işaret parmağı arası ses yüksekliğini kontrol eder.
