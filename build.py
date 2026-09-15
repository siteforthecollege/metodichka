"""Build a portable static website; Python standard library only."""
import html
import json
from pathlib import Path
from urllib.parse import quote, urlencode
from materials import MATERIALS, CATEGORIES, SOURCES

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
CONFIG = json.loads((ROOT / 'site.json').read_text())
TEACHER = CONFIG['teacher']
REPO = CONFIG['repository']
MODULE = 'Оформление и компоновка технической документации'
OUT.mkdir(exist_ok=True)
(OUT / 'materials').mkdir(exist_ok=True)
(OUT / 'downloads').mkdir(exist_ok=True)
e = html.escape

def date_text(value):
    y, m, d = value.split('-')
    months = ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря']
    return f'{int(d)} {months[int(m)-1]} {y}'

def link(path, text, cls=''):
    return f'<a class="{cls}" href="{e(path, quote=True)}">{e(text)}</a>'

def base(title, content, prefix='', active='materials', body_class=''):
    nav = ''.join(link(prefix + href, label, 'nav-link active' if active==key else 'nav-link') for key,href,label in [
        ('materials','index.html','Материалы'),('method','method.html','Коллегам'),('contact','contact.html','Обратная связь')])
    initials = ''.join(x[0] for x in TEACHER.split()[:2])
    analytics = ''
    if CONFIG.get('analyticsUrl','').startswith('https://'):
        analytics = link(CONFIG['analyticsUrl'], 'Статистика посещений')
    counter_key = 'siteforthecollege.github.io/metodichka'
    counter_url = f'https://hits.sh/{counter_key}/'
    counter_badge = f'https://hits.sh/{counter_key}.svg?' + urlencode({
        'label': 'Просмотры сайта', 'color': '235cc7',
        'labelColor': '142b4e', 'style': 'flat', 'view': 'total'
    })
    counter = f'<div class="visit-counter"><a href="{counter_url}" target="_blank" rel="noopener noreferrer" title="Общий счётчик просмотров всех страниц. Открыть статистику Hits.sh"><img src="{e(counter_badge, quote=True)}" alt="Просмотры сайта — общий счётчик" height="24" referrerpolicy="no-referrer" data-visit-counter></a><small>Общие просмотры страниц · <a href="{counter_url}" target="_blank" rel="noopener noreferrer">Статистика</a></small></div>'
    favicon = quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#142b4e"/><path d="M7 8h7l2 2 2-2h7v16h-7l-2 2-2-2H7Z" fill="none" stroke="#fff" stroke-width="2"/><path d="M16 10v16" stroke="#e0a453" stroke-width="2"/></svg>')
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · {e(TEACHER)}</title><meta name="description" content="Учебно-методические материалы преподавателя {e(TEACHER)}: разработка информационных систем, программный код и техническая документация. 2025–2026 учебный год.">
<meta name="theme-color" content="#142b4e"><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{favicon}">
<link rel="stylesheet" href="{prefix}style.css"><script defer src="{prefix}site.js"></script></head>
<body class="{body_class}"><a href="#main" class="skip-link">К содержанию</a>
<header class="topbar"><a class="brand" href="{prefix}index.html"><span class="brand-icon" aria-hidden="true">М</span><span>Методический<br><strong>кабинет</strong></span></a><nav aria-label="Основная навигация">{nav}</nav><span class="year">2025–2026 <span>учебный год</span></span></header>
{content}
<footer class="footer"><div><strong>{e(TEACHER)}</strong><span>Учебно-методические материалы · 2025–2026</span></div>{counter}<div>{link(prefix+'contact.html','Задать вопрос')}{analytics}</div></footer></body></html>'''

def material_card(m, num):
    return f'''<article class="card"><div class="card-top"><span class="kind">{e(m['kind'])}</span><span class="card-number">{num:02}</span></div>
