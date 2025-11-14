import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageWin
import tempfile, os, re, win32print, win32ui, json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# ==========================
# TEMEL AYARLAR
# ==========================
DPI = 203
TMP_BMP = os.path.join(tempfile.gettempdir(), "etiket_temp.bmp")
CONFIG_FILE = "etiket_config.json"
RECORD_FILE = "gecmis_kayitlar.json"
CUSTOMER_FILE = "musteri_kayit.json"
FONT_PATHS = ["arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]

# Bu değişkenler artık load_settings() tarafından doldurulacak
FIXED_SENDER = "POSSIFY BİLGİSAYAR"
KDV_ORANI = 0.20
LOG_USER = "selcuk"
LOG_PASS = "5377"

# (İl/İlçe listesi çok uzun olduğu için kodda yer kaplamaması adına küçültülmüştür)
# (Sizin tam listeniz burada yer almalıdır)
IL_ILCE = {
    "Adana": ["Aladağ", "Ceyhan", "Çukurova", "Feke", "İmamoğlu", "Karaisalı", "Karataş", "Kozan", "Pozantı", "Saimbeyli", "Sarıçam", "Seyhan", "Tufanbeyli", "Yumurtalık", "Yüreğir"],
    "Adıyaman": ["Besni", "Çelikhan", "Gerger", "Gölbaşı", "Kahta", "Merkez", "Samsat", "Sincik", "Tut"],
    "Afyonkarahisar": ["Başmakçı", "Bayat", "Bolvadin", "Çay", "Çobanlar", "Dazkırı", "Dinar", "Emirdağ", "Evciler", "Hocalar", "İhsaniye", "İscehisar", "Kızılören", "Merkez", "Sandıklı", "Sinanpaşa", "Şuhut", "Sultandağı"],
    "Ağrı": ["Diyadin", "Doğubayazıt", "Eleşkirt", "Hamur", "Merkez", "Patnos", "Taşlıçay", "Tutak"],
    "Aksaray": ["Ağaçören", "Eskil", "Gülağaç", "Güzelyurt", "Merkez", "Ortaköy", "Sarıyahşi", "Sultanhanı"],
    "Amasya": ["Göynücek", "Gümüşhacıköy", "Hamamözü", "Merkez", "Merzifon", "Suluova", "Taşova"],
    "Ankara": ["Akyurt", "Altındağ", "Ayaş", "Bala", "Beypazarı", "Çamlıdere", "Çankaya", "Çubuk", "Elmadağ", "Etimesgut", "Evren", "Gölbaşı", "Güdül", "Haymana", "Kahramankazan", "Kalecik", "Keçiören", "Kızılcahamam", "Mamak", "Nallıhan", "Polatlı", "Pursaklar", "Şereflikoçhisar", "Sincan", "Yenimahalle"],
    "Antalya": ["Akseki", "Aksu", "Alanya", "Demre", "Döşemealtı", "Elmalı", "Finike", "Gazipaşa", "Gündoğmuş", "İbradı", "Kaş", "Kemer", "Kepez", "Konyaaltı", "Korkuteli", "Kumluca", "Manavgat", "Muratpaşa", "Serik"],
    "Ardahan": ["Çıldır", "Damal", "Göle", "Hanak", "Merkez", "Posof"],
    "Artvin": ["Ardanuç", "Arhavi", "Borçka", "Hopa", "Kemalpaşa", "Merkez", "Murgul", "Şavşat", "Yusufeli"],
    "Aydın": ["Bozdoğan", "Buharkent", "Çine", "Didim", "Efeler", "Germencik", "İncirliova", "Karacasu", "Karpuzlu", "Koçarlı", "Köşk", "Kuşadası", "Kuyucak", "Nazilli", "Söke", "Sultanhisar", "Yenipazar"],
    "Balıkesir": ["Altıeylül", "Ayvalık", "Balya", "Bandırma", "Bigadiç", "Burhaniye", "Dursunbey", "Edremit", "Erdek", "Gömeç", "Gönen", "Havran", "İvrindi", "Karesi", "Kepsut", "Manyas", "Marmara", "Savaştepe", "Sındırgı", "Susurluk"],
    "Bartın": ["Amasra", "Kurucaşile", "Merkez", "Ulus"],
    "Batman": ["Beşiri", "Gercüş", "Hasankeyf", "Kozluk", "Merkez", "Sason"],
    "Bayburt": ["Aydıntepe", "Demirözü", "Merkez"],
    "Bilecik": ["Bozüyük", "Gölpazarı", "İnhisar", "Merkez", "Osmaneli", "Pazaryeri", "Söğüt", "Yenipazar"],
    "Bingöl": ["Adaklı", "Genç", "Karlıova", "Kiğı", "Merkez", "Solhan", "Yayladere", "Yedisu"],
    "Bitlis": ["Adilcevaz", "Ahlat", "Güroymak", "Hizan", "Merkez", "Mutki", "Tatvan"],
    "Bolu": ["Dörtdivan", "Gerede", "Göynük", "Kıbrıscık", "Mengen", "Merkez", "Mudurnu", "Seben", "Yeniçağa"],
    "Burdur": ["Ağlasun", "Altınyayla", "Bucak", "Çavdır", "Çeltikçi", "Gölhisar", "Karamanlı", "Kemer", "Merkez", "Tefenni", "Yeşilova"],
    "Bursa": ["Büyükorhan", "Gemlik", "Gürsu", "Harmancık", "İnegöl", "İznik", "Karacabey", "Keles", "Kestel", "Mudanya", "Mustafakemalpaşa", "Nilüfer", "Orhaneli", "Orhangazi", "Osmangazi", "Yenişehir", "Yıldırım"],
    "Çanakkale": ["Ayvacık", "Bayramiç", "Biga", "Bozcaada", "Çan", "Eceabat", "Ezine", "Gelibolu", "Gökçeada", "Lapseki", "Merkez", "Yenice"],
    "Çankırı": ["Atkaracalar", "Bayramören", "Çerkeş", "Eldivan", "Ilgaz", "Kızılırmak", "Korgun", "Kurşunlu", "Merkez", "Orta", "Şabanözü", "Yapraklı"],
    "Çorum": ["Alaca", "Bayat", "Boğazkale", "Dodurga", "İskilip", "Kargı", "Laçin", "Mecitözü", "Merkez", "Oğuzlar", "Ortaköy", "Osmancık", "Sungurlu", "Uğurludağ"],
    "Denizli": ["Acıpayam", "Babadağ", "Baklan", "Bekilli", "Beyağaç", "Bozkurt", "Buldan", "Çal", "Çameli", "Çardak", "Çivril", "Güney", "Honaz", "Kale", "Merkezefendi", "Pamukkale", "Sarayköy", "Serinhisar", "Tavas"],
    "Diyarbakır": ["Bağlar", "Bismil", "Çermik", "Çınar", "Çüngüş", "Dicle", "Eğil", "Ergani", "Hani", "Hazro", "Kayapınar", "Kocaköy", "Kulp", "Lice", "Silvan", "Sur", "Yenişehir"],
    "Düzce": ["Akçakoca", "Çilimli", "Cumayeri", "Gölyaka", "Gümüşova", "Kaynaşlı", "Merkez", "Yığılca"],
    "Edirne": ["Enez", "Havsa", "İpsala", "Keşan", "Lalapaşa", "Meriç", "Merkez", "Süloğlu", "Uzunköprü"],
    "Elazığ": ["Ağın", "Alacakaya", "Arıcak", "Baskil", "Karakoçan", "Keban", "Kovancılar", "Maden", "Merkez", "Palu", "Sivrice"],
    "Erzincan": ["Çayırlı", "İliç", "Kemah", "Kemaliye", "Merkez", "Otlukbeli", "Refahiye", "Tercan", "Üzümlü"],
    "Erzurum": ["Aşkale", "Aziziye", "Çat", "Hınıs", "Horasan", "İspir", "Karaçoban", "Karayazı", "Köprüköy", "Narman", "Oltu", "Olur", "Palandöken", "Pasinler", "Pazaryolu", "Şenkaya", "Tekman", "Tortum", "Uzundere", "Yakutiye"],
    "Eskişehir": ["Alpu", "Beylikova", "Çifteler", "Günyüzü", "Han", "İnönü", "Mahmudiye", "Mihalgazi", "Mihalıççık", "Odunpazarı", "Sarıcakaya", "Seyitgazi", "Sivrihisar", "Tepebaşı"],
    "Gaziantep": ["Araban", "İslahiye", "Karkamış", "Nizip", "Nurdağı", "Oğuzeli", "Şahinbey", "Şehitkamil", "Yavuzeli"],
    "Giresun": ["Alucra", "Bulancak", "Çamoluk", "Çanakçı", "Dereli", "Doğankent", "Espiye", "Eynesil", "Görele", "Güce", "Keşap", "Merkez", "Piraziz", "Şebinkarahisar", "Tirebolu", "Yağlıdere"],
    "Gümüşhane": ["Kelkit", "Köse", "Kürtün", "Merkez", "Şiran", "Torul"],
    "Hakkari": ["Çukurca", "Derecik", "Merkez", "Şemdinli", "Yüksekova"],
    "Hatay": ["Altınözü", "Antakya", "Arsuz", "Belen", "Defne", "Dörtyol", "Erzin", "Hassa", "İskenderun", "Kırıkhan", "Kumlu", "Payas", "Reyhanlı", "Samandağ", "Yayladağı"],
    "Iğdır": ["Aralık", "Karakoyunlu", "Merkez", "Tuzluca"],
    "Isparta": ["Aksu", "Atabey", "Eğirdir", "Gelendost", "Gönen", "Keçiborlu", "Merkez", "Senirkent", "Sütçüler", "Şarkikaraağaç", "Uluborlu", "Yalvaç", "Yenişarbademli"],
    "İstanbul": ["Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar", "Bahçelievler", "Bakırköy", "Başakşehir", "Bayrampaşa", "Beşiktaş", "Beykoz", "Beylikdüzü", "Beyoğlu", "Büyükçekmece", "Çatalca", "Çekmeköy", "Esenler", "Esenyurt", "Eyüpsultan", "Fatih", "Gaziosmanpaşa", "Güngören", "Kadıköy", "Kağıthane", "Kartal", "Küçükçekmece", "Maltepe", "Pendik", "Sancaktepe", "Sarıyer", "Silivri", "Sultanbeyli", "Sultangazi", "Şile", "Şişli", "Tuzla", "Ümraniye", "Üsküdar", "Zeytinburnu"],
    "İzmir": ["Aliağa", "Balçova", "Bayındır", "Bayraklı", "Bergama", "Beydağ", "Bornova", "Buca", "Çeşme", "Çiğli", "Dikili", "Foça", "Gaziemir", "Güzelbahçe", "Karabağlar", "Karaburun", "Karşıyaka", "Kemalpaşa", "Kınık", "Kiraz", "Konak", "Menderes", "Menemen", "Narlıdere", "Ödemiş", "Seferihisar", "Selçuk", "Tire", "Torbalı", "Urla"],
    "Kahramanmaraş": ["Afşin", "Andırın", "Çağlayancerit", "Dulkadiroğlu", "Ekinözü", "Elbistan", "Göksun", "Nurhak", "Onikişubat", "Pazarcık", "Türkoğlu"],
    "Karabük": ["Eflani", "Eskipazar", "Merkez", "Ovacık", "Safranbolu", "Yenice"],
    "Karaman": ["Ayrancı", "Başyayla", "Ermenek", "Kazımkarabekir", "Merkez", "Sarıveliler"],
    "Kars": ["Akyaka", "Arpaçay", "Digor", "Kağızman", "Merkez", "Sarıkamış", "Selim", "Susuz"],
    "Kastamonu": ["Abana", "Ağlı", "Araç", "Azdavay", "Bozkurt", "Cide", "Çatalzeytin", "Daday", "Devrekani", "Doğanyurt", "Hanönü", "İhsangazi", "İnebolu", "Küre", "Merkez", "Pınarbaşı", "Seydiler", "Şenpazar", "Taşköprü", "Tosya"],
    "Kayseri": ["Akkışla", "Bünyan", "Develi", "Felahiye", "Hacılar", "İncesu", "Kocasinan", "Melikgazi", "Özvatan", "Pınarbaşı", "Sarıoğlan", "Sarız", "Talas", "Tomarza", "Yahyalı", "Yeşilhisar"],
    "Kilis": ["Elbeyli", "Merkez", "Musabeyli", "Polateli"],
    "Kırıkkale": ["Bahşili", "Balışeyh", "Çelebi", "Delice", "Karakeçili", "Keskin", "Merkez", "Sulakyurt", "Yahşihan"],
    "Kırklareli": ["Babaeski", "Demirköy", "Kofçaz", "Lüleburgaz", "Merkez", "Pehlivanköy", "Pınarhisar", "Vize"],
    "Kırşehir": ["Akçakent", "Akpınar", "Boztepe", "Çiçekdağı", "Kaman", "Merkez", "Mucur"],
    "Kocaeli": ["Başiskele", "Çayırova", "Darıca", "Derince", "Dilovası", "Gebze", "Gölcük", "İzmit", "Kandıra", "Karamürsel", "Kartepe", "Körfez"],
    "Konya": ["Ahırlı", "Akören", "Akşehir", "Altınekin", "Beyşehir", "Bozkır", "Cihanbeyli", "Çeltik", "Çumra", "Derebucak", "Derbent", "Doğanhisar", "Emirgazi", "Ereğli", "Güneysınır", "Hadim", "Halkapınar", "Hüyük", "Ilgın", "Kadınhanı", "Karapınar", "Karatay", "Kulu", "Meram", "Sarayönü", "Selçuklu", "Seydişehir", "Taşkent", "Tuzlukçu", "Yalıhüyük", "Yunak"],
    "Kütahya": ["Altıntaş", "Aslanapa", "Çavdarhisar", "Domaniç", "Dumlupınar", "Emet", "Gediz", "Hisarcık", "Merkez", "Pazarlar", "Şaphane", "Simav", "Tavşanlı"],
    "Malatya": ["Akçadağ", "Arapgir", "Arguvan", "Battalgazi", "Darende", "Doğanşehir", "Doğanyol", "Hekimhan", "Kale", "Kuluncak", "Pütürge", "Yazıhan", "Yeşilyurt"],
    "Manisa": ["Ahmetli", "Akhisar", "Alaşehir", "Demirci", "Gölmarmara", "Gördes", "Kırkağaç", "Köprübaşı", "Kula", "Salihli", "Sarıgöl", "Saruhanlı", "Şehzadeler", "Selendi", "Soma", "Turgutlu", "Yunusemre"],
    "Mardin": ["Artuklu", "Dargeçit", "Derik", "Kızıltepe", "Mazıdağı", "Midyat", "Nusaybin", "Ömerli", "Savur", "Yeşilli"],
    "Mersin": ["Akdeniz", "Anamur", "Aydıncık", "Bozyazı", "Çamlıyayla", "Erdemli", "Gülnar", "Mezitli", "Mut", "Silifke", "Tarsus", "Toroslar", "Yenişehir"],
    "Muğla": ["Bodrum", "Dalaman", "Datça", "Fethiye", "Kavaklıdere", "Köyceğiz", "Marmaris", "Menteşe", "Milas", "Ortaca", "Seydikemer", "Ula", "Yatağan"],
    "Muş": ["Bulanık", "Hasköy", "Korkut", "Malazgirt", "Merkez", "Varto"],
    "Nevşehir": ["Acıgöl", "Avanos", "Derinkuyu", "Gülşehir", "Hacıbektaş", "Kozaklı", "Merkez", "Ürgüp"],
    "Niğde": ["Altunhisar", "Bor", "Çamardı", "Çiftlik", "Merkez", "Ulukışla"],
    "Ordu": ["Akkuş", "Altınordu", "Aybastı", "Çamaş", "Çatalpınar", "Çaybaşı", "Fatsa", "Gölköy", "Gülyalı", "Gürgentepe", "İkizce", "Kabadüz", "Kabataş", "Korgan", "Kumru", "Mesudiye", "Perşembe", "Ulubey", "Ünye"],
    "Osmaniye": ["Bahçe", "Düziçi", "Hasanbeyli", "Kadirli", "Merkez", "Sumbas", "Toprakkale"],
    "Rize": ["Ardeşen", "Çamlıhemşin", "Çayeli", "Derepazarı", "Fındıklı", "Güneysu", "Hemşin", "İkizdere", "İyidere", "Kalkandere", "Merkez", "Pazar"],
    "Sakarya": ["Adapazarı", "Akyazı", "Arifiye", "Erenler", "Ferizli", "Geyve", "Hendek", "Karapürçek", "Karasu", "Kaynarca", "Kocaali", "Pamukova", "Sapanca", "Serdivan", "Söğütlü", "Taraklı"],
    "Samsun": ["19 Mayıs", "Alaçam", "Asarcık", "Atakum", "Ayvacık", "Bafra", "Canik", "Çarşamba", "Havza", "İlkadım", "Kavak", "Ladik", "Salıpazarı", "Tekkeköy", "Terme", "Vezirköprü", "Yakakent"],
    "Şanlıurfa": ["Akçakale", "Birecik", "Bozova", "Ceylanpınar", "Eyyübiye", "Halfeti", "Haliliye", "Harran", "Hilvan", "Karaköprü", "Siverek", "Suruç", "Viranşehir"],
    "Siirt": ["Baykan", "Eruh", "Kurtalan", "Merkez", "Pervari", "Şirvan", "Tillo"],
    "Sinop": ["Ayancık", "Boyabat", "Dikmen", "Durağan", "Erfelek", "Gerze", "Merkez", "Saraydüzü", "Türkeli"],
    "Şırnak": ["Beytüşşebap", "Cizre", "Güçlükonak", "İdil", "Merkez", "Silopi", "Uludere"],
    "Sivas": ["Akıncılar", "Altınyayla", "Divriği", "Doğanşar", "Gemerek", "Gölova", "Gürün", "Hafik", "İmranlı", "Kangal", "Koyulhisar", "Merkez", "Suşehri", "Şarkışla", "Ulaş", "Yıldızeli", "Zara"],
    "Tekirdağ": ["Çerkezköy", "Çorlu", "Ergene", "Hayrabolu", "Kapaklı", "Malkara", "Marmaraereğlisi", "Muratlı", "Saray", "Süleymanpaşa", "Şarköy"],
    "Tokat": ["Almus", "Artova", "Başçiftlik", "Erbaa", "Merkez", "Niksar", "Pazar", "Reşadiye", "Sulusaray", "Turhal", "Yeşilyurt", "Zile"],
    "Trabzon": ["Akçaabat", "Araklı", "Arsin", "Beşikdüzü", "Çarşıbaşı", "Çaykara", "Dernekpazarı", "Düzköy", "Hayrat", "Köprübaşı", "Maçka", "Of", "Ortahisar", "Sürmene", "Şalpazarı", "Tonya", "Vakfıkebir", "Yomra"],
    "Tunceli": ["Çemişgezek", "Hozat", "Mazgirt", "Merkez", "Nazımiye", "Ovacık", "Pertek", "Pülümür"],
    "Uşak": ["Banaz", "Eşme", "Karahallı", "Merkez", "Sivaslı", "Ulubey"],
    "Van": ["Bahçesaray", "Başkale", "Çaldıran", "Çatak", "Edremit", "Erciş", "Gevaş", "Gürpınar", "İpekyolu", "Muradiye", "Özalp", "Saray", "Tuşba"],
    "Yalova": ["Altınova", "Armutlu", "Çiftlikköy", "Çınarcık", "Merkez", "Termal"],
    "Yozgat": ["Akdağmadeni", "Aydıncık", "Boğazlıyan", "Çandır", "Çayıralan", "Çekerek", "Kadışehri", "Merkez", "Saraykent", "Sarıkaya", "Şefaatli", "Sorgun", "Yenifakılı", "Yerköy"],
    "Zonguldak": ["Alaplı", "Çaycuma", "Devrek", "Ereğli", "Gökçebey", "Kilimli", "Kozlu", "Merkez"]
}


# ==========================
# YARDIMCI FONKSİYONLAR
# ==========================
def mm_to_px(mm, dpi=DPI):
    try:
        mm = str(mm).replace(",", ".").replace("mm", "").strip()
        return int((float(mm) / 25.4) * dpi)
    except Exception:
        raise ValueError("Etiket ölçüleri sayısal olmalıdır.")

def load_font(size):
    for fp in FONT_PATHS:
        try: return ImageFont.truetype(fp, size)
        except Exception: continue
    return ImageFont.load_default()

def sanitize_text(text):
    if text is None: return ""
    s = str(text); s = re.sub(r'[\r\n\t]+', ' ', s); s = re.sub(r'\s{2,}', ' ', s)
    return s.strip()

def wrap_text(text, draw, font, max_width):
    text = sanitize_text(text)
    if not text: return [""]
    words = text.split()
    lines = []; line = ""
    for w in words:
        if not line:
            line = w; continue
        test = f"{line} {w}"
        try: w_px = draw.textlength(test, font=font)
        except: w_px = draw.textsize(test, font=font)[0]
        if w_px <= max_width: line = test
        else: lines.append(line); line = w
    lines.append(line)
    return lines

# ==========================
# KAYIT VE VERİ FONKSİYONLARI
# ==========================
def save_record(data):
    try:
        with open(RECORD_FILE, "r", encoding="utf-8") as f: records = json.load(f)
    except: records = []
    data["id"] = (records[-1]["id"] + 1) if records else 1
    data["type"] = data.get("type", "servis")
    data["tarih"] = datetime.now().strftime("%d.%m.%Y %H:%M")
    records.append(data)
    with open(RECORD_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

def load_records():
    try:
        with open(RECORD_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return []

def save_customer(data, customer_type):
    try:
        with open(CUSTOMER_FILE, "r", encoding="utf-8") as f: customers = json.load(f)
    except: customers = {"servis": {}, "kargo": {}}
    
    if customer_type == "servis":
        key = data.get("İletişim No", "")
        if not key: return
        customers["servis"][key] = {
            "Müşteri Adı Soyadı": data.get("Müşteri Adı Soyadı", ""),
            "İşletme Adı": data.get("İşletme Adı", ""),
            "İletişim No": key, "İl": data.get("İl", ""), "İlçe": data.get("İlçe", ""),
            "Son İşlem Tarihi": datetime.now().strftime("%d.%m.%Y")
        }
    elif customer_type == "kargo":
        key = data.get("İletişim", "")
        if not key: return
        customers["kargo"][key] = {
            "Müşteri Adı Soyadı": data.get("Müşteri Adı Soyadı", ""),
            "İşletme Adı": data.get("İşletme Adı", ""),
            "İletişim": key, "İl": data.get("İl", ""), "İlçe": data.get("İlçe", ""),
            "Son İşlem Tarihi": datetime.now().strftime("%d.%m.%Y")
        }
        
    with open(CUSTOMER_FILE, "w", encoding="utf-8") as f:
        json.dump(customers, f, ensure_ascii=False, indent=2)

def load_customers():
    try:
        with open(CUSTOMER_FILE, "r", encoding="utf-8") as f: return json.load(f)
    except: return {"servis": {}, "kargo": {}}

# ==========================
# ETİKET OLUŞTURMA (FONT İYİLEŞTİRMELİ)
# ==========================
def create_service_label_image(data, width_mm, height_mm, align="left"):
    width_px, height_px = mm_to_px(width_mm, dpi=DPI), mm_to_px(height_mm, dpi=DPI)
    img = Image.new("RGB", (width_px, height_px), "white")
    draw = ImageDraw.Draw(img)
    margin = int(width_px * 0.05); usable_w = width_px - 2 * margin; spacing = 0

    adsoyad = sanitize_text(data.get("Müşteri Adı Soyadı", "")).upper()
    isletme = sanitize_text(data.get("İşletme Adı", "")).upper()
    iletisim = sanitize_text(data.get("İletişim No", "")).upper()
    il = sanitize_text(data.get("İl", "")).upper()
    ilce = sanitize_text(data.get("İlçe", "")).upper()
    yapılan_islem = sanitize_text(data.get("Yapılan İşlem", "")).upper()
    ucret = sanitize_text(data.get("Ücret", "")).upper()
    seri = sanitize_text(data.get("Seri Numarası", "")).upper()
    ililce = f"{ilce} / {il}" if (ilce and il) else (ilce or il)
    durum = sanitize_text(data.get("Durum", "")).upper()
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M").upper()

    infos = []
    if adsoyad: infos.append(adsoyad)
    if isletme: infos.append(isletme)
    if iletisim: infos.append(iletisim)
    if ililce: infos.append(ililce)
    if yapılan_islem: infos.append(yapılan_islem)
    if ucret:
        if not ucret.endswith("$+KDV"): infos.append(f"{ucret}$+KDV")
        else: infos.append(ucret)
    if seri: infos.append(seri)
    if durum: infos.append(durum)
    if tarih: infos.append(tarih)

    max_font = max(10, int(height_px * 0.18)); min_font = 8; font_size = max_font
    while font_size >= min_font:
        font = load_font(font_size); item_spacing = max(2, int(font_size * 0.25))
        total_h = 0; fits = True
        valid_infos = [val for val in infos if val]; num = len(valid_infos)
        for val in valid_infos:
            lines = wrap_text(val, draw, font, usable_w)
            if lines and lines != [""]:
                text = '\n'.join(lines)
                bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
                h = bbox[3] - bbox[1]; total_h += h
        if num > 1: total_h += item_spacing * (num - 1)
        if total_h + margin * 2 > height_px: fits = False
        if fits: break
        font_size -= 1

    font = load_font(font_size); item_spacing = max(2, int(font_size * 0.25))
    valid_infos = [val for val in infos if val]; num = len(valid_infos); total_h = 0
    line_heights = []
    for val in valid_infos:
        lines = wrap_text(val, draw, font, usable_w)
        text = '\n'.join(lines)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        h = bbox[3] - bbox[1]; line_heights.append(h); total_h += h
    if num > 1: total_h += item_spacing * (num - 1)
    y = max(margin, (height_px - total_h) // 2)
    for i, val in enumerate(valid_infos):
        lines = wrap_text(val, draw, font, usable_w); text = '\n'.join(lines)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        w = bbox[2] - bbox[0]; h = line_heights[i]
        x = (width_px - w) // 2 if align == "center" else margin
        if y + h > height_px - margin: break
        draw.multiline_text((x, y), text, font=font, fill="black", spacing=spacing, align="center" if align == "center" else "left")
        y += h + item_spacing
    return img

def create_shipping_label_image(data, width_mm, height_mm, align="left"):
    width_px, height_px = mm_to_px(width_mm, dpi=DPI), mm_to_px(height_mm, dpi=DPI)
    img = Image.new("RGB", (width_px, height_px), "white")
    draw = ImageDraw.Draw(img); margin = int(width_px * 0.05)
    usable_w = width_px - 2 * margin; y = 0

    firma = sanitize_text(data.get("Kargo Firması", "")).upper()
    odeme = sanitize_text(data.get("Ödeme Tipi", "")).upper()
    adsoyad = sanitize_text(data.get("Müşteri Adı Soyadı", "")).upper()
    isletme = sanitize_text(data.get("İşletme Adı", "")).upper()
    iletisim = sanitize_text(data.get("İletişim", "")).upper()
    il = sanitize_text(data.get("İl", "")).upper()
    ilce = sanitize_text(data.get("İlçe", "")).upper()
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M").upper()
    sender_text = f"GÖNDERİCİ: {FIXED_SENDER}"
    ililce = f"{ilce} / {il}" if (ilce and il) else (ilce or il)

    infos = [("firma", firma), ("odeme", odeme), ("alici", adsoyad), ("isletme", isletme),
             ("iletisim", iletisim), ("il_ilce", ililce), ("tarih", tarih)]
    proportions = {"firma": 0.12, "odeme": 0.10, "alici": 0.12, "isletme": 0.10,
                   "iletisim": 0.10, "il_ilce": 0.10, "tarih": 0.09, "sender": 0.09}
    min_font_px = 8; min_sender_font_px = 8
    font_sizes = {key: max(min_font_px, int(height_px * proportions[key])) for key in proportions}
    item_spacing = int(height_px * 0.04)

    while True:
        heights = []
        if firma: band_h = int(height_px * 0.14); heights.append(band_h + item_spacing)
        if odeme: box_h = int(height_px * 0.12); heights.append(box_h + item_spacing)
        for key, val in infos[2:]:
            if not val: continue
            font = load_font(font_sizes[key]); lines = wrap_text(val, draw, font, usable_w)
            text = '\n'.join(lines)
            bbox = draw.multiline_textbbox((0,0), text, font=font, spacing=0)
            heights.append(bbox[3] - bbox[1] + item_spacing)
        heights.append(font_sizes["sender"] * 1.2 + item_spacing)
        total_h = sum(heights) + margin
        if total_h <= height_px or min(font_sizes.values()) <= min_sender_font_px: break
        for k in font_sizes:
            if font_sizes[k] > min_sender_font_px:
                font_sizes[k] = max(min_sender_font_px, font_sizes[k] - 1)
        if all(f <= min_sender_font_px for f in font_sizes.values()): break
             
    if firma:
        font = load_font(font_sizes["firma"]); band_h = int(height_px * 0.14)
        draw.rectangle([0, 0, width_px, band_h], fill="black")
        tw = draw.textlength(firma, font=font); th = font.size
        draw.text(((width_px - tw) / 2, (band_h - th) / 2), firma, font=font, fill="white")
        y = band_h + item_spacing
    else: y = margin
    if odeme:
        font = load_font(font_sizes["odeme"]); box_h = int(height_px * 0.12)
        draw.rectangle([margin, y, width_px - margin, y + box_h], outline="black", width=3)
        tw = draw.textlength(odeme, font=font); th = font.size
        draw.text(((width_px - tw) / 2, y + (box_h - th) / 2), odeme, font=font, fill="black")
        y += box_h + item_spacing
    for key, val in infos[2:]:
        if not val: continue
        font = load_font(font_sizes[key]); lines = wrap_text(val, draw, font, usable_w)
        text = '\n'.join(lines)
        bbox = draw.multiline_textbbox((0,0), text, font=font, spacing=0)
        h = bbox[3] - bbox[1]; w = bbox[2] - bbox[0]
        x = (width_px - w) // 2 if align=="center" else margin
        if y + h > height_px - margin: break
        draw.multiline_text((x, y), text, font=font, fill="black", spacing=0, align="center" if align=="center" else "left")
        y += h + item_spacing
    sender_font = load_font(font_sizes["sender"]); sender_h = sender_font.size * 1.2
    y = height_px - sender_h - margin
    draw.line([margin, y - item_spacing // 2, width_px - margin, y - item_spacing // 2], fill="black", width=2)
    sender_x = margin if align == "left" else (width_px - draw.textlength(sender_text, font=sender_font)) // 2
    draw.text((sender_x, y), sender_text, font=sender_font, fill="black")
    return img

def create_exchange_label_image(data, width_mm, height_mm, align="left"):
    width_px, height_px = mm_to_px(width_mm, dpi=DPI), mm_to_px(height_mm, dpi=DPI)
    img = Image.new("RGB", (width_px, height_px), "white")
    draw = ImageDraw.Draw(img); margin = int(width_px * 0.05)
    usable_w = width_px - 2 * margin; spacing = 0

    usd = sanitize_text(data.get("dolar", "")).upper()
    kur = sanitize_text(data.get("kur", "")).upper()
    tl = sanitize_text(data.get("tl", "")).upper()
    kdv = sanitize_text(data.get("kdv", "")).upper()
    tl_kdv = sanitize_text(data.get("tl_kdv", "")).upper()
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M").upper()

    infos = []
    if usd: infos.append(f"DOLAR TUTARI: {usd}$")
    if kur: infos.append(f"DOLAR KURU: {kur} TL")
    if tl: infos.append(f"TL KARŞILIĞI: {tl} TL")
    if kdv: infos.append(f"KDV (%{int(KDV_ORANI*100)}): {kdv} TL")
    if tl_kdv: infos.append(f"KDV DAHİL: {tl_kdv} TL")
    if tarih: infos.append(tarih)

    max_font = max(10, int(height_px * 0.18)); min_font = 8; font_size = max_font
    while font_size >= min_font:
        font = load_font(font_size); item_spacing = max(2, int(font_size * 0.25))
        total_h = 0; fits = True; num = len(infos)
        for val in infos:
            lines = wrap_text(val, draw, font, usable_w); text = '\n'.join(lines)
            bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
            h = bbox[3] - bbox[1]; total_h += h
        if num > 1: total_h += item_spacing * (num - 1)
        if total_h + margin * 2 > height_px: fits = False
        if fits: break
        font_size -= 1

    font = load_font(font_size); item_spacing = max(2, int(font_size * 0.25))
    num = len(infos); total_h = 0; line_heights = []
    for val in infos:
        lines = wrap_text(val, draw, font, usable_w); text = '\n'.join(lines)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        h = bbox[3] - bbox[1]; line_heights.append(h); total_h += h
    if num > 1: total_h += item_spacing * (num - 1)
    y = max(margin, (height_px - total_h) // 2)

    for i, val in enumerate(infos):
        lines = wrap_text(val, draw, font, usable_w); text = '\n'.join(lines)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        w = bbox[2] - bbox[0]; h = line_heights[i]
        x = (width_px - w) // 2 if align == "center" else margin
        if y + h > height_px - margin: break
        draw.multiline_text((x, y), text, font=font, fill="black", spacing=spacing, align="left" if align == "left" else "center")
        y += h + item_spacing
    return img

def create_box_content_label_image(data, width_mm, height_mm, align="left"):
    width_px, height_px = mm_to_px(width_mm, dpi=DPI), mm_to_px(height_mm, dpi=DPI)
    img = Image.new("RGB", (width_px, height_px), "white")
    draw = ImageDraw.Draw(img); margin = int(width_px * 0.05)
    usable_w = width_px - 2 * margin; spacing = 0

    selected = data.get("selected", []); infos = [opt.upper() for opt in selected]
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M").upper(); infos.append(tarih)

    max_font = max(10, int(height_px * 0.18)); min_font = 8; font_size = max_font
    while font_size >= min_font:
        font = load_font(font_size); item_spacing = max(2, int(font_size * 0.25))
        total_h = 0; fits = True
        valid_infos = [val for val in infos if val]; num = len(valid_infos)
        for val in valid_infos:
            lines = wrap_text(val, draw, font, usable_w); text = '\n'.join(lines)
            bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
            h = bbox[3] - bbox[1]; total_h += h
        if num > 1: total_h += item_spacing * (num - 1)
        if total_h + margin * 2 > height_px: fits = False
        if fits: break
        font_size -= 1
        
    font = load_font(font_size); item_spacing = max(2, int(font_size * 0.25))
    valid_infos = [val for val in infos if val]; num = len(valid_infos); total_h = 0
    line_heights = []
    for val in valid_infos:
        lines = wrap_text(val, draw, font, usable_w); text = '\n'.join(lines)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        h = bbox[3] - bbox[1]; line_heights.append(h); total_h += h
    if num > 1: total_h += item_spacing * (num - 1)
    y = max(margin, (height_px - total_h) // 2)

    for i, val in enumerate(valid_infos):
        lines = wrap_text(val, draw, font, usable_w); text = '\n'.join(lines)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing)
        w = bbox[2] - bbox[0]; h = line_heights[i]
        x = (width_px - w) // 2 if align == "center" else margin
        if y + h > height_px - margin: break
        draw.multiline_text((x, y), text, font=font, fill="black", spacing=spacing, align="center" if align == "center" else "left")
        y += h + item_spacing
    return img

def print_image_to_printer(pil_image, printer_name, copies=1):
    pil_image.save(TMP_BMP, "BMP")
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hdc = win32ui.CreateDC() # <-- DÜZELTME (win3n32ui -> win32ui)
        hdc.CreatePrinterDC(printer_name)
        hdc.StartDoc("Etiket Yazdırma"); bmp = Image.open(TMP_BMP)
        for _ in range(copies):
            hdc.StartPage()
            dib = ImageWin.Dib(bmp)
            dib.draw(hdc.GetHandleOutput(), (0, 0, bmp.width, bmp.height))
            hdc.EndPage()
        hdc.EndDoc(); hdc.DeleteDC()
    finally:
        if 'bmp' in locals(): bmp.close()
        win32print.ClosePrinter(hPrinter)
        if os.path.exists(TMP_BMP): os.remove(TMP_BMP)

def get_usd_try_from_tcmb(satis=False):
    try:
        url = "https://www.tcmb.gov.tr/kurlar/today.xml"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        tree = ET.fromstring(response.content)
        for currency in tree.findall("Currency"):
            if currency.attrib.get("Kod") == "USD":
                usd_value = currency.find("ForexSelling" if satis else "ForexBuying").text
                return float(usd_value.replace(",", "."))
    except Exception:
        return None

# ==========================
# ANA UYGULAMA SINIFI
# ==========================
class LabelApp:
    def __init__(self, root):
        self.root = root
        self.load_settings() # Ayarları en başta yükle (tema ve global değişkenler için)
        
        self.root.title("Etiket Yazdırma v9.4 - Gelişmiş Ayarlar ve Hata Düzeltmeleri")
        self.root.state('zoomed')
        
        self.notebook = tb.Notebook(root, bootstyle="primary")
        self.tab_service = ttk.Frame(self.notebook)
        self.tab_shipping = ttk.Frame(self.notebook)
        self.tab_exchange = ttk.Frame(self.notebook)
        self.tab_box_content = ttk.Frame(self.notebook)
        self.tab_customer_log = ttk.Frame(self.notebook)
        self.tab_log = ttk.Frame(self.notebook)
        self.tab_settings = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_service, text="Servis Etiketi")
        self.notebook.add(self.tab_shipping, text="Kargo Etiketi")
        self.notebook.add(self.tab_exchange, text="Döviz Kuru Hesaplama")
        self.notebook.add(self.tab_box_content, text="Kutu İçeriği")
        self.notebook.add(self.tab_customer_log, text="Müşteri Kayıtları")
        self.notebook.add(self.tab_log, text="Geçmiş Log")
        self.notebook.add(self.tab_settings, text="Ayarlar")
        self.notebook.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        self.setup_service_tab()
        self.setup_shipping_tab()
        self.setup_exchange_tab()
        self.setup_box_content_tab()
        self.setup_customer_log_tab()
        self.setup_log_tab()
        self.setup_settings_tab()
        self.setup_right_panel() # Panel en son oluşturulmalı

        self.last_service_image = None
        self.last_shipping_image = None
        self.last_exchange_image = None
        self.last_box_content_image = None
        
        self.load_settings_into_fields() # Ayar alanlarını doldur
        self.auto_update_usd_kur()
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        # === DÜZELTME: Bağlantı (bind) en sona taşındı ===
        # Bu, self.right_frame'in oluşturulmasını garanti eder.
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def toggle_fullscreen(self, event=None): self.root.state('zoomed')
    def exit_fullscreen(self, event=None): self.root.state('normal')

    # DÜZELTİLDİ: Sekme değişince sağ panelin kaybolması
    def on_tab_changed(self, event=None):
        img_to_show = None
        try:
            # right_frame henüz oluşturulmadıysa (ilk açılışta) bir şey yapma
            if not hasattr(self, 'right_frame'):
                return
                
            tab = self.notebook.index(self.notebook.select())
            
            # 4: Müşteri, 5: Log, 6: Ayarlar
            if tab in [4, 5, 6]:
                if self.right_frame.winfo_ismapped():
                    self.right_frame.pack_forget() # Paneli gizle
            else:
                if not self.right_frame.winfo_ismapped():
                    self.right_frame.pack(side="right", fill="y", expand=False) # Paneli göster
                
                if tab == 0:   img_to_show = self.last_service_image
                elif tab == 1: img_to_show = self.last_shipping_image
                elif tab == 2: img_to_show = self.last_exchange_image
                elif tab == 3: img_to_show = self.last_box_content_image
            
            self.show_image_on_preview(img_to_show)
        except Exception as e:
             print(f"Sekme değiştirme hatası: {e}")
             if hasattr(self, 'right_frame') and not self.right_frame.winfo_ismapped():
                 self.right_frame.pack(side="right", fill="y", expand=False)
             
    def show_image_on_preview(self, pil_image):
        if not hasattr(self, 'preview_canvas'): return
        self.preview_canvas.delete("all")
        if pil_image is None:
            self.preview_canvas.image = None
            return
        
        preview = pil_image.copy()
        preview.thumbnail((380, 380), Image.Resampling.LANCZOS)
        tkimg = ImageTk.PhotoImage(preview)
        self.preview_canvas.create_image(190, 190, image=tkimg, anchor="center")
        self.preview_canvas.image = tkimg

    def setup_service_tab(self):
        frm = ttk.Frame(self.tab_service, padding=12)
        frm.pack(side="left", fill="y", padx=20)
        labels = ["Müşteri Adı Soyadı", "İşletme Adı", "İletişim No", "Yapılan İşlem", "Ücret", "Seri Numarası"]
        self.entries_service = {}
        for i, lab in enumerate(labels):
            tb.Label(frm, text=lab, bootstyle="primary").grid(row=i, column=0, sticky="w", pady=6)
            ent = tb.Entry(frm, width=50, bootstyle="info")
            ent.grid(row=i, column=1, pady=6, padx=6, columnspan=3)
            self.entries_service[lab] = ent

        tb.Label(frm, text="İl Ara", bootstyle="primary").grid(row=6, column=0, sticky="w", pady=6)
        self.service_il_search = tb.Entry(frm, width=30, bootstyle="info")
        self.service_il_search.grid(row=6, column=1, sticky="w", columnspan=2)
        tb.Button(frm, text="Bul", bootstyle="info", command=self.search_service_il).grid(row=6, column=3, padx=4)
        self.service_il_search.bind("<Return>", lambda e: self.search_service_il())

        tb.Label(frm, text="İl Seç", bootstyle="primary").grid(row=7, column=0, sticky="w", pady=6)
        self.il_var = tk.StringVar()
        self.il_combo = tb.Combobox(frm, textvariable=self.il_var, values=[""], width=40, bootstyle="info", state="readonly")
        self.il_combo.grid(row=7, column=1, sticky="w", columnspan=3)
        self.il_combo.bind("<<ComboboxSelected>>", self.update_service_ilce_combo)

        tb.Label(frm, text="İlçe Ara", bootstyle="primary").grid(row=8, column=0, sticky="w", pady=6)
        self.service_ilce_search = tb.Entry(frm, width=30, bootstyle="info")
        self.service_ilce_search.grid(row=8, column=1, sticky="w", columnspan=2)
        tb.Button(frm, text="Bul", bootstyle="info", command=self.search_service_ilce).grid(row=8, column=3, padx=4)
        self.service_ilce_search.bind("<Return>", lambda e: self.search_service_ilce())

        tb.Label(frm, text="İlçe Seç", bootstyle="primary").grid(row=9, column=0, sticky="w", pady=6)
        self.ilce_var = tk.StringVar()
        self.ilce_combo = tb.Combobox(frm, textvariable=self.ilce_var, width=40, bootstyle="info", state="readonly")
        self.ilce_combo.grid(row=9, column=1, sticky="w", columnspan=3)
        self.search_service_il()

        tb.Label(frm, text="Durum", bootstyle="primary").grid(row=10, column=0, sticky="w", pady=6)
        self.durum_var = tk.StringVar()
        self.service_durum_combo = tb.Combobox(frm, textvariable=self.durum_var, values=self.service_durum_opsiyonlar, width=40, bootstyle="info", state="readonly")
        self.service_durum_combo.grid(row=10, column=1, sticky="w", columnspan=3)

        tb.Label(frm, text="Etiket Genişliği (mm)", bootstyle="primary").grid(row=11, column=0, sticky="w", pady=6)
        self.service_w = tb.Entry(frm, width=10, bootstyle="info")
        self.service_w.grid(row=11, column=1, sticky="w")

        tb.Label(frm, text="Etiket Yüksekliği (mm)", bootstyle="primary").grid(row=12, column=0, sticky="w", pady=6)
        self.service_h = tb.Entry(frm, width=10, bootstyle="info")
        self.service_h.grid(row=12, column=1, sticky="w")

        tb.Label(frm, text="Hizalama", bootstyle="primary").grid(row=13, column=0, sticky="w", pady=6)
        self.service_align = tk.StringVar(value="left")
        tb.Combobox(frm, textvariable=self.service_align, values=["left", "center"], width=10, bootstyle="info", state="readonly").grid(row=13, column=1, sticky="w")

    def search_service_il(self):
        typed = self.service_il_search.get()
        if typed == '': data = list(IL_ILCE.keys())
        else: data = [item for item in IL_ILCE.keys() if typed.lower() in item.lower()]
        self.il_combo['values'] = data
        if data: self.il_combo.set(data[0])
        else: self.il_combo.set("")
        self.update_service_ilce_combo(None)

    def update_service_ilce_combo(self, event):
        il = self.il_var.get()
        if il in IL_ILCE:
            self.ilce_combo['values'] = IL_ILCE[il]
            if IL_ILCE[il]: self.ilce_combo.set(IL_ILCE[il][0])
            else: self.ilce_combo.set("")
        else: self.ilce_combo['values'] = []; self.ilce_combo.set("")
        self.service_ilce_search.delete(0, tk.END)

    def search_service_ilce(self):
        typed = self.service_ilce_search.get()
        il = self.il_var.get()
        if il in IL_ILCE:
            if typed == '': data = IL_ILCE[il]
            else: data = [item for item in IL_ILCE[il] if typed.lower() in item.lower()]
            self.ilce_combo['values'] = data
            if data: self.ilce_combo.set(data[0])
            else: self.ilce_combo.set("")
        else: messagebox.showwarning("Uyarı", "Lütfen önce geçerli bir İl seçin.")

    def setup_shipping_tab(self):
        frm = ttk.Frame(self.tab_shipping, padding=12)
        frm.pack(side="left", fill="y", padx=20)
        fields = ["Müşteri Adı Soyadı", "İşletme Adı", "İletişim"]
        self.entries_shipping = {}
        for i, lab in enumerate(fields):
            tb.Label(frm, text=lab, bootstyle="primary").grid(row=i, column=0, sticky="w", pady=6)
            ent = tb.Entry(frm, width=50, bootstyle="info")
            ent.grid(row=i, column=1, pady=6, padx=6, columnspan=3)
            self.entries_shipping[lab] = ent

        tb.Label(frm, text="İl Ara", bootstyle="primary").grid(row=3, column=0, sticky="w", pady=6)
        self.shipping_il_search = tb.Entry(frm, width=30, bootstyle="info")
        self.shipping_il_search.grid(row=3, column=1, sticky="w", columnspan=2)
        tb.Button(frm, text="Bul", bootstyle="info", command=self.search_shipping_il).grid(row=3, column=3, padx=4)
        self.shipping_il_search.bind("<Return>", lambda e: self.search_shipping_il())

        tb.Label(frm, text="İl Seç", bootstyle="primary").grid(row=4, column=0, sticky="w", pady=6)
        self.shipping_il_var = tk.StringVar()
        self.shipping_il_combo = tb.Combobox(frm, textvariable=self.shipping_il_var, values=[""], width=40, bootstyle="info", state="readonly")
        self.shipping_il_combo.grid(row=4, column=1, sticky="w", columnspan=3)
        self.shipping_il_combo.bind("<<ComboboxSelected>>", self.update_shipping_ilce_combo)

        tb.Label(frm, text="İlçe Ara", bootstyle="primary").grid(row=5, column=0, sticky="w", pady=6)
        self.shipping_ilce_search = tb.Entry(frm, width=30, bootstyle="info")
        self.shipping_ilce_search.grid(row=5, column=1, sticky="w", columnspan=2)
        tb.Button(frm, text="Bul", bootstyle="info", command=self.search_shipping_ilce).grid(row=5, column=3, padx=4)
        self.shipping_ilce_search.bind("<Return>", lambda e: self.search_shipping_ilce())

        tb.Label(frm, text="İlçe Seç", bootstyle="primary").grid(row=6, column=0, sticky="w", pady=6)
        self.shipping_ilce_var = tk.StringVar()
        self.shipping_ilce_combo = tb.Combobox(frm, textvariable=self.shipping_ilce_var, width=40, bootstyle="info", state="readonly")
        self.shipping_ilce_combo.grid(row=6, column=1, sticky="w", columnspan=3)
        self.search_shipping_il()

        tb.Label(frm, text="Kargo Firması", bootstyle="primary").grid(row=7, column=0, sticky="w", pady=6)
        self.kargo_var = tk.StringVar()
        self.kargo_combo = tb.Combobox(frm, textvariable=self.kargo_var, values=self.kargo_firmalari_list, width=40, bootstyle="info", state="readonly")
        self.kargo_combo.grid(row=7, column=1, sticky="w", columnspan=3)

        tb.Label(frm, text="Ödeme Tipi", bootstyle="primary").grid(row=8, column=0, sticky="w", pady=6)
        self.odeme_var = tk.StringVar()
        self.odeme_combo = tb.Combobox(frm, textvariable=self.odeme_var, values=self.odeme_tipleri_list, width=40, bootstyle="info", state="readonly")
        self.odeme_combo.grid(row=8, column=1, sticky="w", columnspan=3)

        tb.Label(frm, text="Etiket Genişliği (mm)", bootstyle="primary").grid(row=9, column=0, sticky="w", pady=6)
        self.shipping_w = tb.Entry(frm, width=10, bootstyle="info")
        self.shipping_w.grid(row=9, column=1, sticky="w")

        tb.Label(frm, text="Etiket Yüksekliği (mm)", bootstyle="primary").grid(row=10, column=0, sticky="w", pady=6)
        self.shipping_h = tb.Entry(frm, width=10, bootstyle="info")
        self.shipping_h.grid(row=10, column=1, sticky="w")

        tb.Label(frm, text="Hizalama", bootstyle="primary").grid(row=11, column=0, sticky="w", pady=6)
        self.shipping_align = tk.StringVar(value="left")
        tb.Combobox(frm, textvariable=self.shipping_align, values=["left", "center"], width=10, bootstyle="info", state="readonly").grid(row=11, column=1, sticky="w")

    def search_shipping_il(self):
        typed = self.shipping_il_search.get()
        if typed == '': data = list(IL_ILCE.keys())
        else: data = [item for item in IL_ILCE.keys() if typed.lower() in item.lower()]
        self.shipping_il_combo['values'] = data
        if data: self.shipping_il_combo.set(data[0])
        else: self.shipping_il_combo.set("")
        self.update_shipping_ilce_combo(None)

    def update_shipping_ilce_combo(self, event):
        il = self.shipping_il_var.get()
        if il in IL_ILCE:
            self.shipping_ilce_combo['values'] = IL_ILCE[il]
            if IL_ILCE[il]: self.shipping_ilce_combo.set(IL_ILCE[il][0])
            else: self.shipping_ilce_combo.set("")
        else: self.shipping_ilce_combo['values'] = []; self.shipping_ilce_combo.set("")
        self.shipping_ilce_search.delete(0, tk.END)

    def search_shipping_ilce(self):
        typed = self.shipping_ilce_search.get()
        il = self.shipping_il_var.get()
        if il in IL_ILCE:
            if typed == '': data = IL_ILCE[il]
            else: data = [item for item in IL_ILCE[il] if typed.lower() in item.lower()]
            self.shipping_ilce_combo['values'] = data
            if data: self.shipping_ilce_combo.set(data[0])
            else: self.shipping_ilce_combo.set("")
        else: messagebox.showwarning("Uyarı", "Lütfen önce geçerli bir İl seçin.")

    def setup_exchange_tab(self):
        frm = ttk.Frame(self.tab_exchange, padding=12)
        frm.pack(side="left", fill="y", padx=20)

        input_frame = tb.Frame(frm); input_frame.pack(fill="x", pady=5)
        tb.Label(input_frame, text="Dolar Tutarı ($)", bootstyle="primary", width=15).grid(row=0, column=0, sticky="w", pady=6)
        self.dolar_entry = tb.Entry(input_frame, width=30, bootstyle="info")
        self.dolar_entry.grid(row=0, column=1, pady=6, padx=6, sticky="w")
        tb.Label(input_frame, text="Dolar Kuru (TL)", bootstyle="primary", width=15).grid(row=1, column=0, sticky="w", pady=6)
        self.kur_entry = tb.Entry(input_frame, width=30, bootstyle="info")
        self.kur_entry.grid(row=1, column=1, pady=6, padx=6, sticky="w")

        btn_frame = tb.Frame(frm); btn_frame.pack(fill="x", pady=5, anchor="w")
        tb.Button(btn_frame, text="Satış Fiyatını Yükle", bootstyle="success", command=self.load_usd_satis_kur).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Hesapla ve Göster", bootstyle="success", command=self.calculate_exchange).pack(side="left", padx=5)

        result_frame = tb.Labelframe(frm, text="Sonuç", bootstyle="info", padding=10)
        result_frame.pack(fill="x", expand=True, pady=10, anchor="w")
        self.exchange_result = tk.StringVar()
        tb.Label(result_frame, textvariable=self.exchange_result, font=("Arial", 13, "bold"), bootstyle="info", justify="left").pack(anchor="w")

        self.exchange_kur_label = tb.Label(frm, font=("Arial", 10, "italic"), bootstyle="warning", wraplength=450, justify="left")
        self.exchange_kur_label.pack(fill="x", pady=10, anchor="w")

        settings_frame = tb.Frame(frm); settings_frame.pack(fill="x", pady=20, anchor="w")
        tb.Label(settings_frame, text="Etiket Genişliği (mm)", bootstyle="primary").grid(row=0, column=0, sticky="w", pady=6)
        self.exchange_w = tb.Entry(settings_frame, width=10, bootstyle="info")
        self.exchange_w.grid(row=0, column=1, sticky="w", padx=5)
        tb.Label(settings_frame, text="Etiket Yüksekliği (mm)", bootstyle="primary").grid(row=1, column=0, sticky="w", pady=6)
        self.exchange_h = tb.Entry(settings_frame, width=10, bootstyle="info")
        self.exchange_h.grid(row=1, column=1, sticky="w", padx=5)
        tb.Label(settings_frame, text="Hizalama", bootstyle="primary").grid(row=2, column=0, sticky="w", pady=6)
        self.exchange_align = tk.StringVar(value="left")
        tb.Combobox(settings_frame, textvariable=self.exchange_align, values=["left", "center"], width=10, bootstyle="info", state="readonly").grid(row=2, column=1, sticky="w", padx=5)

    def setup_box_content_tab(self):
        frm = ttk.Frame(self.tab_box_content, padding=12)
        frm.pack(side="left", fill="y", padx=20)
        
        self.box_vars_frame = tb.Frame(frm)
        self.box_vars_frame.pack(anchor="w")
        self.box_vars = self.create_checkbuttons(self.box_vars_frame, self.box_options_list)

        settings_frame = tb.Frame(frm); settings_frame.pack(fill="x", pady=20, anchor="w")
        tb.Label(settings_frame, text="Etiket Genişliği (mm)", bootstyle="primary").grid(row=0, column=0, sticky="w", pady=6)
        self.box_w = tb.Entry(settings_frame, width=10, bootstyle="info")
        self.box_w.grid(row=0, column=1, sticky="w", padx=5)
        tb.Label(settings_frame, text="Etiket Yüksekliği (mm)", bootstyle="primary").grid(row=1, column=0, sticky="w", pady=6)
        self.box_h = tb.Entry(settings_frame, width=10, bootstyle="info")
        self.box_h.grid(row=1, column=1, sticky="w", padx=5)
        tb.Label(settings_frame, text="Hizalama", bootstyle="primary").grid(row=2, column=0, sticky="w", pady=6)
        self.box_align = tk.StringVar(value="left")
        tb.Combobox(settings_frame, textvariable=self.box_align, values=["left", "center"], width=10, bootstyle="info", state="readonly").grid(row=2, column=1, sticky="w", padx=5)

    def create_checkbuttons(self, parent, options):
        vars_list = []
        for i, opt in enumerate(options):
            var = tk.BooleanVar(value=False)
            vars_list.append(var)
            tb.Checkbutton(parent, text=opt, variable=var, bootstyle="primary").grid(row=i, column=0, sticky="w", pady=6)
        return vars_list

    def setup_customer_log_tab(self):
        frm = ttk.Frame(self.tab_customer_log, padding=12)
        frm.pack(fill="both", expand=True)

        tb.Button(frm, text="Kayıtları Yenile", command=self.refresh_customer_logs, bootstyle="info").pack(anchor="ne", pady=5)
        
        self.customer_notebook = tb.Notebook(frm, bootstyle="primary")
        self.customer_notebook.pack(fill="both", expand=True, pady=5)
        
        self.cust_tab_servis = ttk.Frame(self.customer_notebook)
        self.cust_tab_kargo = ttk.Frame(self.customer_notebook)
        self.customer_notebook.add(self.cust_tab_servis, text="Servis Müşterileri")
        self.customer_notebook.add(self.cust_tab_kargo, text="Kargo Müşterileri")
        
        self.servis_tree = self.create_customer_tree(self.cust_tab_servis, ("Ad Soyad", "İşletme", "İletişim", "İl/İlçe", "Tarih"))
        self.kargo_tree = self.create_customer_tree(self.cust_tab_kargo, ("Ad Soyad", "İşletme", "İletişim", "İl/İlçe", "Tarih"))
        
        self.refresh_customer_logs()

    def create_customer_tree(self, parent, columns):
        frm = ttk.Frame(parent); frm.pack(fill="both", expand=True)
        cols_id = [c.lower().replace(" ", "").replace("/", "") for c in columns]
        tree = tb.Treeview(frm, columns=cols_id, show="headings", height=20, bootstyle="info")
        for i, col in enumerate(columns):
            tree.heading(cols_id[i], text=col)
            tree.column(cols_id[i], width=150, anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        
        yscroll = tb.Scrollbar(frm, orient="vertical", command=tree.yview, bootstyle="primary-round")
        yscroll.pack(side="right", fill="y")
        tree.configure(yscrollcommand=yscroll.set)
        xscroll = tb.Scrollbar(frm, orient="horizontal", command=tree.xview, bootstyle="primary-round")
        xscroll.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=xscroll.set)
        
        tree.tag_configure('odd', background='#f2f2f2')
        tree.tag_configure('even', background='#e6f7ff')
        return tree

    def refresh_customer_logs(self):
        customers = load_customers()
        
        for i in self.servis_tree.get_children(): self.servis_tree.delete(i)
        for i, (key, data) in enumerate(customers.get("servis", {}).items()):
            tag = 'odd' if i % 2 == 0 else 'even'
            self.servis_tree.insert("", "end", values=(
                data.get("Müşteri Adı Soyadı", ""), data.get("İşletme Adı", ""),
                data.get("İletişim No", ""), f"{data.get('İlçe', '')} / {data.get('İl', '')}",
                data.get("Son İşlem Tarihi", "")
            ), tags=(tag,))
            
        for i in self.kargo_tree.get_children(): self.kargo_tree.delete(i)
        for i, (key, data) in enumerate(customers.get("kargo", {}).items()):
            tag = 'odd' if i % 2 == 0 else 'even'
            self.kargo_tree.insert("", "end", values=(
                data.get("Müşteri Adı Soyadı", ""), data.get("İşletme Adı", ""),
                data.get("İletişim", ""), f"{data.get('İlçe', '')} / {data.get('İl', '')}",
                data.get("Son İşlem Tarihi", "")
            ), tags=(tag,))

    # GÜNCELLENDİ: Ayarlar Sekmesi (Güvenlik + Yeni Ayarlar)
    def setup_settings_tab(self):
        frm = ttk.Frame(self.tab_settings, padding=20)
        frm.pack(fill="y", anchor="n")
        
        # --- Genel Ayarlar ---
        general_frame = tb.Labelframe(frm, text="Genel Ayarlar", padding=10, bootstyle="info")
        general_frame.grid(row=0, column=0, pady=10, sticky="ew")

        tb.Label(general_frame, text="Uygulama Teması", bootstyle="primary").grid(row=0, column=0, sticky="w", pady=6)
        self.theme_var = tk.StringVar()
        self.theme_combo = tb.Combobox(general_frame, textvariable=self.theme_var, values=['cosmo', 'litera', 'darkly', 'superhero', 'cyborg', 'vapor'], width=20, bootstyle="info", state="readonly")
        self.theme_combo.grid(row=0, column=1, sticky="w", padx=10)

        tb.Label(general_frame, text="Sabit Gönderici Adı", bootstyle="primary").grid(row=1, column=0, sticky="w", pady=6)
        self.sender_entry = tb.Entry(general_frame, width=22, bootstyle="info")
        self.sender_entry.grid(row=1, column=1, sticky="w", padx=10)
        
        tb.Label(general_frame, text="KDV Oranı (Örn: 0.20)", bootstyle="primary").grid(row=2, column=0, sticky="w", pady=6)
        self.kdv_entry = tb.Entry(general_frame, width=22, bootstyle="info")
        self.kdv_entry.grid(row=2, column=1, sticky="w", padx=10)
        
        tb.Label(general_frame, text="Yazıcı DPI", bootstyle="primary").grid(row=3, column=0, sticky="w", pady=6)
        self.dpi_entry = tb.Entry(general_frame, width=22, bootstyle="info")
        self.dpi_entry.grid(row=3, column=1, sticky="w", padx=10)

        self.auto_save_cust_var = tk.BooleanVar(value=True)
        tb.Checkbutton(general_frame, text="Yazdırırken Müşteriyi Otomatik Kaydet", variable=self.auto_save_cust_var, bootstyle="primary").grid(row=4, column=0, columnspan=2, sticky="w", pady=10)

        # --- Varsayılan Değerler ---
        defaults_frame = tb.Labelframe(frm, text="Varsayılan Etiket Boyutları", padding=10, bootstyle="info")
        defaults_frame.grid(row=1, column=0, pady=10, sticky="ew")

        tb.Label(defaults_frame, text="Servis (Genişlik mm)", bootstyle="primary").grid(row=0, column=0, sticky="w", pady=6)
        self.service_def_w = tb.Entry(defaults_frame, width=10, bootstyle="info")
        self.service_def_w.grid(row=0, column=1, sticky="w", padx=10)
        tb.Label(defaults_frame, text="Servis (Yükseklik mm)", bootstyle="primary").grid(row=1, column=0, sticky="w", pady=6)
        self.service_def_h = tb.Entry(defaults_frame, width=10, bootstyle="info")
        self.service_def_h.grid(row=1, column=1, sticky="w", padx=10)
        
        tb.Label(defaults_frame, text="Kargo (Genişlik mm)", bootstyle="primary").grid(row=2, column=0, sticky="w", pady=6)
        self.kargo_def_w = tb.Entry(defaults_frame, width=10, bootstyle="info")
        self.kargo_def_w.grid(row=2, column=1, sticky="w", padx=10)
        tb.Label(defaults_frame, text="Kargo (Yükseklik mm)", bootstyle="primary").grid(row=3, column=0, sticky="w", pady=6)
        self.kargo_def_h = tb.Entry(defaults_frame, width=10, bootstyle="info")
        self.kargo_def_h.grid(row=3, column=1, sticky="w", padx=10)
        
        tb.Label(defaults_frame, text="Döviz (Genişlik mm)", bootstyle="primary").grid(row=4, column=0, sticky="w", pady=6)
        self.doviz_def_w = tb.Entry(defaults_frame, width=10, bootstyle="info")
        self.doviz_def_w.grid(row=4, column=1, sticky="w", padx=10)
        tb.Label(defaults_frame, text="Döviz (Yükseklik mm)", bootstyle="primary").grid(row=5, column=0, sticky="w", pady=6)
        self.doviz_def_h = tb.Entry(defaults_frame, width=10, bootstyle="info")
        self.doviz_def_h.grid(row=5, column=1, sticky="w", padx=10)
        
        tb.Label(defaults_frame, text="Kutu (Genişlik mm)", bootstyle="primary").grid(row=6, column=0, sticky="w", pady=6)
        self.kutu_def_w = tb.Entry(defaults_frame, width=10, bootstyle="info")
        self.kutu_def_w.grid(row=6, column=1, sticky="w", padx=10)
        tb.Label(defaults_frame, text="Kutu (Yükseklik mm)", bootstyle="primary").grid(row=7, column=0, sticky="w", pady=6)
        self.kutu_def_h = tb.Entry(defaults_frame, width=10, bootstyle="info")
        self.kutu_def_h.grid(row=7, column=1, sticky="w", padx=10)

        # --- Kaydetme ve Admin Butonu ---
        btn_frame = tb.Frame(frm)
        btn_frame.grid(row=2, column=0, pady=20, sticky="ew")
        tb.Button(btn_frame, text="AYARLARI KAYDET VE UYGULA", bootstyle="success", command=self.save_settings).pack(side="left", fill="x", expand=True, padx=5)
        tb.Button(btn_frame, text="ADMİN AYARLARI", bootstyle="danger", command=self.open_admin_settings).pack(side="left", fill="x", expand=True, padx=5)

        # --- Liste Ayarları ---
        list_frame = tb.Labelframe(frm, text="Liste Ayarları", padding=10, bootstyle="info")
        list_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=20, pady=10)
        
        tb.Label(list_frame, text="Servis Durum Seçenekleri (Her biri yeni satırda)").pack(anchor="w")
        self.servis_durum_text = tb.Text(list_frame, width=40, height=5, font=("Arial", 10))
        self.servis_durum_text.pack(fill="x", expand=True, pady=5)
        
        tb.Label(list_frame, text="Kutu İçeriği Seçenekleri (Her biri yeni satırda)").pack(anchor="w")
        self.kutu_icerik_text = tb.Text(list_frame, width=40, height=5, font=("Arial", 10))
        self.kutu_icerik_text.pack(fill="x", expand=True, pady=5)
        
        tb.Label(list_frame, text="Kargo Firmaları (Her biri yeni satırda)").pack(anchor="w")
        self.kargo_firmalari_text = tb.Text(list_frame, width=40, height=5, font=("Arial", 10))
        self.kargo_firmalari_text.pack(fill="x", expand=True, pady=5)
        
        tb.Label(list_frame, text="Ödeme Tipleri (Her biri yeni satırda)").pack(anchor="w")
        self.odeme_tipleri_text = tb.Text(list_frame, width=40, height=5, font=("Arial", 10))
        self.odeme_tipleri_text.pack(fill="x", expand=True, pady=5)

    # YENİ: Güvenli Admin Ayarları Penceresi
    def open_admin_settings(self):
        password = simpledialog.askstring("Admin Girişi", "Lütfen admin şifresini girin:", show='*')
        if password != LOG_PASS:
            messagebox.showerror("Hata", "Şifre yanlış!")
            return
            
        # Şifre doğruysa, yeni pencere aç
        win_admin = tb.Toplevel(self.root)
        win_admin.title("Güvenli Admin Ayarları")
        win_admin.geometry("400x200")
        win_admin.transient(self.root) # Ana pencerenin üstünde
        win_admin.grab_set() # Diğer pencereleri kitle
        
        frm = tb.Frame(win_admin, padding=20)
        frm.pack(fill="both", expand=True)
        
        tb.Label(frm, text="Log Kullanıcı Adı", bootstyle="primary").grid(row=0, column=0, sticky="w", pady=10)
        user_entry = tb.Entry(frm, width=25, bootstyle="info")
        user_entry.grid(row=0, column=1, padx=10)
        user_entry.insert(0, LOG_USER)
        
        tb.Label(frm, text="Log Şifre", bootstyle="primary").grid(row=1, column=0, sticky="w", pady=10)
        pass_entry = tb.Entry(frm, width=25, bootstyle="info")
        pass_entry.grid(row=1, column=1, padx=10)
        pass_entry.insert(0, LOG_PASS)
        
        def save_admin_changes():
            global LOG_USER, LOG_PASS
            new_user = user_entry.get().strip()
            new_pass = pass_entry.get().strip()
            
            if not new_user or not new_pass:
                messagebox.showwarning("Uyarı", "Kullanıcı adı ve şifre boş olamaz.", parent=win_admin)
                return
                
            LOG_USER = new_user
            LOG_PASS = new_pass
            
            # Değişiklikleri ana config'e de yansıt
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f: config = json.load(f)
            except: config = {}
            
            config["log_user"] = new_user
            config["log_pass"] = new_pass
            
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
            messagebox.showinfo("Başarılı", "Admin bilgileri güncellendi.", parent=win_admin)
            win_admin.destroy()

        tb.Button(frm, text="Kaydet", bootstyle="success", command=save_admin_changes).grid(row=2, column=0, columnspan=2, pady=20)

    # GÜNCELLENDİ: Ayarları Kaydetme
    def save_settings(self):
        global FIXED_SENDER, KDV_ORANI, DPI
        
        theme = self.theme_var.get()
        sender = self.sender_entry.get().strip()
        kdv_str = self.kdv_entry.get().strip()
        dpi_str = self.dpi_entry.get().strip()
        auto_save = self.auto_save_cust_var.get()
        
        config = {
            "theme": theme, "sender": sender, "kdv_rate": kdv_str, "dpi": dpi_str,
            "auto_save_customer": auto_save,
            "service_def_w": self.service_def_w.get(), "service_def_h": self.service_def_h.get(),
            "kargo_def_w": self.kargo_def_w.get(), "kargo_def_h": self.kargo_def_h.get(),
            "doviz_def_w": self.doviz_def_w.get(), "doviz_def_h": self.doviz_def_h.get(),
            "kutu_def_w": self.kutu_def_w.get(), "kutu_def_h": self.kutu_def_h.get(),
            "durum_options": [l.strip() for l in self.servis_durum_text.get("1.0", tk.END).split("\n") if l.strip()],
            "kutu_options": [l.strip() for l in self.kutu_icerik_text.get("1.0", tk.END).split("\n") if l.strip()],
            "kargo_options": [l.strip() for l in self.kargo_firmalari_text.get("1.0", tk.END).split("\n") if l.strip()],
            "odeme_options": [l.strip() for l in self.odeme_tipleri_text.get("1.0", tk.END).split("\n") if l.strip()],
            "last_printer": self.cmb_printer.get(),
            "log_user": LOG_USER, # Global'den al, modal'da değiştirildi
            "log_pass": LOG_PASS  # Global'den al, modal'da değiştirildi
        }
        
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
            
        # Ayarları global değişkenlere ve anlık kullanıma uygula
        if theme: self.root.style.theme_use(theme)
        if sender: FIXED_SENDER = sender
        try: KDV_ORANI = float(kdv_str)
        except: KDV_ORANI = 0.20
        try: DPI = int(dpi_str)
        except: DPI = 203
        
        # Listeleri ve widget'ları anlık güncelle
        self.service_durum_opsiyonlar = config["durum_options"]
        self.service_durum_combo['values'] = self.service_durum_opsiyonlar
        self.box_options_list = config["kutu_options"]
        for widget in self.box_vars_frame.winfo_children(): widget.destroy()
        self.box_vars = self.create_checkbuttons(self.box_vars_frame, self.box_options_list)
        self.kargo_firmalari_list = config["kargo_options"]
        self.kargo_combo['values'] = self.kargo_firmalari_list
        self.odeme_tipleri_list = config["odeme_options"]
        self.odeme_combo['values'] = self.odeme_tipleri_list

        messagebox.showinfo("Tamam", "Ayarlar kaydedildi ve uygulandı.")

    # GÜNCELLENDİ: Ayarları Yükleme (Başlangıç)
    def load_settings(self):
        global FIXED_SENDER, KDV_ORANI, LOG_USER, LOG_PASS, DPI
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f: config = json.load(f)
        except: config = {}
            
        self.root.style.theme_use(config.get("theme", "cosmo"))
        FIXED_SENDER = config.get("sender", "POSSIFY BİLGİSAYAR")
        LOG_USER = config.get("log_user", "selcuk")
        LOG_PASS = config.get("log_pass", "5377")
        try: KDV_ORANI = float(config.get("kdv_rate", "0.20"))
        except: KDV_ORANI = 0.20
        try: DPI = int(config.get("dpi", "203"))
        except: DPI = 203
        
        self.service_durum_opsiyonlar = config.get("durum_options", ["ÖDEME BEKLENİYOR", "CARİ BEKLENİYOR", "GARANTİ KAPSAMINDA ONARILDI"])
        self.box_options_list = config.get("kutu_options", ["ADAPTÖR VE USB KABLO VAR.", "ADAPTÖR VE USB KABLO YOK."])
        self.kargo_firmalari_list = config.get("kargo_options", ["YURTİÇİ KARGO", "MNG KARGO", "ARAS KARGO", "SÜRAT KARGO"])
        self.odeme_tipleri_list = config.get("odeme_options", ["PEŞİN ÖDEME", "ÜCRET ALICI"])
        self.auto_save_cust_var_val = config.get("auto_save_customer", True)


    # GÜNCELLENDİ: Ayarları Yükleme (Alanlara Doldurma)
    def load_settings_into_fields(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f: config = json.load(f)
        except: config = {}

        # Ayarlar Sekmesi
        self.theme_var.set(config.get("theme", "cosmo"))
        self.sender_entry.insert(0, config.get("sender", FIXED_SENDER))
        self.kdv_entry.insert(0, config.get("kdv_rate", str(KDV_ORANI)))
        self.dpi_entry.insert(0, config.get("dpi", str(DPI)))
        self.auto_save_cust_var.set(config.get("auto_save_customer", True))
        
        self.service_def_w.insert(0, config.get("service_def_w", "60"))
        self.service_def_h.insert(0, config.get("service_def_h", "40"))
        self.kargo_def_w.insert(0, config.get("kargo_def_w", "60"))
        self.kargo_def_h.insert(0, config.get("kargo_def_h", "40"))
        self.doviz_def_w.insert(0, config.get("doviz_def_w", "60")) # YENİ
        self.doviz_def_h.insert(0, config.get("doviz_def_h", "40")) # YENİ
        self.kutu_def_w.insert(0, config.get("kutu_def_w", "60"))   # YENİ
        self.kutu_def_h.insert(0, config.get("kutu_def_h", "40"))   # YENİ
        
        self.servis_durum_text.insert("1.0", "\n".join(self.service_durum_opsiyonlar))
        self.kutu_icerik_text.insert("1.0", "\n".join(self.box_options_list))
        self.kargo_firmalari_text.insert("1.0", "\n".join(self.kargo_firmalari_list))
        self.odeme_tipleri_text.insert("1.0", "\n".join(self.odeme_tipleri_list))
        
        # Diğer Sekmeler (Varsayılan değerleri bas)
        self.service_w.insert(0, config.get("service_def_w", "60"))
        self.service_h.insert(0, config.get("service_def_h", "40"))
        self.shipping_w.insert(0, config.get("kargo_def_w", "60"))
        self.shipping_h.insert(0, config.get("kargo_def_h", "40"))
        self.exchange_w.insert(0, config.get("doviz_def_w", "60"))
        self.exchange_h.insert(0, config.get("doviz_def_h", "40"))
        self.box_w.insert(0, config.get("kutu_def_w", "60"))
        self.box_h.insert(0, config.get("kutu_def_h", "40"))
        
        # Kayıtlı yazıcıyı yükle
        last_printer = config.get("last_printer", "")
        if last_printer and last_printer in self.cmb_printer['values']:
            self.cmb_printer.set(last_printer)
        elif self.cmb_printer['values']:
            try: self.cmb_printer.set(win32print.GetDefaultPrinter())
            except: self.cmb_printer.set(self.cmb_printer['values'][0])

    def setup_log_tab(self):
        frm = ttk.Frame(self.tab_log, padding=12)
        frm.pack(side="top", fill="both", expand=True)
        self.log_search_frame = ttk.Frame(frm)
        self.log_search_frame.pack(side="top", fill="x", pady=10)
        tb.Label(self.log_search_frame, text="Arama (Numara veya İsim):", bootstyle="info").pack(side="left", padx=4)
        self.log_search_entry = tb.Entry(self.log_search_frame, width=30, bootstyle="info")
        self.log_search_entry.pack(side="left", padx=2)
        tb.Button(self.log_search_frame, text="Ara", bootstyle="success", command=self.log_search).pack(side="left", padx=6)
        self.log_search_entry.bind("<Return>", lambda e: self.log_search())

        self.log_login_frame = ttk.Frame(frm)
        self.log_login_frame.pack(side="top", pady=10)
        tb.Label(self.log_login_frame, text="Kullanıcı Adı:", bootstyle="info").grid(row=0, column=0, sticky="e", padx=4)
        self.log_user_entry = tb.Entry(self.log_login_frame, width=20, bootstyle="info")
        self.log_user_entry.grid(row=0, column=1, padx=4)
        tb.Label(self.log_login_frame, text="Şifre:", bootstyle="info").grid(row=0, column=2, sticky="e", padx=4)
        self.log_pass_entry = tb.Entry(self.log_login_frame, width=20, show="*", bootstyle="info")
        self.log_pass_entry.grid(row=0, column=3, padx=4)
        tb.Button(self.log_login_frame, text="Giriş Yap", bootstyle="success", command=self.log_login_check).grid(row=0, column=4, padx=8)
        self.log_pass_entry.bind("<Return>", lambda e: self.log_login_check())

        self.log_table_frame = ttk.Frame(frm)
        self.log_table_frame.pack(side="top", fill="both", expand=True)
        self.log_table = None
        self.log_access_granted = False

    def log_login_check(self):
        user = self.log_user_entry.get().strip()
        pw = self.log_pass_entry.get().strip()
        if user == LOG_USER and pw == LOG_PASS:
            self.log_access_granted = True
            self.show_log_table(load_records())
        else:
            self.log_access_granted = False
            messagebox.showerror("Yetkisiz", "Kullanıcı adı veya şifre hatalı.")

    def show_log_table(self, records):
        if self.log_table: self.log_table.destroy()
        COLS = ("id", "tip", "ad", "isletme", "iletisim", "ililce", "islem", "ucret", "durum", "tarih")
        self.log_table = tb.Treeview(self.log_table_frame, columns=COLS, show="headings", height=20, bootstyle="info")
        for col in COLS:
            self.log_table.heading(col, text=col.upper())
            self.log_table.column(col, width=130, anchor="w")
        self.log_table.column("id", width=50, anchor="center")
        self.log_table.column("tip", width=80, anchor="center")
        self.log_table.pack(side="left", fill="both", expand=True)

        yscroll = tb.Scrollbar(self.log_table_frame, orient="vertical", command=self.log_table.yview, bootstyle="primary-round")
        yscroll.pack(side="right", fill="y")
        self.log_table.configure(yscrollcommand=yscroll.set)
        xscroll = tb.Scrollbar(self.log_table_frame, orient="horizontal", command=self.log_table.xview, bootstyle="primary-round")
        xscroll.pack(side="bottom", fill="x")
        self.log_table.configure(xscrollcommand=xscroll.set)

        self.log_table.tag_configure('odd', background='#f2f2f2')
        self.log_table.tag_configure('even', background='#e6f7ff')
        
        sorted_records = sorted(records, key=lambda x: x.get('id', 0), reverse=True)

        for i, rec in enumerate(sorted_records):
            tag = 'odd' if i % 2 == 0 else 'even'
            ililce = f"{rec.get('İlçe','')} / {rec.get('İl','')}"
            self.log_table.insert("", "end", values=(
                rec.get("id", ""), rec.get("type", ""),
                rec.get("Müşteri Adı Soyadı", rec.get("dolar", "")),
                rec.get("İşletme Adı", rec.get("kur", "")),
                rec.get("İletişim No", rec.get("İletişim", rec.get("tl", ""))),
                ililce, rec.get("Yapılan İşlem", ""),
                rec.get("Ücret", rec.get("kdv", "")),
                rec.get("Durum", rec.get("tl_kdv", "")),
                rec.get("tarih", "")
            ), tags=(tag,))

        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Satırı Kopyala", command=lambda: self.copy_selected_row())
        def on_right_click(event):
            iid = self.log_table.identify_row(event.y)
            if iid: self.log_table.selection_set(iid); menu.post(event.x_root, event.y_root)
        self.log_table.bind("<Button-3>", on_right_click)
        def on_double_click(event):
            sel = self.log_table.selection()
            if sel: self.show_detail_modal(self.log_table.item(sel[0])["values"])
        self.log_table.bind("<Double-1>", on_double_click)

    def show_detail_modal(self, values):
        win = tb.Toplevel(self.root); win.title("Kayıt Detayları"); win.geometry("420x520")
        fields = ["Numara", "Tip", "Ad Soyad/Dolar", "İşletme/Kur", "İletişim/TL", "İl/İlçe", "Yapılan İşlem", "Ücret/KDV", "Durum/KDV Dahil", "Tarih"]
        for i, v in enumerate(values):
            tb.Label(win, text=f"{fields[i]}:", font=("Arial", 12, "bold"), bootstyle="primary").pack(anchor="w", pady=8, padx=12)
            tb.Label(win, text=str(v), font=("Arial", 12), bootstyle="info", wraplength=400, justify="left").pack(anchor="w", pady=2, padx=36)
        tb.Button(win, text="Kopyala", bootstyle="success", command=lambda: self.copy_detail(values)).pack(pady=18)
        tb.Button(win, text="Kapat", bootstyle="danger", command=win.destroy).pack(pady=8)

    def copy_selected_row(self):
        sel = self.log_table.selection()
        if sel:
            vals = self.log_table.item(sel[0])["values"]
            self.root.clipboard_clear(); self.root.clipboard_append(" | ".join(str(v) for v in vals))
            messagebox.showinfo("Kopyalandı", "Satır bilgileri panoya kopyalandı.")

    def copy_detail(self, values):
        self.root.clipboard_clear(); self.root.clipboard_append(" | ".join(str(v) for v in values))
        messagebox.showinfo("Kopyalandı", "Kayıt bilgileri panoya kopyalandı.")

    def log_search(self):
        if not self.log_access_granted:
            messagebox.showwarning("Giriş", "Lütfen önce giriş yapınız.")
            return
        q = self.log_search_entry.get().strip().lower()
        records = load_records(); filtered = []
        for rec in records:
            if not q: filtered.append(rec)
            elif q.isdigit() and str(rec.get("id","")) == q: filtered.append(rec)
            elif q in str(rec.get("Müşteri Adı Soyadı","")).lower(): filtered.append(rec)
            elif q in str(rec.get("İletişim No","")).lower(): filtered.append(rec)
            elif q in str(rec.get("İletişim","")).lower(): filtered.append(rec)
        self.show_log_table(filtered)

    def setup_right_panel(self):
        self.right_frame = ttk.Frame(self.root, width=400)
        self.right_frame.pack(side="right", fill="y", expand=False)
        self.right_frame.pack_propagate(0)

        frm = ttk.Frame(self.right_frame, padding=16)
        frm.pack(fill="both", expand=True)
        tb.Label(frm, text="Yazıcı Seç", font=("Arial", 11, "bold"), bootstyle="primary").pack(anchor="w")
        printers = [p[2] for p in win32print.EnumPrinters(2)]
        self.cmb_printer = tb.Combobox(frm, values=printers, width=40, bootstyle="info", state="readonly")
        self.cmb_printer.pack(anchor="w", pady=8)
        
        tb.Label(frm, text="Kopya Sayısı", bootstyle="primary").pack(anchor="w", pady=(8,0))
        self.copy_var = tk.IntVar(value=1)
        tb.Spinbox(frm, from_=1, to=100, textvariable=self.copy_var, width=8, bootstyle="info").pack(anchor="w", pady=8)

        tb.Button(frm, text="Önizleme Oluştur", bootstyle="success", command=self.on_preview).pack(fill="x", pady=8)
        tb.Button(frm, text="Yazdır", bootstyle="success", command=self.on_print).pack(fill="x", pady=8)
        tb.Button(frm, text="Formu Temizle", bootstyle="warning", command=self.clear_form).pack(fill="x", pady=8)

        tb.Label(frm, text="Önizleme", font=("Arial", 14, "bold"), bootstyle="primary").pack(anchor="nw", pady=(12,8))
        self.preview_canvas = tk.Canvas(frm, width=380, height=380, bg="white", relief="solid")
        self.preview_canvas.pack(fill="x", expand=False, padx=8, pady=8)

    def on_preview(self):
        tab = self.notebook.index(self.notebook.select())
        img = None
        try:
            if tab == 0:
                width = self.service_w.get(); height = self.service_h.get()
                data = {k: v.get() for k, v in self.entries_service.items()}
                data["Durum"] = self.durum_var.get()
                data["İl"] = self.il_var.get(); data["İlçe"] = self.ilce_var.get()
                img = create_service_label_image(data, width, height, self.service_align.get())
                save_data = dict(data); save_data["type"] = "servis"
                save_record(save_data)
                # === DÜZELTME: self.save_customer -> save_customer ===
                if self.auto_save_cust_var.get(): save_customer(data, "servis")
                self.last_service_image = img
            elif tab == 1:
                width = self.shipping_w.get(); height = self.shipping_h.get()
                data = {k: v.get() for k, v in self.entries_shipping.items()}
                data["Kargo Firması"] = self.kargo_var.get(); data["Ödeme Tipi"] = self.odeme_var.get()
                data["İl"] = self.shipping_il_var.get(); data["İlçe"] = self.shipping_ilce_var.get()
                img = create_shipping_label_image(data, width, height, self.shipping_align.get())
                save_data = dict(data); save_data["type"] = "kargo"
                save_record(save_data)
                # === DÜZELTME: self.save_customer -> save_customer ===
                if self.auto_save_cust_var.get(): save_customer(data, "kargo")
                self.last_shipping_image = img
            elif tab == 2:
                width = self.exchange_w.get(); height = self.exchange_h.get()
                # === DÜZELTME: Donma sorununu çözmek için önce hesapla ===
                calculated_data = self.calculate_exchange() # Önce hesapla
                if calculated_data is None: return # Hata varsa dur
                
                data = {"dolar": self.dolar_entry.get(), "kur": self.kur_entry.get()}
                data.update(calculated_data) # Hesaplanan veriyi ekle
                
                img = create_exchange_label_image(data, width, height, self.exchange_align.get())
                save_data = dict(data); save_data["type"] = "doviz"
                save_record(save_data); self.last_exchange_image = img
            elif tab == 3:
                width = self.box_w.get(); height = self.box_h.get()
                selected = [self.box_options_list[i] for i, var in enumerate(self.box_vars) if var.get()]
                data = {"selected": selected}
                img = create_box_content_label_image(data, width, height, self.box_align.get())
                save_data = dict(data); save_data["type"] = "kutu_iceriği"
                save_record(save_data); self.last_box_content_image = img
            else: return
        except Exception as e:
            messagebox.showerror("Hata", f"Önizleme hatası:\n{e}"); return

        if img: self.show_image_on_preview(img)

    def on_print(self):
        printer = self.cmb_printer.get()
        if not printer: messagebox.showwarning("Uyarı", "Lütfen yazıcı seçin."); return
        
        # Ayarlara son yazıcıyı kaydet (save_settings() çağrısı tüm ayarları kaydeder)
        self.save_settings()

        tab = self.notebook.index(self.notebook.select())
        img = None
        if tab == 0: img = self.last_service_image
        elif tab == 1: img = self.last_shipping_image
        elif tab == 2: img = self.last_exchange_image
        elif tab == 3: img = self.last_box_content_image
        if img is None: messagebox.showwarning("Uyarı", "Lütfen önce bir önizleme oluşturun."); return

        try:
            copies = max(1, self.copy_var.get())
            print_image_to_printer(img, printer, copies)
            messagebox.showinfo("Tamam", f"{copies} kopya yazdırıldı.")
        except Exception as e:
            messagebox.showerror("Yazdırma Hatası", f"Yazdırırken hata oluştu:\n{e}")

    def clear_form(self):
        tab = self.notebook.index(self.notebook.select())
        if tab == 0:
            for e in self.entries_service.values(): e.delete(0, tk.END)
            self.durum_var.set(""); self.il_var.set(""); self.ilce_var.set("")
            self.service_il_search.delete(0, tk.END); self.service_ilce_search.delete(0, tk.END)
        elif tab == 1:
            for e in self.entries_shipping.values(): e.delete(0, tk.END)
            self.kargo_var.set(""); self.odeme_var.set(""); self.shipping_align.set("left")
            self.shipping_il_var.set(""); self.shipping_ilce_var.set("")
            self.shipping_il_search.delete(0, tk.END); self.shipping_ilce_search.delete(0, tk.END)
        elif tab == 2:
            self.dolar_entry.delete(0, tk.END); self.exchange_result.set(""); self.exchange_align.set("left")
            self.auto_update_usd_kur()
        elif tab == 3:
            for var in self.box_vars: var.set(False)
            self.box_align.set("left")
        elif tab == 4:
            self.refresh_customer_logs()
        elif tab == 5:
            self.log_user_entry.delete(0, tk.END); self.log_pass_entry.delete(0, tk.END)
            self.log_search_entry.delete(0, tk.END)
            if self.log_table: self.log_table.destroy(); self.log_table = None
            self.log_access_granted = False
        
        self.show_image_on_preview(None)
        self.last_service_image = None; self.last_shipping_image = None
        self.last_exchange_image = None; self.last_box_content_image = None

    def auto_update_usd_kur(self):
        kur = get_usd_try_from_tcmb(satis=True)
        if kur:
            self.exchange_kur_label.config(text=f"Güncel TCMB USD/TRY Satış: {kur:.4f} TL (Otomatik güncellendi)")
            if not self.kur_entry.get():
                self.kur_entry.delete(0, tk.END); self.kur_entry.insert(0, f"{kur:.4f}")
        else: self.exchange_kur_label.config(text="Kura erişilemedi veya TCMB verisi alınamadı.")
        self.root.after(300000, self.auto_update_usd_kur)

    def load_usd_satis_kur(self):
        kur = get_usd_try_from_tcmb(satis=True)
        if kur:
            self.kur_entry.delete(0, tk.END); self.kur_entry.insert(0, f"{kur:.4f}")
            self.exchange_result.set(f"Güncel TCMB USD/TRY Satış Kuru: {kur:.4f} TL (Manuel güncellendi)")
        else: self.exchange_result.set("Kura erişilemedi veya TCMB verisi alınamadı.")

    # DÜZELTİLDİ: Artık hesaplanan veriyi bir sözlük olarak döndürür
    def calculate_exchange(self):
        try:
            dolar = float(self.dolar_entry.get().replace(",", "."))
            kur = float(self.kur_entry.get().replace(",", "."))
            tl = dolar * kur
            kdv = tl * KDV_ORANI
            tl_kdv = tl + kdv
            self.exchange_result.set(f"TL Karşılığı: {tl:.2f} TL\nKDV (%{int(KDV_ORANI*100)}): {kdv:.2f} TL\nKDV Dahil: {tl_kdv:.2f} TL")
            # Önizleme için veriyi döndür
            return {
                "tl": f"{tl:.2f}",
                "kdv": f"{kdv:.2f}",
                "tl_kdv": f"{tl_kdv:.2f}"
            }
        except Exception:
            self.exchange_result.set("Geçerli bir değer giriniz.")
            return None # Hata durumunda None döndür

# ==========================
# UYGULAMAYI ÇALIŞTIR
# ==========================
if __name__ == "__main__":
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f: config = json.load(f)
        theme = config.get("theme", "cosmo")
    except: theme = "cosmo"
        
    root = tb.Window(themename=theme)
    app = LabelApp(root)
    root.mainloop()
