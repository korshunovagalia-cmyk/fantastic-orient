// Shared tour data and site behaviour for every page, in English and Russian.
// Each page sets <html lang> and <body data-root> (path back to the site root).
const ROOT = document.body.dataset.root || "";
const LANG = document.documentElement.lang === "ru" ? "ru" : "en";
const BASE = LANG === "ru" ? "ru/" : "";
const LOCALE = LANG === "ru" ? "ru-RU" : "en-US";

const UI = {
  en: {
    from: "From", book: "Book now", more: "Learn more",
    guests: n => `${n} guest${n > 1 ? "s" : ""}`,
    ok: (tour, date, guests, email) => `${tour}, ${date}, ${guests}. Confirmation is on its way to ${email}.`
  },
  ru: {
    from: "от", book: "Забронировать", more: "Подробнее",
    guests: n => `${n} ${plural(n, "гость", "гостя", "гостей")}`,
    ok: (tour, date, guests, email) => `${tour}, ${date}, ${guests}. Подтверждение отправлено на ${email}.`
  }
}[LANG];

function plural(n, one, few, many) {
  const m10 = n % 10, m100 = n % 100;
  if (m10 === 1 && m100 !== 11) return one;
  if (m10 >= 2 && m10 <= 4 && (m100 < 12 || m100 > 14)) return few;
  return many;
}

const TOURS = [
  {
    id: "dubai", slug: "dubai-city-tour",
    now: 330,
    img: "assets/tours/dubai-city-tour.jpg",
    en: { title: "Dubai City Tour", tag: "Recommended", duration: "Approx. 6 hours", alt: "Dubai skyline at sunset" },
    ru: { title: "Обзорная экскурсия по Дубаю", tag: "Рекомендуем", duration: "Около 6 часов", alt: "Небоскрёбы Дубая на закате" }
  },
  {
    id: "abudhabi", slug: "abu-dhabi-city-tour",
    now: 450,
    img: "assets/tours/abu-dhabi-city-tour.jpg",
    en: { title: "Abu Dhabi City Tour", tag: "Recommended", duration: "Approx. 8–11 hours", alt: "Aerial view of Abu Dhabi at dusk" },
    ru: { title: "Обзорная экскурсия по Абу-Даби", tag: "Рекомендуем", duration: "Около 8–11 часов", alt: "Вечерний Абу-Даби с высоты" }
  },
  {
    id: "ferrari", slug: "abu-dhabi-ferrari-world",
    now: 495,
    img: "assets/tours/abu-dhabi-ferrari-world.jpg",
    en: { title: "Abu Dhabi City Tour with Ferrari World", tag: "Recommended", duration: "Full day", alt: "Guests riding a Ferrari-themed ride at Ferrari World" },
    ru: { title: "Абу-Даби и Ferrari World", tag: "Рекомендуем", duration: "Целый день", alt: "Гости на аттракционе в Ferrari World" }
  },
  {
    id: "louvre", slug: "abu-dhabi-louvre-museum",
    now: 173,
    img: "assets/tours/abu-dhabi-louvre.jpg",
    en: { title: "Abu Dhabi City Tour with Louvre Museum", tag: "New", duration: "Full day · Tue, Thu, Sat", alt: "The Louvre Abu Dhabi dome on Saadiyat Island" },
    ru: { title: "Абу-Даби и Лувр", tag: "Новинка", duration: "Целый день · вт, чт, сб", alt: "Купол Лувра Абу-Даби на острове Саадият" }
  }
].map(t => ({ ...t, ...t[LANG] }));

const num = (n, d) => n.toLocaleString(LOCALE, { minimumFractionDigits: d, maximumFractionDigits: d });
const fmt = n => "AED " + num(n, Number.isInteger(n) ? 0 : 2);
const $ = s => document.querySelector(s);
const tourUrl = t => `${ROOT}${BASE}tours/${t.slug}.html`;

// Tour cards: <div class="grid" data-cards data-exclude="id"></div>
document.querySelectorAll("[data-cards]").forEach(grid => {
  const list = TOURS.filter(t => t.id !== grid.dataset.exclude);
  grid.innerHTML = list.map(t => `
    <article class="card reveal">
      <div class="card-body">
        <div class="tag">${t.tag}</div>
        <h3><a href="${tourUrl(t)}" style="color:inherit">${t.title}</a></h3>
        <div class="meta">${t.duration}</div>
        <div class="price">
          <span class="now">${UI.from} ${fmt(t.now)}</span>
        </div>
        <div class="btn-row">
          <a class="btn" href="${tourUrl(t)}#book">${UI.book}</a>
          <a class="link-more" href="${tourUrl(t)}">${UI.more}</a>
        </div>
      </div>
      <a href="${tourUrl(t)}" tabindex="-1" aria-hidden="true" style="margin-top:auto"><img src="${ROOT}${t.img}" alt="${t.alt}" loading="lazy"></a>
    </article>`).join("");
});