<h3>{link('materials/'+m['id']+'.html',m['title'])}</h3><p>{e(m['goal'])}</p>
<div class="card-bottom"><time datetime="{m['date']}">{date_text(m['date'])}</time><a href="materials/{m['id']}.html" class="read-link" aria-label="Открыть: {e(m['title'])}">Читать <span aria-hidden="true">↗</span></a></div></article>'''

sidebar = ''.join(f'<a href="#{k}"><span>{v[2]}</span>{e(v[0])}<small>{sum(m["category"]==k for m in MATERIALS)}</small></a>' for k,v in CATEGORIES.items())
sections = ''
for cat, (name,kind,num,period) in CATEGORIES.items():
    sections += f'<section class="subject" id="{cat}"><div class="section-head"><span class="section-no">{num}</span><div><p class="eyebrow">{kind}</p><h2>{e(name)}</h2></div></div>'
    if kind == 'Практика':
        sections += f'<p class="module">Модуль «{MODULE}»</p>'
    for semester in [1,2]:
        group = [m for m in MATERIALS if m['category']==cat and m['semester']==semester]
        if not group: continue
        per = ('Ноябрь — декабрь 2025' if semester==1 else 'Июнь — июль 2026') if kind=='Практика' else period
        sections += f'<div class="semester-label"><span>{semester} семестр</span><span>{per}</span><span>4 материала</span></div><div class="cards">'
        sections += ''.join(material_card(m,i+1) for i,m in enumerate(group)) + '</div>'
    sections += '</section>'

home = f'''<main id="main"><section class="intro"><div><p class="eyebrow">Личный сайт преподавателя</p><h1>{e(TEACHER)}</h1><p class="role">{e(CONFIG['role'])}</p><p class="intro-copy">От проектирования информационной системы<br class="desktop-break"> до программного кода и технической документации.</p><a class="button light" href="#systems">Перейти к материалам <span aria-hidden="true">↓</span></a></div><div class="intro-aside"><span class="academic">Учебный архив</span><strong>2025<span>—</span>2026</strong><div class="intro-counts"><div><b>24</b><span>материала</span></div><div><b>2</b><span>дисциплины</span></div><div><b>2</b><span>вида практики</span></div></div></div></section>
<div class="content-layout"><aside class="sidebar"><p class="eyebrow">Навигация по курсам</p><nav aria-label="Разделы материалов">{sidebar}</nav><div class="calendar-note"><span class="eyebrow">Учебный календарь</span><p><strong>I семестр</strong><br>Сентябрь — декабрь 2025</p><p><strong>II семестр</strong><br>12 января — июль 2026</p><p class="muted">Практики — в последние два месяца каждого семестра.</p></div></aside><div class="subjects"><div class="catalog-heading"><h2>Учебные материалы</h2><span>Объяснение · Пример · Практика</span></div>{sections}</div></div></main>'''
(OUT/'index.html').write_text(base('Методический кабинет',home),encoding='utf-8')

for m in MATERIALS:
    title=m['title']; cat=CATEGORIES[m['category']][0]
    practical=m['category'] in ('training','production')
    group=[v for v in MATERIALS if v['category']==m['category'] and v['semester']==m['semester']]
    pos=group.index(m)
    issue=f'https://github.com/{REPO}/issues/new?'+urlencode({'title':'Вопрос по материалу: '+title,'body':'Материал: '+title+'\n\nМой вопрос:\n'})
    steps=''.join(f'<li>{e(s)}</li>' for s in m['steps'])
    questions=''.join(f'<li>{e(q)}</li>' for q in m['questions'])
    sources=''.join(f'<li>{link(SOURCES[s][1],SOURCES[s][0])}</li>' for s in m['source'])
    example=f'<pre><code>{e(m["example"])}</code></pre>' if m['example'].startswith(('def ','import ')) else f'<div class="example"><p>{e(m["example"])}</p></div>'
    previous=link(group[pos-1]['id']+'.html','← '+group[pos-1]['title']) if pos else '<span></span>'
    nextlink=link(group[pos+1]['id']+'.html',group[pos+1]['title']+' →') if pos+1<len(group) else '<span></span>'
    content=f'''<main id="main" class="reading"><nav class="breadcrumbs" aria-label="Хлебные крошки">{link('../index.html','Материалы')}<span>/</span>{link('../index.html#'+m['category'],cat)}</nav>
