import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import Tk, Label, Entry, Button, messagebox, Text, Scrollbar, Y, Toplevel, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, messagebox, END, BOTH, LEFT, RIGHT, Y, TOP, X
from tkinter import ttk

# MySQL bağlantısı kurma
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sentes_solar"
)

if mydb.is_connected():
    print("MySQL veritabanına bağlantı başarılı.")

# Tkinter uygulama penceresi
app = Tk()
app.title("Sentes Solar Sistem")
app.geometry("500x400")

# Kullanıcı giriş fonksiyonları
def register_user():
    username = entry_username.get().upper()
    password = entry_password.get().upper()
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = %s", (username,))
    result = cursor.fetchone()
    
    if result:
        messagebox.showerror("Hata", "Bu kullanıcı adı zaten mevcut. Lütfen farklı bir kullanıcı adı seçin.")
    else:
        cursor.execute("INSERT INTO kullanici (kullanici_adi, sifre) VALUES (%s, %s)", (username, password))
        mydb.commit()
        messagebox.showinfo("Başarılı", "Kayıt işlemi başarıyla tamamlandı.")
    
    cursor.close()

def login_user():
    username = entry_username.get().upper()
    password = entry_password.get().upper()
    
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM kullanici WHERE kullanici_adi = %s AND sifre = %s", (username, password))
    result = cursor.fetchone()
    
    if result:
        messagebox.showinfo("Başarılı", f"Giriş başarılı. Hoş geldiniz, {username}")
        show_main_menu()
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı. Tekrar deneyin.")
    
    cursor.close()

def logout():
    app.quit()

def show_main_menu():
    clear_frame()
    Label(app, text="Ana Menü", font=("Helvetica", 18)).pack(pady=10)
    
    Button(app, text="Veritabanı İşlemleri", command=database_operations_menu).pack(pady=10)
    Button(app, text="Grafik İşlemleri", command=graph_operations_menu).pack(pady=10)
    Button(app, text="Excel İşlemleri", command=excel_operations_menu).pack(pady=10)
    Button(app, text="Çıkış", command=logout).pack(pady=10)

def database_operations_menu():
    clear_frame()
    Label(app, text="Veritabanı İşlemleri Menüsü", font=("Helvetica", 18)).pack(pady=10)
    
    Button(app, text="Veri Ekleme", command=data_insertion).pack(pady=10)
    Button(app, text="Veri Silme", command=data_deletion).pack(pady=10)
    Button(app, text="Veri Güncelleme", command=data_update).pack(pady=10)
    Button(app, text="Veri Listeleme", command=data_listing).pack(pady=10)
    Button(app, text="Ana Menü", command=show_main_menu).pack(pady=10)

