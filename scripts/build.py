# Generates index.html, tours/*.html and ru/** from the content below.
# Run from the site root:  python3 scripts/build.py .
import os, sys
from html import escape as e

OUT = sys.argv[1]

# Version tags so browsers fetch fresh CSS/JS after every change.
import hashlib
def ver(name):
    return hashlib.md5(open(os.path.join(OUT, name), "rb").read()).hexdigest()[:8]
LANGS = ["en", "ru"]

# ---------- Tours ----------
TOURS = [
  dict(id="dubai", slug="dubai-city-tour", img="assets/tours/dubai-city-tour.jpg",
       now=330,
       en=dict(title="Dubai City Tour", tag="Recommended",
               alt="Dubai skyline at sunset",
               desc="Modern landmarks and old souks in one half-day.",
               overview="Modern landmarks and old souks in one half-day. Your driver-guide takes you from Downtown Dubai to the creek-side quarters of Old Dubai, then along the coast.",
               facts=["Approx. 6 hours", "8:30 am – 2:30 pm, daily",
                      "Hotels in Deira, Bur Dubai, Sheikh Zayed Road and Marina"],
               highlights=["Zabeel Palace, home of Dubai's ruling family (photo stop)",
                           "Dubai Frame (photo stop)",
                           "Abra boat ride across Dubai Creek",
                           "Al Fahidi Historical Neighbourhood and a restored courtyard house",
                           "Gold Souk and Spice Souk",
                           "Islamic Art Centre",
                           "Drive past Etihad Museum, Jumeirah Mosque and The Pointe",
                           "Burj Al Arab, Al Qasr and Atlantis, The Palm photo stops"],
               notes="Some sites may be closed on certain days or weekends. Pickup times may vary by 30–60 minutes depending on traffic."),
       ru=dict(title="Обзорная экскурсия по Дубаю", tag="Рекомендуем",
               alt="Небоскрёбы Дубая на закате",
               desc="Современный Дубай и старинные рынки за полдня.",
               overview="Современный Дубай и старинные рынки за полдня. Гид-водитель проведёт вас от Даунтауна до исторических кварталов Старого Дубая у залива, а затем — вдоль побережья.",
               facts=["Около 6 часов", "8:30 – 14:30, ежедневно",
                      "Отели в Дейре, Бур-Дубае, на Шейх-Зайед-роуд и в Марине"],
               highlights=["Дворец Забиль — резиденция правящей семьи Дубая (фотостоп)",
                           "Рамка Дубая — Dubai Frame (фотостоп)",
                           "Прогулка на абре через залив Дубай-Крик",
                           "Исторический квартал Аль-Фахиди и отреставрированный дом с внутренним двором",
                           "Золотой рынок и рынок специй",
                           "Центр исламского искусства",
                           "Проезд мимо музея Этихад, мечети Джумейра и The Pointe",
                           "Фотостопы у Бурдж-эль-Араб, Al Qasr и Atlantis, The Palm"],
               notes="Некоторые объекты могут быть закрыты в отдельные дни или выходные. Время трансфера может сдвигаться на 30–60 минут в зависимости от трафика.")),
  dict(id="abudhabi", slug="abu-dhabi-city-tour", img="assets/tours/abu-dhabi-city-tour.jpg",
       now=450,
       en=dict(title="Abu Dhabi City Tour", tag="Recommended",
               alt="Aerial view of Abu Dhabi at dusk",
               desc="A full day in the capital, with return transfers from Dubai.",
               overview="A full day in the capital, with return hotel transfers from Dubai. See the landmarks, drive the waterfront and break for lunch at Marina Mall.",
               facts=["Approx. 8–11 hours", "Starts around 9:30 am, daily",
                      "Central Dubai hotels — Deira, Bur Dubai, Sheikh Zayed Road, Marina"],
               highlights=["Sheikh Zayed Grand Mosque",
                           "Emirates Palace drive-by",
                           "Scenic drive along the Corniche",
                           "Lunch break at Marina Mall",
                           "Yas Island and Ferrari World drive-by"],
               notes="Please dress modestly for the mosque, with shoulders and knees covered. Lunch is at your own expense unless you choose a lunch-inclusive option."),
       ru=dict(title="Обзорная экскурсия по Абу-Даби", tag="Рекомендуем",
               alt="Вечерний Абу-Даби с высоты",
               desc="Целый день в столице ОАЭ с трансфером из Дубая и обратно.",
               overview="Целый день в столице с трансфером из отеля в Дубае и обратно. Главные достопримечательности, поездка вдоль набережной и обед в Marina Mall.",
               facts=["Около 8–11 часов", "Начало около 9:30, ежедневно",
                      "Отели в центре Дубая — Дейра, Бур-Дубай, Шейх-Зайед-роуд, Марина"],
               highlights=["Большая мечеть шейха Зайда",
                           "Проезд мимо дворца Emirates Palace",
                           "Живописная поездка по набережной Корниш",
                           "Перерыв на обед в Marina Mall",
                           "Проезд по острову Яс мимо Ferrari World"],
               notes="Для посещения мечети нужна закрытая одежда: плечи и колени должны быть покрыты. Обед оплачивается отдельно, если вы не выбрали вариант с обедом.")),
  dict(id="ferrari", slug="abu-dhabi-ferrari-world", img="assets/tours/abu-dhabi-ferrari-world.jpg",
       now=495,
       en=dict(title="Abu Dhabi City Tour with Ferrari World", tag="Recommended",
               alt="Guests riding a Ferrari-themed ride at Ferrari World",
               desc="Abu Dhabi's icons, then full entry to Ferrari World.",
               overview="Abu Dhabi's cultural icons in the morning, then full entry to Ferrari World on Yas Island — home of Formula Rossa, the world's fastest roller coaster.",
               facts=["Full day", "Pickup around 8:30 am, back in the evening",
                      "Central Dubai hotels — Deira, Bur Dubai, Sheikh Zayed Road, Marina"],
               highlights=["Sheikh Zayed Grand Mosque",
                           "BAPS Mandir, hand-carved stone temple (Tuesday – Sunday)",
                           "Corniche drive, Emirates Palace and Islamic Art Gallery (Mondays)",
                           "Ferrari World Abu Dhabi entry ticket",
                           "Formula Rossa, racing simulators and family rides"],
               notes="The cultural stop changes on Mondays. Please dress modestly for the mosque and temple."),
       ru=dict(title="Абу-Даби и Ferrari World", tag="Рекомендуем",
               alt="Гости на аттракционе в Ferrari World",
               desc="Символы Абу-Даби и полный доступ в Ferrari World.",
               overview="Утром — культурные символы Абу-Даби, затем полный доступ в Ferrari World на острове Яс, где находятся Formula Rossa — самые быстрые американские горки в мире.",
               facts=["Целый день", "Выезд около 8:30, возвращение вечером",
                      "Отели в центре Дубая — Дейра, Бур-Дубай, Шейх-Зайед-роуд, Марина"],
               highlights=["Большая мечеть шейха Зайда",
                           "Индуистский храм BAPS Mandir с резьбой по камню (вторник – воскресенье)",
                           "Набережная Корниш, Emirates Palace и галерея исламского искусства (по понедельникам)",
                           "Входной билет в Ferrari World Абу-Даби",
                           "Formula Rossa, гоночные симуляторы и семейные аттракционы"],
               notes="По понедельникам культурная программа меняется. Для посещения мечети и храма нужна закрытая одежда.")),
  dict(id="louvre", slug="abu-dhabi-louvre-museum", img="assets/tours/abu-dhabi-louvre.jpg",
       now=173,
       en=dict(title="Abu Dhabi City Tour with Louvre Museum", tag="New",
               alt="The Louvre Abu Dhabi dome on Saadiyat Island",
               desc="Landmarks and art, under the dome of the Louvre.",
               overview="Landmarks and art in one day. Visit the Grand Mosque, then step under the dome of the Louvre Abu Dhabi — more than 600 works, about half on loan from French museums.",
               facts=["Full day", "Tuesday, Thursday and Saturday",
                      "Hotels in Deira, Bur Dubai, Marina, Al Barsha and Sheikh Zayed Road"],
               highlights=["Louvre Abu Dhabi admission on Saadiyat Island",
                           "Sheikh Zayed Grand Mosque",
                           "Abu Dhabi Date Market",
                           "Heritage Village",
                           "Corniche photo stop and Emirates Palace drive-through",
                           "Yas Island Ferrari World drive-through"],
               notes="Meals, drinks and tips are not included. A mosque entrance fee of AED 8 per person applies from 1 September 2026. Please dress modestly."),
       ru=dict(title="Абу-Даби и Лувр", tag="Новинка",
               alt="Купол Лувра Абу-Даби на острове Саадият",
               desc="Достопримечательности и искусство под куполом Лувра.",
               overview="Достопримечательности и искусство за один день. Посетите Большую мечеть, а затем войдите под купол Лувра Абу-Даби — более 600 произведений, около половины из них предоставлены музеями Франции.",
               facts=["Целый день", "Вторник, четверг и суббота",
                      "Отели в Дейре, Бур-Дубае, Марине, Аль-Барше и на Шейх-Зайед-роуд"],
               highlights=["Входной билет в Лувр Абу-Даби на острове Саадият",
                           "Большая мечеть шейха Зайда",
                           "Финиковый рынок Абу-Даби",
                           "Деревня наследия (Heritage Village)",
                           "Фотостоп на Корнише и проезд мимо Emirates Palace",
                           "Проезд по острову Яс мимо Ferrari World"],
               notes="Питание, напитки и чаевые не включены. С 1 сентября 2026 года взимается плата за вход в мечеть — 8 AED с человека. Пожалуйста, выбирайте закрытую одежду.")),
]