<header class="article-header"><p class="eyebrow">{e(m['kind'])} · {m['semester']} семестр</p><h1>{e(title)}</h1>{f'<p class="module">Модуль «{MODULE}»</p>' if practical else ''}<div class="article-meta"><span>{e(TEACHER)}</span><span>Публикация: <time datetime="{m['date']}">{date_text(m['date'])}</time></span></div><div class="article-actions"><a class="button" download href="../downloads/{m['id']}.md">Скачать материал <span class="file-type">MD</span></a><button class="button secondary" type="button" data-print>Печать / PDF</button>{link(issue,'Задать вопрос','text-link')}</div></header>
<article class="lesson"><div class="goal"><span class="eyebrow">После работы вы сможете</span><p>{e(m['goal'])}</p></div><section><h2>Разберёмся в теме</h2><p>{e(m['theory'])}</p></section><section><h2>Пример</h2>{example}</section><section><h2>Выполните задание</h2><ol class="steps">{steps}</ol></section><aside class="extension">{e(m['extra'])}</aside><section><h2>Что представить</h2><p>{e(m['result'])}</p></section><section><h2>Проверьте себя</h2><ol>{questions}</ol><details><summary>Ориентиры для ответа</summary><p>{e(m['answer'])}</p></details></section>
<section><h2>Критерии проверки</h2><div class="table-wrap"><table><thead><tr><th>Критерий</th><th>Баллы</th></tr></thead><tbody><tr><td>Результат соответствует поставленной задаче и примеру</td><td>0–4</td></tr><tr><td>Выполнены все основные шаги, представлены подтверждения</td><td>0–3</td></tr><tr><td>Оформление понятно, файлы и ссылки работают</td><td>0–2</td></tr><tr><td>Студент объясняет решение и ограничения</td><td>0–1</td></tr></tbody></table></div><p class="note">Учебная шкала: 9–10 баллов — «5», 7–8 — «4», 5–6 — «3», 0–4 — работа требует доработки. Итоговое оценивание — по требованиям преподавателя.</p></section><section class="sources"><h2>Источники и дополнительное чтение</h2><ul>{sources}</ul><p class="note">Задание и учебные примеры составлены для самостоятельной работы. По ссылкам доступна документация для уточнения технических деталей.</p></section></article><nav class="lesson-nav" aria-label="Следующие материалы">{previous}{nextlink}</nav></main>'''
    (OUT/'materials'/f'{m["id"]}.html').write_text(base(title,content,'../'),encoding='utf-8')
    md=f'# {title}\n\n{TEACHER}\n\n{cat} · {m["semester"]} семестр · Публикация: {date_text(m["date"])}\n\n'
    if practical: md+=f'Модуль: {MODULE}\n\n'
    md+=f'## Цель\n\n{m["goal"]}\n\n## Краткое объяснение\n\n{m["theory"]}\n\n## Пример\n\n'
    md+=('```python\n'+m['example']+'\n```' if m['example'].startswith(('def ','import ')) else m['example'])+'\n\n## Задание\n\n'
    md+='\n'.join(f'{i+1}. {s}' for i,s in enumerate(m['steps']))
    md+=f'\n\n{m["extra"]}\n\n## Что представить\n\n{m["result"]}\n\n## Самопроверка\n\n'+'\n'.join(f'{i+1}. {q}' for i,q in enumerate(m['questions']))
    md+=f'\n\nОриентиры: {m["answer"]}\n\n## Критерии\n\nСоответствие задаче — 4 балла; полнота и подтверждения — 3; оформление — 2; объяснение — 1. 9–10: «5»; 7–8: «4»; 5–6: «3»; 0–4: доработка. Учебная шкала, итог — по требованиям преподавателя.\n\n## Источники\n\n'
    md+='\n'.join(f'- [{SOURCES[s][0]}]({SOURCES[s][1]})' for s in m['source'])+'\n'
    (OUT/'downloads'/f'{m["id"]}.md').write_text(md,encoding='utf-8')

method=f'''<main id="main" class="reading"><p class="eyebrow">Методическая поддержка</p><h1>Коллегам-преподавателям</h1><p class="lead">Как использовать материалы на занятиях и помогать студентам с разным уровнем подготовки.</p><article class="lesson"><section><h2>Один проект на весь учебный год</h2><p>Общий пример — система учета заявок на ремонт техники в колледже. В первом семестре студенты формулируют требования, проектируют данные и интерфейс. Во втором — реализуют функции, хранение данных и проверки. На практиках оформляют и согласуют документацию.</p></section><section><h2>От простого действия к самостоятельной работе</h2><ol class="steps"><li>Начните с разбора готового примера: попросите студента объяснить входные данные и ожидаемый результат.</li><li>Предложите повторить пример, изменив одно значение. Для слабой группы сократите число объектов, сохранив смысл задания.</li><li>Перейдите к основным шагам работы. После первых двух шагов проверьте результат, чтобы ошибка не перенеслась дальше.</li><li>Дайте дополнительное условие тем, кто справился раньше. Оно размещено после задания каждого материала.</li><li>Попросите объяснить одно решение и одну найденную ошибку. Оценивайте не только внешний вид результата.</li></ol></section><section><h2>Какие трудности можно отработать</h2><div class="table-wrap"><table><thead><tr><th>Трудность</th><th>Материал и прием</th></tr></thead><tbody><tr><td>Студент сразу пишет код, не понимая задачи</td><td>{link('materials/is-requirements.html','Требования')}: сформулировать наблюдаемый результат до выбора технологии</td></tr><tr><td>Не умеет проверять граничные случаи</td><td>{link('materials/code-tests.html','Модульные тесты')}: сравнить 4, 5 и 6 символов</td></tr><tr><td>Оформляет документ вручную и теряет структуру</td><td>{link('materials/up-layout.html','Стили и оглавление')}: изменить один заголовок и обновить оглавление</td></tr><tr><td>Считает исправление доказанным без проверки</td><td>{link('materials/pp-review.html','Проверка комплекта')}: повторить сценарий после исправления</td></tr></tbody></table></div></section><section><h2>Адаптация под рабочую программу</h2><p>Материалы — учебные разработки по заявленным темам. До применения сверьте их с действующей рабочей программой, заданиями практики, доступным оборудованием и локальными критериями оценивания. Часы и коды компетенций здесь не назначены без исходной программы.</p></section><section><h2>Обмен опытом</h2><p>Можно задать вопрос по конкретному заданию, предложить уточнение или сообщить о найденной ошибке.</p>{link('contact.html','Перейти к обратной связи','button')}</section></article></main>'''
(OUT/'method.html').write_text(base('Коллегам',method,active='method'),encoding='utf-8')

contact=f'''<main id="main" class="reading contact-page"><p class="eyebrow">Обратная связь</p><h1>Задать вопрос преподавателю</h1><p class="lead">Вопрос по заданию, замечание к материалу или предложение для совместной методической работы.</p><div class="contact-grid"><form id="feedback" data-repository="{e(REPO)}"><label for="topic">Тема</label><select id="topic" name="topic"><option>Вопрос по учебному материалу</option><option>Ошибка или неточность</option><option>Методическое сотрудничество</option></select><label for="material">Название материала <span class="muted">(если есть)</span></label><input id="material" name="material" maxlength="180" placeholder="Например, «Модель данных»"><label for="message">Ваш вопрос</label><textarea id="message" name="message" rows="6" required minlength="10" maxlength="4000" placeholder="Укажите шаг задания и что вызвало затруднение."></textarea><p class="note">Не указывайте пароли, персональные данные студентов и внутреннюю информацию организации: обращение будет публичным.</p><button class="button" type="submit">Подготовить обращение ↗</button><p id="feedback-status" role="status"></p></form><aside class="contact-note"><h2>Как отправить</h2><p>Кнопка откроет GitHub с заполненным текстом. Войдите в свой аккаунт, проверьте обращение и нажмите Create.</p><p>До подтверждения на GitHub сообщение не отправляется.</p>{link('https://github.com/'+REPO+'/issues','Посмотреть обсуждения','text-link')}<noscript><p>Для заполнения формы включите JavaScript или откройте обсуждения по ссылке выше.</p></noscript></aside></div></main>'''
if CONFIG.get('email'):
    contact=contact.replace('</aside>',f'<p>{link("mailto:"+CONFIG["email"],CONFIG["email"])}</p></aside>')
(OUT/'contact.html').write_text(base('Обратная связь',contact,active='contact'),encoding='utf-8')
(OUT/'404.html').write_text(base('Страница не найдена','<main id="main" class="reading"><p class="eyebrow">404</p><h1>Такой страницы нет</h1><p>Возможно, материал был перемещен. Вернитесь к списку разделов.</p><a class="button" href="/metodichka/">Открыть материалы</a></main>'),encoding='utf-8')
for name in ['style.css','site.js']:
    (OUT/name).write_text((ROOT/name).read_text(),encoding='utf-8')
(OUT/'.nojekyll').write_text('')
print(f'Built {len(MATERIALS)} materials and 4 service pages in {OUT}')