def data_insertion():
    clear_frame()
    Label(app, text="Veri Ekleme", font=("Helvetica", 18)).pack(pady=10)
    
    def insert_data():
        sef = entry_sef.get().upper()
        yapildigi_lokasyon = entry_yapildigi_lokasyon.get().upper()
        musteri = entry_musteri.get().upper()
        calisan_isci_adet = int(entry_calisan_isci_adet.get())
        kullanilan_is_araclari = entry_kullanilan_is_araclari.get().upper()
        maliyet = float(entry_maliyet.get())
        etap = entry_etap.get().upper()
        tahmini_teslim = entry_tahmini_teslim.get().upper()
        
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM proje WHERE sef = %s", (sef,))
        existing_record = cursor.fetchone()
        
        if existing_record:
            messagebox.showerror("Hata", f"{sef} isimli proje zaten kayıtlı. Eklenemedi.")
        else:
            cursor.execute("INSERT INTO proje (sef, yapildigi_lokasyon, musteri, calisan_isci_adet, kullanilan_is_araclari, maliyet, etap, tahmini_teslim) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (sef, yapildigi_lokasyon, musteri, calisan_isci_adet, kullanilan_is_araclari, maliyet, etap, tahmini_teslim))
            mydb.commit()
            messagebox.showinfo("Başarılı", f"{sef} isimli proje başarıyla eklendi.")
        
        cursor.close()
    
    Label(app, text="Proje Şefi:").pack()
    entry_sef = Entry(app)
    entry_sef.pack()
    
    Label(app, text="Yapıldığı Lokasyon:").pack()
    entry_yapildigi_lokasyon = Entry(app)
    entry_yapildigi_lokasyon.pack()
    
    Label(app, text="Müşteri:").pack()
    entry_musteri = Entry(app)
    entry_musteri.pack()
    
    Label(app, text="Çalışan İşçi Adet:").pack()
    entry_calisan_isci_adet = Entry(app)
    entry_calisan_isci_adet.pack()
    
    Label(app, text="Kullanılan İş Araçları:").pack()
    entry_kullanilan_is_araclari = Entry(app)
    entry_kullanilan_is_araclari.pack()
    
    Label(app, text="Maliyet:").pack()
    entry_maliyet = Entry(app)
    entry_maliyet.pack()
    
    Label(app, text="Etap:").pack()
    entry_etap = Entry(app)
    entry_etap.pack()
    
    Label(app, text="Tahmini Teslim:").pack()
    entry_tahmini_teslim = Entry(app)
    entry_tahmini_teslim.pack()
    
    Button(app, text="Veri Ekle", command=insert_data).pack(pady=10)
    Button(app, text="Ana Menü", command=show_main_menu).pack(pady=10)

def data_deletion():
    clear_frame()
    Label(app, text="Veri Silme", font=("Helvetica", 18)).pack(pady=10)
    
    def delete_data():
        sef = entry_sef.get().upper()
        
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM proje WHERE sef = %s", (sef,))
        existing_record = cursor.fetchone()
        
        if existing_record:
            cursor.execute("DELETE FROM proje WHERE sef = %s", (sef,))
            mydb.commit()
            messagebox.showinfo("Başarılı", f"{sef} isimli proje başarıyla silindi.")
        else:
            messagebox.showerror("Hata", f"{sef} isimli proje bulunamadı.")
        
        cursor.close()
    
    Label(app, text="Silinecek Projenin Şefi:").pack()
    entry_sef = Entry(app)
    entry_sef.pack()
    
    Button(app, text="Veri Sil", command=delete_data).pack(pady=10)
    Button(app, text="Ana Menü", command=show_main_menu).pack(pady=10)

def data_update():
    clear_frame()
    Label(app, text="Veri Güncelleme", font=("Helvetica", 18)).pack(pady=10)
    
    def update_data():
        sef = entry_sef.get().upper()
        new_yapildigi_lokasyon = entry_yapildigi_lokasyon.get().upper()
        new_musteri = entry_musteri.get().upper()
        new_calisan_isci_adet = int(entry_calisan_isci_adet.get())
        new_kullanilan_is_araclari = entry_kullanilan_is_araclari.get().upper()
        new_maliyet = float(entry_maliyet.get())
        new_etap = entry_etap.get().upper()
        new_tahmini_teslim = entry_tahmini_teslim.get().upper()
        
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM proje WHERE sef = %s", (sef,))
        existing_record = cursor.fetchone()
        
        if existing_record:
            cursor.execute(
                "UPDATE proje SET yapildigi_lokasyon = %s, musteri = %s, calisan_isci_adet = %s, kullanilan_is_araclari = %s, maliyet = %s, etap = %s, tahmini_teslim = %s WHERE sef = %s",
                (new_yapildigi_lokasyon, new_musteri, new_calisan_isci_adet, new_kullanilan_is_araclari, new_maliyet, new_etap, new_tahmini_teslim, sef)
            )
            mydb.commit()
            messagebox.showinfo("Başarılı", f"{sef} isimli proje başarıyla güncellendi.")
        else:
            messagebox.showerror("Hata", f"{sef} isimli proje bulunamadı.")
        
        cursor.close()
    
    Label(app, text="Güncellenecek Projenin Şefi:").pack()
    entry_sef = Entry(app)
    entry_sef.pack()
    
    Label(app, text="Yeni Yapıldığı Lokasyon:").pack()
    entry_yapildigi_lokasyon = Entry(app)
    entry_yapildigi_lokasyon.pack()
    
    Label(app, text="Yeni Müşteri:").pack()
    entry_musteri = Entry(app)
    entry_musteri.pack()
    
    Label(app, text="Yeni Çalışan İşçi Adet:").pack()
    entry_calisan_isci_adet = Entry(app)
    entry_calisan_isci_adet.pack()
    
    Label(app, text="Yeni Kullanılan İş Araçları:").pack()
    entry_kullanilan_is_araclari = Entry(app)
    entry_kullanilan_is_araclari.pack()
    
    Label(app, text="Yeni Maliyet:").pack()
    entry_maliyet = Entry(app)
    entry_maliyet.pack()
    
    Label(app, text="Yeni Etap:").pack()
    entry_etap = Entry(app)
    entry_etap.pack()
    
    Label(app, text="Yeni Tahmini Teslim:").pack()
    entry_tahmini_teslim = Entry(app)
    entry_tahmini_teslim.pack()
    
    Button(app, text="Veri Güncelle", command=update_data).pack(pady=10)
    Button(app, text="Ana Menü", command=show_main_menu).pack(pady=10)

def data_listing():
    clear_frame()
    Label(app, text="Veri Listeleme", font=("Helvetica", 18)).pack(pady=10)

    def list_data():
        try:
            cursor = mydb.cursor()
            cursor.execute("SELECT * FROM proje")
            rows = cursor.fetchall()

            if not rows:
                text_area.insert(END, "Veritabanında kayıtlı veri bulunmamaktadır.\n")
            else:
                for row in rows:
                    text_area.insert(END, f"Şef: {row[1]}, Lokasyon: {row[2]}, Müşteri: {row[3]}, Çalışan İşçi Adet: {row[4]}, Kullanılan İş Araçları: {row[5]}, Maliyet: {row[6]}, Etap: {row[7]}, Tahmini Teslim: {row[8]}\n")
        
        except Exception as e:
            messagebox.showerror("Hata", f"Veri listeleme işlemi sırasında bir hata oluştu: {str(e)}")
        
        finally:
            cursor.close()

    # Scrollbar ile birlikte Text widget'ı oluştur
    text_area = Text(app)
    text_area.pack(expand=True, fill=BOTH)  

    # Scrollbar
    scroll = Scrollbar(text_area)
    scroll.pack(side=RIGHT, fill=Y)
    text_area.config(yscrollcommand=scroll.set)
    scroll.config(command=text_area.yview)

    # Verileri listeleme butonu
    Button(app, text="Verileri Listele", command=list_data).pack(pady=10)
    
    # Ana menüye geri dönme butonu
    Button(app, text="Ana Menü", command=show_main_menu).pack(pady=10)

def graph_operations_menu():
    clear_frame()
    Label(app, text="Grafik İşlemleri Menüsü", font=("Helvetica", 18)).pack(pady=10)
    
    Button(app, text="Veri Görselleştirme", command=visualize_data).pack(pady=10)
    Button(app, text="Ana Menü", command=show_main_menu).pack(pady=10)

def visualize_data():
    def plot_graph():
        cursor = mydb.cursor()
        cursor.execute("SELECT yapildigi_lokasyon, COUNT(*) FROM proje GROUP BY yapildigi_lokasyon")
        data = cursor.fetchall()
        
        locations = [item[0] for item in data]
        counts = [item[1] for item in data]
        
        fig, ax = plt.subplots()
        ax.bar(locations, counts)
        ax.set_xlabel('Yapıldığı Lokasyon')
        ax.set_ylabel('Sayı')
        ax.set_title('Proje Lokasyonlarına Göre Dağılım')
        
        canvas = FigureCanvasTkAgg(fig, master=app)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        cursor.close()
    
    plot_graph()

def excel_operations_menu():
    clear_frame()
    Label(app, text="Excel İşlemleri Menüsü", font=("Helvetica", 18)).pack(pady=10)
    
    Button(app, text="Excel Dosyasını İçe Aktar", command=import_excel).pack(pady=10)
    Button(app, text="Excel Dosyasını Dışa Aktar", command=export_excel).pack(pady=10)
    Button(app, text="Ana Menü", command=show_main_menu).pack(pady=10)

def import_excel():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Dosyaları", "*.xlsx")])
    
    if file_path:
        df = pd.read_excel(file_path)
        
        cursor = mydb.cursor()
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO proje (sef, yapildigi_lokasyon, musteri, calisan_isci_adet, kullanilan_is_araclari, maliyet, etap, tahmini_teslim) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (row['sef'].upper(), row['yapildigi_lokasyon'].upper(), row['musteri'].upper(), int(row['calisan_isci_adet']), row['kullanilan_is_araclari'].upper(), float(row['maliyet']), row['etap'].upper(), row['tahmini_teslim'].upper())
            )
        mydb.commit()
        cursor.close()
        
        messagebox.showinfo("Başarılı", "Excel dosyası başarıyla içe aktarıldı.")

def export_excel():
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Dosyaları", "*.xlsx")])
    
    if file_path:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM proje")
        rows = cursor.fetchall()
        
        df = pd.DataFrame(rows, columns=['sef', 'yapildigi_lokasyon', 'musteri', 'calisan_isci_adet', 'kullanilan_is_araclari', 'maliyet', 'etap', 'tahmini_teslim'])
        df.to_excel(file_path, index=False)
        
        cursor.close()
        
        messagebox.showinfo("Başarılı", "Veriler başarıyla Excel dosyasına aktarıldı.")

def clear_frame():
    for widget in app.winfo_children():
        widget.destroy()

# Giriş formu
Label(app, text="Kullanıcı Adı:").pack()
entry_username = Entry(app)
entry_username.pack()

Label(app, text="Şifre:").pack()
entry_password = Entry(app, show='*')
entry_password.pack()

Button(app, text="Kayıt Ol", command=register_user).pack(pady=10)
Button(app, text="Giriş Yap", command=login_user).pack(pady=10)

# Uygulamayı çalıştırma
app.mainloop()