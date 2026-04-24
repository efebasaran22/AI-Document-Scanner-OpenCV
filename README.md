# 📄 AI Destekli Belge Tarama ve OCR Uygulaması

Bu proje, Python ve OpenCV kütüphaneleri kullanılarak, fiziksel belgelerin dijital ortama en yüksek netlikte aktarılması amacıyla geliştirilmiştir.

### 🚀 Özellikler
* **Kenar Tespiti:** Görüntü işleme algoritmaları ile kağıdın sınırlarını otomatik olarak belirler.
* **Perspektif Düzeltme (Warp Perspective):** Yamuk duran belgeleri tam karşıdan bakılıyormuş gibi düzeltir.
* **Görüntü İyileştirme:** Okunabilirliği artırmak için eşikleme (thresholding) ve gürültü azaltma tekniklerini uygular.
* **OCR Entegrasyonu:** Pytesseract kütüphanesi sayesinde taranan belgedeki metinleri dijital metne dönüştürür.

### 🛠️ Kullanılan Teknolojiler
* **Programlama Dili:** Python
* **Kütüphaneler:** OpenCV, Pytesseract, NumPy
* **Algoritmalar:** Canny Edge Detection, Gaussian Blur, Four-Point Perspective Transform

### 💡 Nasıl Çalışır?
1. Uygulama bir fotoğrafı girdi olarak alır.
2. Kağıdın dört köşesi tespit edilir ve kuş bakışı görünüme çevrilir.
3. Görüntü siyah-beyaz formata getirilerek metin tanıma (OCR) işlemi gerçekleştirilir.