# ---------- Interface text ----------
T = dict(
  en=dict(
    home_title="Fantastic Orient — City Tours",
    home_desc="Fantastic Orient city tours in Dubai and Abu Dhabi. Hotel pickup, expert guides, best prices.",
    home_aria="Fantastic Orient home",
    nav_tours="Tours", nav_why="Why us", nav_book="Booking", book_now="Book now",
    hero_h1="Fantastic Tours, fantastic journey.", hero_sub="City tours across Dubai and Abu Dhabi.",
    explore="Explore tours", hero_alt="Dubai skyline at sunset seen across the water",
    tours_h="City Tours.", tours_p="Four ways to see the Emirates.",
    why_h="Why travel with us.", why_p="We handle the details. You enjoy the city.",
    f1_h="Hotel pickup", f1_p="Door-to-door transfers from central Dubai hotels.",
    f2_h="Expert guides", f2_p="Local guides who know every story behind the skyline.",
    f3_h="Fair prices", f3_p="Clear prices with transfers included.",
    partners_h="World-class attractions.",
    partners_p="We partner with the leading attractions and entertainment destinations in the UAE.",
    book_h="Book now.", book_tour_h="Book this tour.", book_p="Reserve your seat in under a minute.",
    l_tour="Tour", l_date="Date", l_guests="Guests", l_name="Full name", l_email="Email", l_total="Total",
    ok_h="You're booked.", ok_p="We'll email your confirmation shortly.",
    copyright="Copyright © 2026 Fantastic Orient. All rights reserved.",
    place="Dubai · Abu Dhabi · United Arab Emirates",
    crumbs_home="Home", crumbs_tours="City Tours",
    pickup_incl="Hotel pickup included", from_="From",
    see_hl="See highlights", hl_h="Highlights.", hl_p="What you'll see along the way.",
    more_h="More tours.", facts=["Duration", "Schedule", "Pickup"],
    switch_aria="Language",
  ),
  ru=dict(
    home_title="Fantastic Orient — обзорные экскурсии",
    home_desc="Обзорные экскурсии Fantastic Orient по Дубаю и Абу-Даби. Трансфер из отеля, опытные гиды, лучшие цены.",
    home_aria="Fantastic Orient — на главную",
    nav_tours="Экскурсии", nav_why="Почему мы", nav_book="Бронирование", book_now="Забронировать",
    hero_h1="Фантастические туры, фантастическое путешествие.", hero_sub="Обзорные экскурсии по Дубаю и Абу-Даби.",
    explore="Все экскурсии", hero_alt="Небоскрёбы Дубая на закате с видом через залив",
    tours_h="Обзорные экскурсии.", tours_p="Четыре способа увидеть Эмираты.",
    why_h="Почему мы.", why_p="Мы берём на себя все детали. Вы наслаждаетесь городом.",
    f1_h="Трансфер из отеля", f1_p="Трансфер от двери до двери из отелей в центре Дубая.",
    f2_h="Опытные гиды", f2_p="Местные гиды, которые знают историю каждого здания.",
    f3_h="Честные цены", f3_p="Понятные цены, трансфер уже включён.",
    partners_h="Достопримечательности мирового уровня.",
    partners_p="Мы сотрудничаем с ведущими достопримечательностями и развлекательными центрами ОАЭ.",
    book_h="Бронирование.", book_tour_h="Забронировать экскурсию.", book_p="Забронируйте место меньше чем за минуту.",
    l_tour="Экскурсия", l_date="Дата", l_guests="Гости", l_name="Имя и фамилия", l_email="Email", l_total="Итого",
    ok_h="Бронирование принято.", ok_p="Скоро мы пришлём подтверждение на вашу почту.",
    copyright="© 2026 Fantastic Orient. Все права защищены.",
    place="Дубай · Абу-Даби · Объединённые Арабские Эмираты",
    crumbs_home="Главная", crumbs_tours="Обзорные экскурсии",
    pickup_incl="Трансфер из отеля включён", from_="от",
    see_hl="Программа", hl_h="Программа.", hl_p="Что вы увидите по пути.",
    more_h="Другие экскурсии.", facts=["Продолжительность", "Расписание", "Трансфер"],
    switch_aria="Язык",
  ),
)