// Booking form
const form = $("#form");
if (form) {
  const tourSel = $("#tour"), guestSel = $("#guests"), dateIn = $("#date");
  tourSel.innerHTML = TOURS.map(t => `<option value="${t.id}">${t.title} — ${fmt(t.now)}</option>`).join("");
  if (form.dataset.tour) tourSel.value = form.dataset.tour;
  guestSel.innerHTML = Array.from({length: 10}, (_, i) => `<option>${i + 1}</option>`).join("");
  const tomorrow = new Date(Date.now() + 864e5).toISOString().slice(0, 10);
  dateIn.min = tomorrow; dateIn.value = tomorrow;

  const updateTotal = () => {
    const t = TOURS.find(x => x.id === tourSel.value);
    $("#total").textContent = fmt(Math.round(t.now * +guestSel.value * 100) / 100);
  };
  tourSel.onchange = guestSel.onchange = updateTotal;
  updateTotal();

  form.addEventListener("submit", e => {
    e.preventDefault();
    for (const el of form.querySelectorAll("[required]")) {
      if (!el.checkValidity()) { el.focus(); el.reportValidity(); return; }
    }
    const t = TOURS.find(x => x.id === tourSel.value);
    const d = new Date(dateIn.value + "T00:00").toLocaleDateString(LOCALE, { weekday: "long", day: "numeric", month: "long" });
    $("#success-msg").textContent = UI.ok(t.title, d, UI.guests(+guestSel.value), $("#email").value);
    form.classList.add("done");
  });
}

// WhatsApp chat button. Company number: country code + number, digits only.
const WHATSAPP = "971503984978";
(() => {
  const text = {
    en: { bubble: "Need help? Chat with us", close: "Close", label: "Chat with us on WhatsApp",
          msg: t => `Hello! I'd like to ask about ${t || "your tours"}.` },
    ru: { bubble: "Нужна помощь? Напишите нам", close: "Закрыть", label: "Написать нам в WhatsApp",
          msg: t => `Здравствуйте! Хочу узнать подробнее ${t ? `об экскурсии «${t}»` : "о ваших экскурсиях"}.` }
  }[LANG];
  const tour = form && form.dataset.tour ? TOURS.find(t => t.id === form.dataset.tour).title : "";
  const href = `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(text.msg(tour))}`;

  const wa = document.createElement("div");
  wa.className = "wa";
  wa.innerHTML = `
    <div class="wa-bubble" role="status">
      <a href="${href}" target="_blank" rel="noopener">${text.bubble}</a>
      <button class="wa-x" type="button" aria-label="${text.close}">×</button>
    </div>
    <a class="wa-btn" href="${href}" target="_blank" rel="noopener" aria-label="${text.label}">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path class="wa-ring" d="M12 2.8a9.2 9.2 0 0 0-7.9 13.9L2.8 21.2l4.6-1.2A9.2 9.2 0 1 0 12 2.8z"/>
        <path class="wa-phone" d="M9.1 7.3c.3 0 .5 0 .7.5l.8 1.9c.1.2 0 .5-.1.6l-.6.7c-.1.2-.1.3 0 .5.6 1.1 1.5 2 2.6 2.6.2.1.4.1.5 0l.7-.8c.2-.2.4-.2.6-.1l1.9.9c.3.1.4.3.4.6 0 1.2-1 2.1-2.2 2.1-3.4-.2-6.4-3.2-6.6-6.6 0-1.3 1-2.9 1.3-2.9z"/>
      </svg>
    </a>`;
  document.body.appendChild(wa);

  let dismissed = false;
  try { dismissed = sessionStorage.getItem("wa-dismissed") === "1"; } catch (_) {}
  if (!dismissed) setTimeout(() => wa.classList.add("show"), 2500);
  wa.querySelector(".wa-x").addEventListener("click", () => {
    wa.classList.remove("show");
    try { sessionStorage.setItem("wa-dismissed", "1"); } catch (_) {}
  });
})();

// Reveal on scroll
const io = new IntersectionObserver(es => es.forEach(en => {
  if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
}), { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach(el => io.observe(el));
