# -*- coding: utf-8 -*-
"""Builds section index pages and catalog.html (light cards grouped by content type).
Run from the repo root:  python3 _tools/build_site.py
New files are picked up automatically; add a (name, description) for them in META."""
import os, re, html

SECTIONS = {
 '01_Mechanics/01_1_kinematics': ('קינמטיקה', 'תנועה בקו ישר: סימולציה, יחידת לימוד ובונה פתרון לשאלות בגרות', 'מכניקה'),
 '01_Mechanics/01_2_projectiles': ('זריקה ובליסטיקה', 'תנועה בשדה הכובד: סימולציה ובונה פתרון לשאלות בגרות', 'מכניקה'),
 '01_Mechanics/01_3_forces': ('כוחות וחוקי ניוטון', 'דינמיקה: יחידת לימוד ובונה פתרון לשאלות בגרות', 'מכניקה'),
 '01_Mechanics/01_4_circular_motion': ('תנועה מעגלית', 'דינמיקה של תנועה מעגלית', 'מכניקה'),
 '01_Mechanics/01_5_energy': ('עבודה ואנרגיה', 'שימור אנרגיה ועבודת כוחות', 'מכניקה'),
 '01_Mechanics/01_6_momentum': ('תנע', 'שימור תנע והתנגשויות', 'מכניקה'),
 '01_Mechanics/01_7_gravitation': ('כבידה ולוויינים', 'חוק הכבידה העולמי, חוקי קפלר ומסלולי לוויינים', 'מכניקה'),
 '01_Mechanics/01_8_harmonic_motion': ('תנועה הרמונית', 'נושא בהכנה', 'מכניקה'),
 '02_Electricity/02_1_electrostatics': ('אלקטרוסטטיקה', 'מטען, שדה חשמלי ופוטנציאל', 'חשמל'),
 '02_Electricity/02_2_current': ('זרם חשמלי ומעגלים', 'מעגלי זרם ישר', 'חשמל'),
 '02_Electricity/02_3_magnetism': ('מגנטיות', 'נושא בהכנה', 'חשמל'),
 '02_Electricity/02_4_induction': ('אינדוקציה', 'נושא בהכנה', 'חשמל'),
}
TOPIC = {  # folder: (strong colour, light tint) - same colours as the cards on the 'mechanics' page
 '01_Mechanics/01_1_kinematics': ('#1D4ED8', '#E6F1FB'), '01_Mechanics/01_2_projectiles': ('#EA580C', '#FFF1E7'),
 '01_Mechanics/01_3_forces': ('#059669', '#E3F6EE'), '01_Mechanics/01_4_circular_motion': ('#7C3AED', '#F1EAFE'),
 '01_Mechanics/01_5_energy': ('#D97706', '#FDF2DC'), '01_Mechanics/01_6_momentum': ('#DB2777', '#FCE8F1'),
 '01_Mechanics/01_7_gravitation': ('#0D9488', '#DFF5F2'), '01_Mechanics/01_8_harmonic_motion': ('#4F46E5', '#E9E8FD'),
 '02_Electricity/02_1_electrostatics': ('#CA8A04', '#FEF6D8'), '02_Electricity/02_2_current': ('#0891B2', '#E0F5FA'),
 '02_Electricity/02_3_magnetism': ('#9333EA', '#F3E8FF'), '02_Electricity/02_4_induction': ('#E11D48', '#FFE8EE'),
}
# kind: (section heading, tint bg, dark text, strong colour, open label)
KINDS = [
 ('sim',     'סימולציות',            '#E6F1FB', '#0C447C', '#1D4ED8', 'הפעל סימולציה'),
 ('unit',    'יחידות לימוד',          '#E1F5EE', '#085041', '#0F6E56', 'פתח יחידה'),
 ('bagrut',  'פתרונות מלאים לבגרות', '#FCEBEB', '#791F1F', '#B91C1C', 'לפתרון המלא'),
 ('builder', 'בונה פתרון',           '#EEEDFE', '#3C3489', '#6D28D9', 'כנסו לבונה הפתרון'),
 ('pdf',     'סיכומים PDF',          '#FAEEDA', '#633806', '#B45309', 'פתח PDF'),
]
K = {k[0]: k for k in KINDS}
SIMS = {'kinematics_simulation.html', 'projectiles_simulation.html', 'circular_motion_dynamics.html',
        'work_energy_simulation.html', 'momentum-conservation.html', 'gravity_simulation.html'}