PARTNERS = [
  [("img-worlds","IMG Worlds of Adventure"),("miracle-garden","Dubai Miracle Garden"),("at-the-top","At The Top, Burj Khalifa"),
   ("ski-dubai","Ski Dubai"),("atlantis","Atlantis"),("aquaventure","Aquaventure World"),
   ("dubai-aquarium","Dubai Aquarium & Underwater Zoo"),("kidzania","KidZania")],
  [("dubai-ice-rink","Dubai Ice Rink"),("sky-views","Sky Views"),("aya","AYA Universe"),("dubai-fountain","Dubai Fountain"),
   ("dubai-dolphinarium","Dubai Dolphinarium"),("global-village","Global Village"),("motiongate","Motiongate Dubai")],
]

# ---------- Number formatting ----------
def num(x, lang, decimals=None):
    if decimals is None:
        decimals = 0 if float(x).is_integer() else 2
    s = f"{x:,.{decimals}f}"
    if lang == "ru":
        s = s.replace(",", " ").replace(".", ",")
    return s

# ---------- Paths ----------
# page: "index" or a tour slug. Returns the file path relative to the site root.
def page_path(lang, page):
    base = "" if lang == "en" else "ru/"
    return f"{base}index.html" if page == "index" else f"{base}tours/{page}.html"

