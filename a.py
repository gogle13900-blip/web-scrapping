"""
🛍️  ربات جستجوی محصولات تکنولایف  🛍️
=====================================
این برنامه محصولات رو از سایت تکنولایف پیدا می‌کنه
و توی یه فایل CSV بسیار زیبا ذخیره می‌کنه
=====================================
"""

from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime
import os

# ========== دریافت ورودی ==========
print("\n" + "⭐" * 60)
print("🛒  ربات جستجوی هوشمند محصولات تکنولایف  🛒".center(60))
print("⭐" * 60)

a = input("\n🔍 لطفاً نام محصول مورد نظر را وارد کنید: ").strip()

if not a:
    print("❌ خطا: نام محصول نمی‌تواند خالی باشد!")
    exit()

# ========== آماده‌سازی جستجو ==========
b = a.replace(" ", "+")
url = f"https://technolife.ir/search?q={b}"
print(f"\n🌐 در حال جستجوی '{a}' در سایت تکنولایف...")

# ========== دریافت صفحه ==========
try:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    print("✅ صفحه با موفقیت دریافت شد")
except:
    print("❌ خطا در ارتباط با سایت!")
    exit()

# ========== پردازش HTML ==========
soup = BeautifulSoup(r.text, 'html.parser')
all_sections = soup.find_all('section')
print(f"📦 {len(all_sections)} بخش برای بررسی پیدا شد")

# ========== اطلاعات زمان ==========
now = datetime.now()
date_persian = now.strftime("%Y/%m/%d")
time_persian = now.strftime("%H:%M")
weekdays = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه", "یک‌شنبه"]
weekday = weekdays[now.weekday()]

# ========== ایجاد فایل CSV ==========
filename = f"نتایج_جستجو_{a.replace(' ', '_')}_{date_persian.replace('/', '-')}.csv"

with open(filename, "w", newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    
    # ---------- خطوط تزئینی بالا ----------
    writer.writerow(["="*80])
    writer.writerow(["🛒", "گزارش جستجوی محصولات از سایت تکنولایف", "", "", "", "🛒"])
    writer.writerow(["="*80])
    
    # ---------- اطلاعات جستجو ----------
    writer.writerow(["📅 تاریخ:", date_persian, "", "⏰ ساعت:", time_persian, "", "📆 روز:", weekday])
    writer.writerow(["🔍 کلمه جستجو:", a, "", "🌐 آدرس:", url[:50] + "...", ""])
    writer.writerow(["─"*80])
    
    # ---------- هدر اصلی جدول ----------
    writer.writerow([
        "🔢 ردیف",
        "📱 نام محصول",
        "💰 قیمت (تومان)",
        "🌐 لینک محصول"
    ])
    writer.writerow(["─"*10, "─"*40, "─"*20, "─"*50])
    
    # ---------- استخراج و ذخیره محصولات ----------
    found_count = 0
    products_list = []
    
    print("\n" + "🔍" * 40)
    print("محصولات پیدا شده:")
    print("🔍" * 40)
    
    for idx, section in enumerate(all_sections, 1):
        # پیدا کردن اسم محصول
        name = None
        for tag in section.find_all(['h2', 'h3', 'strong', 'div']):
            text = tag.text.strip()
            if len(text) > 20 and ('گوشی' in text or 'موبایل' in text or 'اپل' in text or 'سامسونگ' in text):
                name = text
                break
        
        # پیدا کردن قیمت
        price = "ناموجود"
        for tag in section.find_all(['p', 'div', 'span']):
            text = tag.text.strip()
            if 'تومان' in text:
                # تمیز کردن قیمت
                clean_text = text.replace('تومان', '').strip()
                # جدا کردن فقط عدد اصلی
                parts = clean_text.split()
                if parts:
                    price = parts[0] + " تومان"
                break
        
        # پیدا کردن لینک
        link = "ندارد"
        link_tag = section.find('a', href=True)
        if link_tag:
            link = link_tag['href']
            if not link.startswith('http'):
                link = f"https://technolife.ir{link}"
        
        # ذخیره اگر اسم پیدا شد و شامل کلمه جستجو بود
        if name and a.lower() in name.lower():
            found_count += 1
            writer.writerow([found_count, name, price, link])
            print(f"  ✅ {found_count:2d}. {name[:60]}...")
            # ذخیره در لیست برای گزارش نهایی
            if found_count == 1:
                first_product = (name, price, link)
    
    # ---------- خطوط تزئینی پایین ----------
    writer.writerow(["─"*80])
    writer.writerow(["📊 جمع‌بندی:", f"تعداد کل محصولات پیدا شده: {found_count}", "", "", "", ""])
    writer.writerow(["⏰ زمان اجرا:", f"{datetime.now().strftime('%H:%M:%S')}", "", "📁 نام فایل:", filename, ""])
    writer.writerow(["="*80])
    writer.writerow(["✨", "تولید شده توسط ربات جستجوی تکنولایف", "✨"])
    writer.writerow(["="*80])

# ========== گزارش نهایی در کنسول ==========
print("\n" + "⭐" * 60)
print("✅ گزارش نهایی".center(60))
print("⭐" * 60)
print(f"🔍 محصول جستجو شده: {a}")
print(f"📦 تعداد محصولات پیدا شده: {found_count}")
print(f"📁 مسیر فایل: {os.path.abspath(filename)}")
print(f"📅 تاریخ ایجاد: {date_persian} - {time_persian}")

if found_count > 0:
    print("\n✨ نمونه اولین محصول:")
    print(f"   📱 نام: {first_product[0][:100]}...")
    print(f"   💰 قیمت: {first_product[1]}")
    print(f"   🔗 لینک: {first_product[2][:60]}...")

print("\n" + "🎉" * 30)
print("🎊  عملیات با موفقیت به پایان رسید!  🎊".center(40))
print("🎉" * 30)
print(f"\n📌 فایل '{filename}' با موفقیت ساخته شد.")
print("💡 می‌توانید آن را با Excel یا Notepad باز کنید.")