B_FORCES = 'בונים את הפתרון צעד אחר צעד: תרשים כוחות, משוואות תנועה וחישוב.'
B_PROJ = 'בונים את הפתרון צעד אחר צעד: רכיבי המהירות, משוואות התנועה וחישוב.'
META = {
 # simulations
 'kinematics_simulation.html': ('תנועה בקו ישר', 'חקר תנועה בקו ישר: גרפים של מקום-זמן, מהירות-זמן ותאוצה.'),
 'projectiles_simulation.html': ('תנועת גוף בשדה הכובד', 'סימולציה של תנועת גוף בשדה הכובד.'),
 'circular_motion_dynamics.html': ('תנועה מעגלית: דינמיקה', 'כוחות, שקול הכוחות, תאוצה ומהירות בתנועה מעגלית, עם ערכים בזמן אמת.'),
 'work_energy_simulation.html': ('עבודה ואנרגיה', 'המרות אנרגיה קינטית ופוטנציאלית ועבודת כוחות לא משמרים.'),
 'momentum-conservation.html': ('שימור תנע בהתנגשויות', 'התנגשות אלסטית, לא אלסטית ופלסטית על מסילה ללא חיכוך.'),
 'gravity_simulation.html': ('מעבדת כבידה', 'חוקי קפלר, חוק הכבידה העולמי ואנרגיה של לוויין.'),
 # study units
 'linear_motion.html': ('תנועה בקו ישר', 'יחידת לימוד בקינמטיקה, 5 יח"ל: נושאים, נוסחאות והדגמות.'),
 'newton_laws.html': ('כוחות וחוקי ניוטון', 'יחידת לימוד בדינמיקה, 5 יח"ל: נושאים, נוסחאות והדגמות.'),
 'gravitation_satellites.html': ('כבידה ולוויינים', 'יחידת לימוד בכבידה, 5 יח"ל: נושאים, נוסחאות והדגמות.'),
 'charge_electric_field.html': ('מטען בשדה חשמלי', 'יחידת המשך באלקטרוסטטיקה, 5 יח"ל: נושאים ונוסחאות.'),
 'electrostatics_field_potential.html': ('מטען, שדה ופוטנציאל', 'יחידת לימוד באלקטרוסטטיקה, 5 יח"ל: נושאים ונוסחאות.'),
 'current_circuits.html': ('זרם חשמלי ומעגלים', 'יחידת לימוד במעגלי זרם ישר, 5 יח"ל: נושאים ונוסחאות.'),
 # PDFs
 '01_0_uniform_motion.pdf': ('תנועה קצובה', 'סיכום שיעור בקובץ PDF.'),
 '01_2_vertical_motion.pdf': ('תנועה אנכית', 'סיכום שיעור בקובץ PDF.'),
 '01_3_projective_motion.pdf': ('זריקה אופקית ומשופעת', 'סיכום שיעור בקובץ PDF.'),
 '01_4_newton_laws.pdf': ('חוקי ניוטון', 'סיכום שיעור: שלושת חוקי ניוטון, כוח נורמלי וחיכוך.'),
 '01_7_circular_motion.pdf': ('תנועה מעגלית', 'סיכום שיעור בקובץ PDF.'),
 # builders
 'kinematics_2014_q1.html': ('צניחה חופשית ומצנח', 'צניחה חופשית ופתיחת מצנח: מהירות סופית.'),
 'kinematics_2015_q1.html': ('שתי משאיות ומעקב GPS', 'מעקב GPS אחר שתי משאיות A ו-B לאורך קטע ישר.'),
 'kinematics_2018_q1.html': ('שלושה כדורים ממגדל', 'שלושה כדורים הנזרקים אנכית ממגדל.'),
 'kinematics_2019_q1.html': ('זריקה אנכית מגג בניין', 'זריקה אנכית מגג בניין: ניתוח גרף מקום-זמן.'),
 'kinematics_2020_q1.html': ('נחיתת "בראשית"', 'נחיתת הגשושית "בראשית" על הירח.'),
 'kinematics_2021_q1.html': ('שתי מכוניות זו לקראת זו', 'שתי מכוניות הנעות זו לקראת זו עד לעצירה משותפת.'),
 'kinematics_2022_q1.html': ('זמן תגובה ובלימה', 'נסיעת מכונית, זמן תגובה ובלימה מול כדור מתגלגל.'),
 'kinematics_2023_q1.html': ('שני ניסויים על מישור משופע', 'שני ניסויים על מישור משופע חלק ועם חיכוך.'),
 'kinematics_2024_q1.html': ('שתי מכוניות ותחנת אוטובוס', "תנועת שתי מכוניות א' ו-ב' ועצירה בתחנת אוטובוס."),
 'kinematics_2025_q1.html': ('ניתור כדור משולחן', 'ניסוי ניתור כדור משולחן אופקי (מעבדה / קינמטיקה).'),
 'projectiles_1993_q1.html': ('צילום סטרובוסקופי', B_PROJ),
 'projectiles_2001_q2.html': ('כדור פורח', B_PROJ),
 'projectiles_2004_q1.html': ('חץ ותפוח', B_PROJ),
 'projectiles_2016_q1.html': ('גרם מדרגות', B_PROJ),
 'projectiles_2017_q1.html': ('בעיטת פננקה בכדורגל', B_PROJ),
 'projectiles_2021_q3.html': ('ניסוי זריקה אופקית', B_PROJ),
 'projectiles_2025_q1.html': ('הטלת כידון', B_PROJ),
 'forces_2015_q2.html': ('תאוצה במורד מדרון', 'ניסוי: התאוצה במורד מדרון כפונקציה של מקדם החיכוך.'),
 'forces_2016_q1.html': ('שמעון והחתול', 'תנועה בממד אחד עם חיכוך.'),
 'forces_2016_q2.html': ('מכונת אטווד', 'דוח מעבדה בשני קטעים על מכונת אטווד.'),
 'forces_2017_q2.html': ('חיכוך סטטי וקינטי', 'חקר כוח החיכוך הסטטי והקינטי.'),
 'forces_2018_q2.html': ('מדרון חלק ומשקולת תלויה', 'ניתוח ליניארי של התאוצה כפונקציה של הכוח.'),
 'forces_2019_q2.html': ('קריעת חוט על מישור משופע', 'חקר תנועה על מישור משופע חלק וקריעת החוט.'),
 'forces_2020_q1.html': ('נחיתת "בראשית"', 'נחיתה רכה של הגשושית "בראשית" על הירח.'),
 'forces_2020_q2.html': ('שני מישורים משופעים', 'שני גופים על שני מישורים משופעים עם חיכוך.'),
 'forces_2021_q2.html': ('מערכת גלגלת אנכית', B_FORCES),
 'forces_2022_q2.html': ('מסילה חלקה ותיבה', 'שלושה ניסויים עם מסילה חלקה ותיבה.'),
 'forces_2023_q1.html': ('מישור משופע', 'תנועה על מישור משופע חלק ועל מישור עם חיכוך.'),
 'forces_2023_q2.html': ('שני גופים וחיישן מתיחות', 'שני גופים קשורים אנכית וחיישן מתיחות.'),
 'forces_2024_q2.html': ('משיכת תיבה עם חיכוך', 'ניסוי משיכת תיבה עם חיכוך.'),
 'forces_2025_q2.html': ('גוף על מישור משופע', B_FORCES),
 'forces_atwood.html': ('מכונת אטווד', B_FORCES),
 'forces_bounce.html': ('כדור מנתר משולחן', B_FORCES),
 'forces_elevator.html': ('תמי במעלית', 'קריאת מאזני הרצפה במעלית כפונקציה של הזמן.'),
 'forces_incline_friction.html': ('מישור משופע עם חיכוך', B_FORCES),
 'energy_incline_work.html': ('עבודה ואנרגיה במישור משופע', 'בונים את הפתרון צעד אחר צעד: עבודה ואנרגיה במישור משופע.'),
 'energy_circular_loop.html': ('תנועה מעגלית אנכית (לולאה)', 'תנועה מעגלית אנכית ועבודת כוחות לא משמרים.'),
}
esc = html.escape