def root_for(lang, page):
    return "../" * page_path(lang, page).count("/")

# ---------- Shared blocks ----------
def head(lang, page, title, desc):
    t, root = T[lang], root_for(lang, page)
    home = root + page_path(lang, "index")
    switch = "".join(
        f'<a href="{root}{page_path(l, page)}" hreflang="{l}" lang="{l}"'
        + (' class="on" aria-current="true"' if l == lang else "") + f'>{l.upper()}</a>'
        for l in LANGS)
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{root}{page_path(l, page)}">' for l in LANGS)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{alternates}
<link rel="icon" href="{root}assets/fo-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}styles.css?v={ver("styles.css")}">
</head>
<body data-root="{root}">

<nav class="nav">
  <div class="wrap">
    <a class="nav-logo" href="{home}" aria-label="{e(t["home_aria"])}"><img src="{root}assets/logo.png" alt="Fantastic Orient"></a>
    <ul class="nav-links">
      <li><a href="{home}#tours">{t["nav_tours"]}</a></li>
      <li><a href="{home}#why">{t["nav_why"]}</a></li>
      <li><a href="#book">{t["nav_book"]}</a></li>
    </ul>
    <div class="nav-right">
      <div class="lang" role="group" aria-label="{t["switch_aria"]}">{switch}</div>
      <a class="nav-cta" href="#book">{t["book_now"]}</a>
    </div>
  </div>
