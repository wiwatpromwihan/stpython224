โปรเจกต์ Streamlit: Currency Exchange
=====================================

ไฟล์:
1. streamlit_exchange_rate_colab.ipynb
   - อัปโหลดเข้า Google Colab แล้ว Run all ได้
   - ติดตั้ง Streamlit และ LocalTunnel
   - สร้าง app.py และเปิดเว็บ

2. currency_exchange_app.py
   - ไฟล์ Streamlit app สำหรับนำไปรันแยกได้

ขั้นตอน:
1. สมัคร/เข้าสู่ระบบ https://www.exchangerate-api.com/
2. คัดลอก API Key
3. เปิดไฟล์ streamlit_exchange_rate_colab.ipynb ใน Google Colab
4. รันทุกเซลล์ตามลำดับ
5. เปิด URL จาก LocalTunnel
6. กรอก API Key ในหน้าเว็บ
7. เลือกสกุลเงินต้นทาง สกุลเงินปลายทาง และจำนวนเงิน
8. กด "คำนวณอัตราแลกเปลี่ยน"

API ที่ใช้:
- Supported Codes:
  https://v6.exchangerate-api.com/v6/YOUR-API-KEY/codes
- Pair Conversion:
  https://v6.exchangerate-api.com/v6/YOUR-API-KEY/pair/FROM/TO/AMOUNT

หมายเหตุ:
- ไม่ควรเขียน API Key จริงค้างไว้ในโค้ด หากจะแชร์ไฟล์ให้ผู้อื่น
- ตัวอย่างนี้ให้ผู้ใช้กรอก API Key ผ่านหน้า Streamlit