def kind_of(name, title):
    if name.endswith('.pdf'):
        return 'pdf'
    if name in SIMS or 'simulation' in name:
        return 'sim'
    if 'בונה הפתרון' in title or 'builder' in name:
        return 'builder'
    if re.search(r'_(19|20)\d{2}_q\d', name):
        return 'bagrut'
    return 'unit'


def collect():
    items, missing = [], []
    for folder in SECTIONS:
        if not os.path.isdir(folder):
            continue
        for f in sorted(os.listdir(folder)):
            if f == 'index.html' or not f.endswith(('.html', '.pdf')):
                continue
            title = ''
            if f.endswith('.html'):
                m = re.search(r'<title>([^<]*)</title>',
                              open(os.path.join(folder, f), encoding='utf-8', errors='ignore').read(5000))
                title = m.group(1).strip() if m else f
            kd = kind_of(f, title)
            ym = re.search(r'_((?:19|20)\d{2})_q(\d)', f)
            year, q = (ym.group(1), ym.group(2)) if ym else ('', '')
            if f in META:
                name, desc = META[f]
            else:
                name = re.sub(r'^בונה הפתרון\s*[-—]\s*', '', title) or f
                desc = ''
                missing.append(folder + '/' + f)
            items.append(dict(folder=folder, file=f, kind=kd, year=year, q=q, name=name, desc=desc))
    return items, missing