</nav>
'''

def partners(lang, root):
    t = T[lang]
    rows = []
    for i, row in enumerate(PARTNERS):
        imgs = "".join(f'<img src="{root}assets/partners/{f}.png" alt="{e(a)}" loading="lazy">' for f, a in row)
        dup = "".join(f'<img src="{root}assets/partners/{f}.png" alt="" aria-hidden="true" loading="lazy">' for f, a in row)
        rows.append(f'    <div class="marquee{" reverse" if i else ""}"><div class="track">{imgs}{dup}</div></div>')
    return f'''
<section class="partners" id="partners">
  <div class="wrap section-head reveal">
    <h2>{t["partners_h"]}</h2>
    <p>{t["partners_p"]}</p>
  </div>
  <div class="marquees reveal">
''' + "\n".join(rows) + '''
  </div>
</section>
'''

def booking(lang, title, tour_id=""):
    t = T[lang]
    attr = f' data-tour="{tour_id}"' if tour_id else ""
    return f'''
<section class="book" id="book">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>{e(title)}</h2>
      <p>{e(t["book_p"])}</p>
    </div>
    <form class="form reveal" id="form"{attr} novalidate>
      <div class="field full">
        <label for="tour">{t["l_tour"]}</label>
        <select id="tour" name="tour" required></select>
      </div>
      <div class="field">
        <label for="date">{t["l_date"]}</label>
        <input id="date" name="date" type="date" required>
      </div>
      <div class="field">
        <label for="guests">{t["l_guests"]}</label>
        <select id="guests" name="guests"></select>
      </div>
      <div class="field">
        <label for="name">{t["l_name"]}</label>
        <input id="name" name="name" type="text" autocomplete="name" required>
      </div>
      <div class="field">
        <label for="email">{t["l_email"]}</label>
        <input id="email" name="email" type="email" autocomplete="email" required>
      </div>
      <div class="total"><span>{t["l_total"]}</span><b id="total"></b></div>
      <button class="btn" type="submit">{t["book_now"]}</button>
      <div class="success" role="status">
        <h3>{t["ok_h"]}</h3>
        <p id="success-msg">{t["ok_p"]}</p>
      </div>
    </form>
  </div>
</section>
'''

def foot(lang, root):
    t = T[lang]
    return f'''
<footer>
  <div class="wrap">
    <div>
      <img src="{root}assets/logo.png" alt="Fantastic Orient">
      <div>{t["copyright"]}</div>
    </div>
    <div>{t["place"]}</div>
  </div>
</footer>

<script src="{root}tours.js?v={ver("tours.js")}"></script>
</body>
</html>
'''

# ---------- Pages ----------
def index_page(lang):
    t, root = T[lang], root_for(lang, "index")
    body = f'''
<header class="hero" id="top">
  <div class="wrap reveal">
    <h1>{t["hero_h1"]}</h1>
    <p class="sub">{t["hero_sub"]}</p>
    <div class="btn-row">
      <a class="btn" href="#book">{t["book_now"]}</a>
      <a class="link-more" href="#tours">{t["explore"]}</a>
    </div>
  </div>
  <div class="hero-media reveal">
    <img src="{root}assets/tours/dubai-city-tour.jpg" alt="{e(t["hero_alt"])}">
  </div>
