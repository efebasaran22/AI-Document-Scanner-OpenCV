import cv2
import numpy as np
import pytesseract

# Tesseract'ın yolunu belirtiyoruz
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def noktalari_sirala(pts):
    x_sirali = pts[np.argsort(pts[:, 0]), :]
    sol_noktalar = x_sirali[:2, :]
    sag_noktalar = x_sirali[2:, :]
    
    sol_noktalar = sol_noktalar[np.argsort(sol_noktalar[:, 1]), :]
    (tl, bl) = sol_noktalar 
    
    sag_noktalar = sag_noktalar[np.argsort(sag_noktalar[:, 1]), :]
    (tr, br) = sag_noktalar 
    
    return np.array([tl, tr, br, bl], dtype="float32")

image = cv2.imread('belge.jpeg')
image = cv2.resize(image, (600, 800)) 
orig = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)

kernel = np.ones((5, 5), np.uint8)
edged = cv2.dilate(edged, kernel, iterations=1)

cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

screenCnt = None
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4: 
        screenCnt = approx
        break

if screenCnt is not None:
    cv2.drawContours(orig, [screenCnt], -1, (0, 255, 0), 3)

    pts = screenCnt.reshape(4, 2)
    rect = noktalari_sirala(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # =================================================================
    # YAPAY ZEKA İLE YÖN TESPİTİ (Gözlük Takılmış Versiyon)
    # =================================================================
    print("Sistem belgeyi tarıyor... Lütfen bekleyin...")
    try:
        # Yapay zekaya özel siyah-beyaz netleştirme (Thresholding)
        gray_ai = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        _, thresh_ai = cv2.threshold(gray_ai, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # OSD (Yön analizi) için net resmi kullanıyoruz
        osd_veri = pytesseract.image_to_osd(thresh_ai, output_type=pytesseract.Output.DICT)
        aci = osd_veri['rotate']
        
        print(f"BAŞARILI! Yapay zeka yazının yönünü buldu. Belge {aci} derece döndürülüyor...")
        
        # Eğer tersse 180 derece, yan yatıksa 90 derece döndür
        if aci == 90:
            warped = cv2.rotate(warped, cv2.ROTATE_90_CLOCKWISE)
        elif aci == 180:
            warped = cv2.rotate(warped, cv2.ROTATE_180)
        elif aci == 270:
            warped = cv2.rotate(warped, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
    except Exception as e:
        print(f"YAPAY ZEKA DİRENDİ: {e}")
        print("BİLGİ: B Planı (Geometrik En-Boy) devreye giriyor...")
        if maxWidth > maxHeight:
            warped = cv2.rotate(warped, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # =================================================================

    # EKRAN GÖSTERİMİ VE KLAVYE KONTROLÜ
    print("\n--- KONTROLLER ---")
    print("Kağıt ters veya yan duruyorsa 'R' tuşuna basarak döndürebilirsin.")
    print("Çıkmak için 'Q' veya 'ESC' tuşuna bas.")
    
    cv2.imshow("1 - Bulunan Kenarlar", orig)
    
    while True:
        cv2.imshow("2 - Kusursuz Taranmis Belge", warped)
        key = cv2.waitKey(0) & 0xFF
        
        if key == ord('r'): # Eğer klavyeden 'R' (Rotate) tuşuna basılırsa
            warped = cv2.rotate(warped, cv2.ROTATE_180)
            print("Belge 180 derece döndürüldü.")
        elif key == 27 or key == ord('q'): # Eğer ESC veya Q tuşuna basılırsa
            break # Programı kapat
            
    cv2.destroyAllWindows()
else:
    print("HATA: Fotoğrafta 4 köşeli bir kağıt bulunamadı!")
    cv2.imshow("Algilanan Cizgiler", edged)
    cv2.waitKey(0)