def pill(it):
    k = it['kind']
    if k == 'bagrut':
        return 'בגרות %s · שאלה %s' % (it['year'], it['q'])
    if k == 'builder':
        return 'בונה פתרון' + (' · בגרות %s · שאלה %s' % (it['year'], it['q']) if it['year'] else '')
    return {'sim': 'סימולציה', 'unit': 'יחידת לימוד', 'pdf': 'סיכום PDF'}[k]


def card(it, href, topic=''):
    _, _, bg, fg, kstrong, openlbl = K[it['kind']]
    strong = TOPIC[it['folder']][0]
    extra = '<span class="topic">%s</span>' % esc(topic) if topic else ''
    tgt = ' target="_blank"' if it['kind'] == 'pdf' else ''
    return ('<a class="card" href="%s"%s data-year="%s" data-topic="%s" style="border-top:4px solid %s">'
            '<span class="pill" style="background:%s;color:%s">%s</span><b>%s</b>'
            '<span class="desc">%s</span>%s<span class="open" style="color:%s">%s ←</span></a>') % (
        esc(href), tgt, it['year'], esc(it['folder']), strong, bg, fg, esc(pill(it)), esc(it['name']),
        esc(it['desc']), extra, strong, openlbl)


def sections_html(items, href_of, with_topic=False, tcol=None):
    out = []
    for k, heading, bg, fg, strong, _ in KINDS:
        its = [i for i in items if i['kind'] == k]
        if not its:
            continue
        its.sort(key=lambda i: (-(int(i['year']) if i['year'] else 0), i['q'], i['file']))
        cards = '\n'.join(card(i, href_of(i), SECTIONS[i['folder']][0] if with_topic else '') for i in its)
        out.append('<section class="grp"><h2 style="color:%s;border-color:%s">%s <span class="cnt">(%d)</span></h2>\n'
                   '<div class="grid">\n%s\n</div></section>' % (tcol or fg, tcol or strong, esc(heading), len(its), cards))
    return '\n'.join(out)