</header>

<section class="tours" id="tours">
  <div class="section-head wrap reveal">
    <h2>{t["tours_h"]}</h2>
    <p>{t["tours_p"]}</p>
  </div>
  <div class="grid" data-cards></div>
</section>

<section id="why">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>{t["why_h"]}</h2>
      <p>{t["why_p"]}</p>
    </div>
    <div class="features">
      <div class="feature reveal">
        <div class="icon"><svg viewBox="0 0 24 24"><path d="M3 13l2-6h14l2 6v5h-2.5M3 13v5h2.5M3 13h18"/><circle cx="7.5" cy="18" r="2"/><circle cx="16.5" cy="18" r="2"/></svg></div>
        <h4>{t["f1_h"]}</h4>
        <p>{t["f1_p"]}</p>
      </div>
      <div class="feature reveal">
        <div class="icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-8 8-8s8 3.6 8 8"/></svg></div>
        <h4>{t["f2_h"]}</h4>
        <p>{t["f2_p"]}</p>
      </div>
      <div class="feature reveal">
        <div class="icon"><svg viewBox="0 0 24 24"><path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg></div>
        <h4>{t["f3_h"]}</h4>
        <p>{t["f3_p"]}</p>
      </div>
    </div>
  </div>
</section>
'''
    return (head(lang, "index", t["home_title"], t["home_desc"]) + body
            + booking(lang, t["book_h"]) + foot(lang, root))

def tour_page(lang, tour):
    t, root, c = T[lang], root_for(lang, tour["slug"]), tour[lang]
    home = root + page_path(lang, "index")
    facts = "\n".join(f'      <div class="fact reveal"><span>{e(k)}</span><b>{e(v)}</b></div>'
                      for k, v in zip(t["facts"], c["facts"]))
    hl = "\n".join(f"      <li>{e(h)}</li>" for h in c["highlights"])
    body = f'''
<div class="wrap crumbs"><a href="{home}">{t["crumbs_home"]}</a> › <a href="{home}#tours">{t["crumbs_tours"]}</a> › {e(c["title"])}</div>

<header class="tour-hero">
  <div class="wrap reveal">
    <div class="tag">{e(c["tag"])}</div>
    <h1>{e(c["title"])}</h1>
    <div class="meta">{t["pickup_incl"]}</div>
    <div class="price">
      <span class="now">{t["from_"]} AED {num(tour["now"], lang)}</span>
    </div>
    <div class="btn-row">
      <a class="btn" href="#book">{t["book_now"]}</a>
      <a class="link-more" href="#highlights">{t["see_hl"]}</a>
    </div>
  </div>
  <div class="hero-media reveal">
    <img src="{root}{tour["img"]}" alt="{e(c["alt"])}">
  </div>
</header>

<section>
  <div class="wrap">
    <p class="tour-overview reveal">{e(c["overview"])}</p>
    <div class="facts">
{facts}
    </div>
  </div>
</section>

<section class="tours" id="highlights">
  <div class="wrap">
    <div class="section-head reveal">
      <h2>{t["hl_h"]}</h2>
      <p>{t["hl_p"]}</p>
    </div>
    <ul class="highlights reveal">
{hl}
    </ul>
    <p class="notes reveal">{e(c["notes"])}</p>
  </div>
</section>

<section class="more-tours">
  <div class="section-head wrap reveal">
    <h2>{t["more_h"]}</h2>
  </div>
  <div class="grid grid-3" data-cards data-exclude="{tour["id"]}"></div>
</section>
''' + booking(lang, t["book_tour_h"], tour["id"])
    return head(lang, tour["slug"], f'{c["title"]} — Fantastic Orient', c["desc"]) + body + foot(lang, root)

def write(rel, html):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(html)

for lang in LANGS:
    write(page_path(lang, "index"), index_page(lang))
    for tour in TOURS:
        write(page_path(lang, tour["slug"]), tour_page(lang, tour))

print("ok")