CSS = '''*{box-sizing:border-box}
body{margin:0;background:#f1f5f9;color:#0f172a;font-family:Heebo,system-ui,sans-serif;padding:24px 16px 60px}
.wrap{max-width:1100px;margin:0 auto}
.top{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;font-size:.9rem;color:#64748b}
.top a{color:#1D4ED8;font-weight:700;text-decoration:none}
h1{text-align:center;font-size:1.9rem;margin:18px 0 6px}
.sub{text-align:center;color:#475569;margin:0 0 22px}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:0 0 10px}
.chips button{background:#fff;color:#0f172a;border:1px solid #cbd5e1;border-radius:999px;padding:6px 14px;font:700 .85rem Heebo,sans-serif;cursor:pointer}
.chips button.on{background:#1D4ED8;border-color:#1D4ED8;color:#fff}
.grp{margin:30px 0 0}
.grp h2{font-size:1.25rem;border-right:5px solid;padding-right:10px;margin:0 0 14px}
.cnt{color:#64748b;font-weight:500;font-size:1rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.card{display:flex;flex-direction:column;gap:8px;background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:16px;color:#0f172a;text-decoration:none;box-shadow:0 2px 6px rgba(15,23,42,.06);transition:transform .15s,box-shadow .15s}
.card:hover{transform:translateY(-3px);box-shadow:0 8px 18px rgba(15,23,42,.12)}
.pill{align-self:flex-start;font-size:.78rem;font-weight:700;padding:3px 10px;border-radius:999px}
.card b{font-size:1.08rem;line-height:1.35}
.desc{font-size:.9rem;color:#475569;line-height:1.5;flex:1}
.topic{font-size:.8rem;color:#64748b}
.open{font-size:.88rem;font-weight:700}
.empty{background:#fff;border:1px dashed #cbd5e1;border-radius:14px;padding:28px;text-align:center;color:#64748b;margin-top:24px}'''
JS = '''<script>
var st={topic:'all',year:'all'};
function setF(k,v,btn){
  st[k]=v;
  btn.parentNode.querySelectorAll('button').forEach(function(b){b.classList.remove('on');});
  btn.classList.add('on');
  document.querySelectorAll('.card').forEach(function(el){
    var ok=(st.topic==='all'||el.dataset.topic===st.topic)&&(st.year==='all'||el.dataset.year===st.year);
    el.style.display=ok?'':'none';
  });
  document.querySelectorAll('.grp').forEach(function(g){
    var any=Array.prototype.some.call(g.querySelectorAll('.card'),function(e){return e.style.display!=='none';});
    g.style.display=any?'':'none';
  });
}
</script>'''


def page(title, top, h1, sub, chips, body, accent='#1D4ED8'):
    return ('<!DOCTYPE html>\n<html lang="he" dir="rtl">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>%s</title>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;500;700;800&display=swap" rel="stylesheet">\n'
            '<style>\n%s\n</style>\n</head>\n<body>\n<div class="wrap">\n%s\n<h1>%s</h1>\n<p class="sub">%s</p>\n%s\n%s\n</div>\n%s\n</body>\n</html>\n') % (
        esc(title), CSS.replace('#1D4ED8', accent), top, esc(h1), esc(sub), chips, body, JS)


def year_chips(items):
    years = sorted({i['year'] for i in items if i['year']}, reverse=True)
    if not years:
        return ''
    return ('<div class="chips"><button class="on" onclick="setF(\'year\',\'all\',this)">כל השנים</button>'
            + ''.join('<button onclick="setF(\'year\',\'%s\',this)">%s</button>' % (y, y) for y in years) + '</div>')


def main():
    items, missing = collect()
    for folder, (h1, sub, parent) in SECTIONS.items():
        if not os.path.isdir(folder):
            continue
        its = [i for i in items if i['folder'] == folder]
        top = ('<div class="top"><a href="../index.html">← חזרה ל%s</a><span>ראשי / %s / %s</span>'
               '<a href="../../catalog.html">כל החומרים</a></div>') % (esc(parent), esc(parent), esc(h1))
        body = sections_html(its, lambda i: i['file'], False, TOPIC[folder][0]) if its else '<div class="empty">החומרים לנושא זה יתווספו בקרוב.</div>'
        open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8').write(
            page(h1, top, h1, sub, year_chips(its), body, TOPIC[folder][0]))
    topics = [(f, SECTIONS[f][0]) for f in SECTIONS if any(i['folder'] == f for i in items)]
    tchips = ('<div class="chips"><button class="on" onclick="setF(\'topic\',\'all\',this)">כל הנושאים</button>'
              + ''.join('<button onclick="setF(\'topic\',\'%s\',this)">%s</button>' % (esc(f), esc(n)) for f, n in topics)
              + '</div>')
    top = '<div class="top"><a href="index.html">← חזרה לעמוד הראשי</a><span>כל החומרים</span></div>'
    open('catalog.html', 'w', encoding='utf-8').write(
        page('כל החומרים | איליה וינוקור', top, 'כל החומרים', 'סינון לפי נושא ושנה', tchips + year_chips(items),
             sections_html(items, lambda i: i['folder'] + '/' + i['file'], True)))
    print('items:', len(items), '| sections written:', sum(os.path.isdir(f) for f in SECTIONS))
    print('files without description (add to META):', missing or 'none')


if __name__ == '__main__':
    main()
