#!/usr/bin/env python3
"""G20YEA Japan Council サイトのHTMLを生成する。

使い方（リポジトリのルートで）:
    python3 scripts/site/build.py docs

データ:
    scripts/site/members.json  … メンバー・スタッフ・メンバー紹介ページの内容
    scripts/site/activities.py … 「最近の活動」ページの内容
デザイン:
    docs/assets/css/site.css, docs/assets/js/site.js
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import activities as ACT  # noqa: E402

DOCS = sys.argv[1] if len(sys.argv) > 1 else 'docs'
DATA = json.load(open(os.path.join(HERE, 'members.json'), encoding='utf-8'))
SITE = 'G20 YEA Japan Council'
ORIGIN = 'https://g20yea.jp/'
UP = 'wp-content/uploads/'
HERO_IMG = UP + '2025/06/54255599_2300495630009380_981151627702435840_n.jpg'
ABOUT_IMG = UP + '2025/06/Gemini_Generated_Image_m5kfi7m5kfi7m5kf-1024x1024.png'
MAIL = 'ask@g20yea.jp'

e = html.escape

# ---------------------------------------------------------------- icons
ICON = {
    'arrow': '<svg class="arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    'ig': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
    'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    'tel': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    'web': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg>',
}

NAV = [
    ('activities/', '最近の活動'),
    ('g20-yea-japan-council-members-information/', 'メンバー紹介'),
    ('g20-yea-japan-council-staffmembers/', 'スタッフ'),
]


# ---------------------------------------------------------------- helpers
def rel(depth):
    return '../' * depth


def href(r, path):
    """サイト内パス（'' / 'ask/' など）→ 相対リンク。index.html を明示（ローカル閲覧でも動くように）"""
    return r + (path if path.endswith('.html') else path + 'index.html')


def fmt_date(d):
    y, m, dd = d.split('-')
    return f'{y}年{int(m)}月{int(dd)}日'


def initial(name):
    return (name.strip() or '?')[0]


def field(p, label):
    for k, v in p['fields']:
        if k == label:
            return v
    return ''


def plain(v):
    return re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', r'\2', v)


def rich(v):
    """members.json のテキスト → HTML（改行と [[URL|テキスト]] リンク）"""
    parts = re.split(r'(\[\[[^\]]+\]\])', v)
    out = []
    for part in parts:
        m = re.match(r'\[\[([^|\]]+)\|([^\]]+)\]\]', part)
        if m:
            out.append(f'<a href="{e(m.group(1))}" target="_blank" rel="noopener">{e(m.group(2))}</a>')
        else:
            out.append(e(part))
    s = ''.join(out)
    s = re.sub(r'\n{2,}', '<br><br>', s)
    return s.replace('\n', '<br>')


def first_url(v):
    m = re.search(r'\[\[([^|\]]+)\|', v) or re.search(r'https?://\S+', v)
    if not m:
        return ''
    return m.group(1) if m.lastindex else m.group(0)


def person_photo(r, photo, name, lazy=True):
    if photo:
        return f'<img src="{r}{e(photo)}" alt="{e(name)}"{" loading=\"lazy\"" if lazy else ""}>'
    return f'<span class="person__initial" aria-hidden="true">{e(initial(name))}</span>'


# ---------------------------------------------------------------- layout
def layout(path, title, body, *, desc='', active='', og_image=HERO_IMG, full_title=None):
    depth = path.count('/')
    r = rel(depth)
    page_title = full_title or (f'{title} | {SITE}' if title else f'{SITE} | G20の若手起業家のグローバルネットワーク')
    url = ORIGIN + path
    nav = ''.join(
        f'<a href="{href(r, p)}"{" aria-current=\"page\"" if active == p else ""}>{e(label)}</a>' for p, label in NAV)
    desc = desc or 'G20YEA Japan Councilは、G20加盟国の若手起業家で構成されるG20YEA（Young Entrepreneurs’ Alliance）の日本代表団体です。'
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(page_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(url)}">
<meta property="og:site_name" content="{SITE}">
<meta property="og:title" content="{e(page_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="{'website' if not path else 'article'}">
<meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{ORIGIN}{e(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a1020">
<link rel="icon" href="{r}{UP}2025/07/cropped-logo-1-32x32.jpg" sizes="32x32">
<link rel="icon" href="{r}{UP}2025/07/cropped-logo-1-192x192.jpg" sizes="192x192">
<link rel="apple-touch-icon" href="{r}{UP}2025/07/cropped-logo-1-180x180.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Noto+Sans+JP:wght@400;700;900&display=swap">
<link rel="stylesheet" href="{r}assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">本文へスキップ</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{href(r, '')}" aria-label="{SITE} トップ">
      <img src="{r}{UP}2025/07/logo.jpg" alt="G20 Young Entrepreneurs' Alliance" width="548" height="166">
      <span class="brand__jc"><b>JAPAN</b>COUNCIL</span>
    </a>
    <button class="nav-toggle" type="button" aria-label="メニュー" aria-expanded="false" aria-controls="gnav"><span></span><span></span><span></span></button>
    <nav class="gnav" id="gnav" aria-label="メインメニュー">
      {nav}
      <a class="btn btn--red btn--sm" href="{href(r, 'ask/')}"{" aria-current=\"page\"" if active == 'ask/' else ""}>入会・お問い合わせ</a>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer__top">
      <div>
        <div class="footer__brand"><i></i><div>G20 YEA<br>Japan Council<small>YOUNG ENTREPRENEURS’ ALLIANCE</small></div></div>
        <div class="social">
          <a href="{ACT.IG}" target="_blank" rel="noopener">{ICON['ig']} Instagram</a>
          <a href="mailto:{MAIL}">{ICON['mail']} {MAIL}</a>
        </div>
      </div>
      <div>
        <h3>MENU</h3>
        <ul>
          <li><a href="{href(r, '')}">トップ</a></li>
          {''.join(f'<li><a href="{href(r, p)}">{e(l)}</a></li>' for p, l in NAV)}
          <li><a href="{href(r, 'ask/')}">入会の申し込み・お問い合わせ</a></li>
        </ul>
      </div>
      <div>
        <h3>LINKS</h3>
        <ul>
          <li><a href="https://www.g20yea.com/" target="_blank" rel="noopener">G20YEA（国際本部）</a></li>
          <li><a href="{href(r, '最新情報/')}">最新情報</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__bottom">
      <span>Copyright © G20 YEA Japan Council All Rights Reserved.</span>
      <a href="#main">PAGE TOP ↑</a>
    </div>
  </div>
</footer>
<script src="{r}assets/js/site.js" defer></script>
</body>
</html>
'''


def page_hero(r, en, title, lead='', crumbs=()):
    cr = [f'<a href="{href(r, "")}">TOP</a>']
    for p, label in crumbs:
        cr.append('<span aria-hidden="true">/</span>')
        cr.append(f'<a href="{href(r, p)}">{e(label)}</a>' if p is not None else f'<span>{e(label)}</span>')
    return f'''<section class="page-hero">
  <div class="wrap">
    <div class="page-hero__en" aria-hidden="true">{e(en)}</div>
    <h1>{e(title)}</h1>
    {f'<p>{lead}</p>' if lead else ''}
    <nav class="crumbs" aria-label="パンくずリスト">{''.join(cr)}</nav>
  </div>
</section>'''


def write(path, content):
    out = os.path.join(DOCS, path, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(content)
    WRITTEN.append(path)


WRITTEN = []

# ---------------------------------------------------------------- data
members = DATA['members']
staff = DATA['staff']
profiles = DATA['profiles']
order_idx = {s: i for i, s in enumerate(DATA.get('order', []))}
POSTS = sorted(profiles.values(), key=lambda p: (p['date'], -order_idx.get(p['slug'], 99)), reverse=True)
HELLO = {'slug': 'hello-world', 'title': 'Hello world!', 'date': '2025-06-14',
         'text': 'WordPress へようこそ。こちらは最初の投稿です。編集または削除し、コンテンツ作成を始めてください。'}


def member_cards(r, items, staff_mode=False, limit=None):
    out = []
    for m in items[:limit]:
        p = profiles.get(m.get('slug') or '')
        photo = (p['photo'] if p and p['photo'] else '') or m['photo']
        if staff_mode and m['photo']:
            photo = m['photo']
        co = plain(field(p, '会社名')) if p else ''
        inner = f'''<div class="person__photo">{person_photo(r, photo, m['name'])}{'<span class="person__go">' + ICON['arrow'] + '</span>' if p else ''}</div>
<div class="person__body">{f'<div class="person__role">{e(m["role"])}</div>' if m.get('role') else ''}<div class="person__name">{e(m['name'])}</div>{f'<div class="person__co">{e(co)}</div>' if co else ''}</div>'''
        if p:
            out.append(f'<a class="person reveal" href="{href(r, p["slug"] + "/")}">{inner}</a>')
        else:
            out.append(f'<div class="person reveal">{inner}</div>')
    return ''.join(out)


def activity_card(r, ev, post, link, external=False):
    """external=True: Instagram の投稿へリンク（活動ページ用）。False: サイト内リンク（トップ用）"""
    code, date, title, text, alt = post
    meta = f'<span>{fmt_date(date)}</span>' if external else f'<span>{e(ev["when"])}</span><span>{e(ev["place"])}</span>'
    more = (f'<span class="card__more">{ICON["ig"].replace("<svg", "<svg width=16 height=16", 1)} Instagramで見る</span>'
            if external else f'<span class="card__more">続きを見る {ICON["arrow"]}</span>')
    attrs = ' target="_blank" rel="noopener"' if external else ''
    return f'''<a class="card reveal" href="{link}"{attrs}>
  <div class="card__img"><img src="{r}{UP}instagram/{code}.jpg" alt="{e(alt)}" width="512" height="640" loading="lazy"></div>
  <div class="card__body">
    <div class="card__meta">{meta}</div>
    <h3>{e(title)}</h3>
    <p>{e(text)}</p>
    {more}
  </div>
</a>'''


# ---------------------------------------------------------------- top
# トップに出す各イベントの代表写真（posts の何番目か）
TOP_PICK = {'vienna': 2, 'toronto': 2, 'tokyo': 0, 'colombo': 0}


def build_top():
    r = ''
    latest = ACT.EVENTS[0]
    ev_cards = ''.join(
        activity_card(r, ev, ev['posts'][TOP_PICK.get(ev['id'], 0)], href(r, 'activities/') + '#' + ev['id'])
        for ev in ACT.EVENTS[:3])
    # 同じ写真の重複を除く
    seen, strip_items = set(), []
    for m in members + staff:
        if m['photo'] and m['photo'] not in seen:
            seen.add(m['photo'])
            strip_items.append(f'<li><img src="{e(m["photo"])}" alt="" loading="lazy"></li>')
    strip = ''.join(strip_items[:9])
    body = f'''<section class="hero">
  <div class="hero__bg"><img src="{HERO_IMG}" alt="G20YEAサミットに集まった各国の若手起業家たち" fetchpriority="high"></div>
  <div class="wrap">
    <p class="hero__eyebrow"><i></i>G20 YOUNG ENTREPRENEURS’ ALLIANCE — JAPAN</p>
    <h1>Accelerate<br>your business<em>.</em></h1>
    <p class="hero__sub">G20の若手起業家のグローバルネットワーク</p>
    <div class="hero__cta">
      <a class="btn btn--red" href="{href(r, 'ask/')}">入会のお申し込み {ICON['arrow']}</a>
      <a class="btn btn--ghost" href="{href(r, 'activities/')}">最近の活動を見る</a>
    </div>
  </div>
  <div class="hero__news">
    <div class="wrap"><a href="{href(r, 'activities/')}#{latest['id']}"><b>LATEST</b><span>{e(latest['when'])}　{e(latest['title'])}（{e(latest['place'])}）</span>{ICON['arrow']}</a></div>
  </div>
</section>

<section class="stats" aria-label="G20YEAの規模">
  <div class="wrap stats__grid reveal">
    <div class="stat"><div class="stat__label">起業家の数</div><div class="stat__num"><span data-count="800">800</span><small>名</small></div><p>G20各国をはじめとして、様々な業種の起業家が社会への行動と新たな出会いを求めて集まっています。</p></div>
    <div class="stat"><div class="stat__label">起業家の出身国</div><div class="stat__num"><span data-count="25">25</span><small>カ国</small></div><p>G20各国はもちろんのこと、今後の成長が期待される国々からも多くの起業家が参加しています。</p></div>
    <div class="stat"><div class="stat__label">グローバル企業も協力</div><div class="stat__num"><span data-count="80">80</span><small>社</small></div><p>フォーブス・グローバル2000にリストアップされる企業もG20YEAの行動に賛同し、協力を表明しています。</p></div>
  </div>
</section>

<section class="section" id="about">
  <div class="wrap about">
    <div class="reveal">
      <p class="eyebrow">ABOUT G20YEA</p>
      <h2 class="section-title">G20YEAとは</h2>
      <p><span class="mark">G20YEA（Young Entrepreneurs’ Alliance）とはG20加盟国の若手起業家で構成される団体です。</span></p>
      <p>G20YEAは、G20の目的である<span class="mark">国際的な経済問題への対処、金融の安定、気候変動対策、持続可能な開発</span>といった主要な課題に対し、若手起業家の視点から貢献することを目指しています。</p>
      <p class="lead" style="font-size:15px">G20に参加する19カ国とEU、AUは、世界のGDPの約85%、国際貿易の75%、世界人口の56%、そして世界の陸地面積の60%を占めています。EUとAUを含めると、世界の人口の78.9%、化石燃料による世界のCO2排出量の83.9%を占めています。</p>
      <div class="figures">
        <div class="figure"><b>85<small>%</small></b><span>世界のGDP（約）</span></div>
        <div class="figure"><b>75<small>%</small></b><span>国際貿易</span></div>
        <div class="figure"><b>56<small>%</small></b><span>世界人口</span></div>
      </div>
    </div>
    <div class="about__media reveal"><img src="{ABOUT_IMG}" alt="" loading="lazy" width="1024" height="1024"></div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">ROLE</p><h2 class="section-title">G20YEAが担う役割</h2></div>
      <p class="lead" style="margin:0;max-width:520px">世界経済の大部分を占めるG20諸国の若手起業家が集まることで、以下の点で重要な役割を担っています。</p>
    </div>
    <div class="roles">
      <article class="role reveal"><div class="role__no">01</div><h3>政策提言</h3><p>各国の若手起業家が直面する課題や成功事例を共有し、G20首脳に対して若者や起業家精神の育成に関する政策提言を行います。</p></article>
      <article class="role reveal"><div class="role__no">02</div><h3>国際的なネットワーク構築</h3><p>世界中の若手起業家が交流し、新たなビジネスチャンスやイノベーションを生み出すためのネットワークを構築します。</p></article>
      <article class="role reveal"><div class="role__no">03</div><h3>グローバルな課題への貢献</h3><p>気候変動や持続可能な開発といった地球規模の課題に対し、起業家ならではの視点と行動力で解決策を探り、貢献します。</p></article>
      <article class="role reveal"><div class="role__no">04</div><h3>国際ビジネス人材育成</h3><p>G20YEAサミットで行われるフォーラムやトレーニングでグローバルなビジネスに携わる人材育成を行なっています。</p></article>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap council">
    <div class="reveal">
      <p class="eyebrow">JAPAN COUNCIL</p>
      <h2 class="section-title">G20YEA<br>Japan Councilとは</h2>
      <p class="lead">G20YEAの<span class="mark">日本を代表する団体</span>として、日本の若手起業家で構成される団体です。</p>
      <a class="btn btn--ghost" href="{href(r, 'g20-yea-japan-council-staffmembers/')}" style="margin-top:12px">運営スタッフを見る {ICON['arrow']}</a>
    </div>
    <div class="reveal">
      <p class="eyebrow" style="color:#fff">主な事業</p>
      <ol class="biz">
        <li><h3>G20YEA Summitへの参加</h3><p>毎年1回開催</p></li>
        <li><h3>G20YEA Japan主催事業</h3><p>総会・勉強会（国際投資、国際展開など）の開催（年2回程度）</p></li>
        <li><h3>G20YEA関連事業への参加</h3><p>G20YEA China等が開催する関連事業への参加</p></li>
        <li><h3>G20YEA加盟団体・企業との交流</h3><p>加盟国の企業とのネットワーキングを目的とした国別訪問</p></li>
        <li><h3>その他の国へのオフィシャルビジット</h3><p>国際的なビジネスチャンスのある地域への訪問</p></li>
      </ol>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><p class="eyebrow">RECENT ACTIVITIES</p><h2 class="section-title">最近の活動</h2></div>
      <a class="btn btn--line" href="{href(r, 'activities/')}">すべての活動を見る {ICON['arrow']}</a>
    </div>
    <div class="cards">{ev_cards}</div>
  </div>
</section>

<section class="section section--mist">
  <div class="wrap">
    <div class="members-cta reveal">
      <div>
        <p class="eyebrow">MEMBERS</p>
        <ul class="strip">{strip}</ul>
        <h2 class="section-title" style="margin-bottom:12px">多様な業種の起業家が参加しています</h2>
        <p class="lead" style="margin:0">エネルギー、金融、医療、不動産、貿易、専門サービスなど、日本各地の経営者がメンバーとして活動しています。</p>
      </div>
      <a class="btn btn--red" href="{href(r, 'g20-yea-japan-council-members-information/')}">メンバー紹介を見る {ICON['arrow']}</a>
    </div>
  </div>
</section>
{cta(r)}'''
    write('', layout('', '', body))


def cta(r):
    return f'''<section class="cta">
  <div class="wrap">
    <div>
      <h2>Join G20YEA<br>Japan Council</h2>
      <p>世界の若手起業家とつながる。入会のお申し込み・お問い合わせはこちらから。</p>
    </div>
    <a class="btn" href="{href(r, 'ask/')}">入会・お問い合わせ {ICON['arrow']}</a>
  </div>
</section>'''


# ---------------------------------------------------------------- members / staff
def build_members():
    path = 'g20-yea-japan-council-members-information/'
    r = rel(1)
    body = page_hero(r, 'MEMBERS', 'メンバー紹介', 'こちらのページではG20YEA Japan Council のメンバーをご紹介いたします。',
                     [(None, 'メンバー紹介')]) + f'''
<section class="section"><div class="wrap"><div class="people">{member_cards(r, members)}</div></div></section>
{cta(r)}'''
    write(path, layout(path, 'メンバー紹介', body, active=path,
                       desc='G20YEA Japan Councilのメンバー紹介。日本各地で活躍する若手起業家・経営者をご紹介します。'))


def build_staff():
    path = 'g20-yea-japan-council-staffmembers/'
    r = rel(1)
    body = page_hero(r, 'STAFF', 'スタッフメンバー一覧', 'G20YEA Japan Councilの運営を担うスタッフメンバーです。',
                     [(None, 'スタッフメンバー一覧')]) + f'''
<section class="section"><div class="wrap"><div class="people people--staff">{member_cards(r, staff, staff_mode=True)}</div></div></section>
{cta(r)}'''
    write(path, layout(path, 'スタッフメンバー一覧', body, active=path,
                       desc='G20YEA Japan Councilのスタッフメンバー一覧。'))


def build_profiles():
    listed = [m['slug'] for m in members if m['slug']]
    for p in profiles.values():
        path = p['slug'] + '/'
        r = rel(1)
        name = p['name'] or plain(field(p, '会社名'))
        co = plain(field(p, '会社名')) if p['name'] else ''
        contact = []
        mail = field(p, 'メールアドレス').strip()
        if mail:
            contact.append(f'<a href="mailto:{e(mail)}">{ICON["mail"]}{e(mail)}</a>')
        for lb in ('連絡先', '連絡先（WhatsApp）'):
            tel = field(p, lb).strip()
            if tel:
                contact.append(f'<a href="tel:{e(re.sub(r"[^0-9+]", "", tel.replace("＋", "+")))}">{ICON["tel"]}{e(tel)}{"（WhatsApp）" if "WhatsApp" in lb else ""}</a>')
        web = first_url(field(p, '会社HP URL'))
        if web:
            contact.append(f'<a href="{e(web)}" target="_blank" rel="noopener">{ICON["web"]}{e(re.sub(r"^https?://|/$", "", web))}</a>')
        rows = []
        for k, v in p['fields']:
            if k in ('メールアドレス', '連絡先', '連絡先（WhatsApp）', '会社HP URL') or not v.strip():
                continue
            rows.append(f'<div><dt>{e(k or "紹介")}</dt><dd>{rich(v)}</dd></div>')
        gallery = ''.join(f'<img src="{r}{e(i)}" alt="{e(co or name)}の紹介画像" loading="lazy">' for i in p['images'])
        pager = ''
        if p['slug'] in listed:
            i = listed.index(p['slug'])
            prev_s, next_s = (listed[i - 1] if i > 0 else None), (listed[i + 1] if i + 1 < len(listed) else None)
            def lk(s, cls, lab):
                if not s:
                    return '<span></span>'
                return f'<a class="{cls}" href="{href(r, s + "/")}"><small>{lab}</small>{e(profiles[s]["name"])}</a>'
            pager = f'''<nav class="pager" aria-label="メンバー移動">{lk(prev_s, "prev", "← PREV")}<a class="mid btn btn--line btn--sm" href="{href(r, "g20-yea-japan-council-members-information/")}">メンバー一覧へ</a>{lk(next_s, "next", "NEXT →")}</nav>'''
        else:
            pager = f'<nav class="pager" aria-label="メンバー移動"><span></span><a class="mid btn btn--line btn--sm" href="{href(r, "g20-yea-japan-council-members-information/")}">メンバー一覧へ</a><span></span></nav>'
        body = page_hero(r, 'MEMBER', name, '', [('g20-yea-japan-council-members-information/', 'メンバー紹介'), (None, name)]) + f'''
<section class="section">
  <div class="wrap profile">
    <aside class="profile__aside">
      <div class="profile__photo">{person_photo(r, p['photo'], name, lazy=False)}</div>
      <div class="profile__name">{e(name)}</div>
      {f'<div class="profile__co">{e(co)}</div>' if co else ''}
      <div class="profile__contact">{''.join(contact)}</div>
    </aside>
    <div>
      <p class="eyebrow">PROFILE</p>
      <dl class="dl">{''.join(rows)}</dl>
      {f'<div class="gallery">{gallery}</div>' if gallery else ''}
      {pager}
    </div>
  </div>
</section>'''
        desc = f'{name}（{co}）' if co else name
        pr = plain(field(p, '社業における得意分野・PRポイント')).replace('\n', ' ')[:90]
        write(path, layout(path, p['title'], body, active='g20-yea-japan-council-members-information/',
                           desc=f'G20YEA Japan Council メンバー紹介：{desc}。{pr}',
                           og_image=p['photo'] or HERO_IMG))


# ---------------------------------------------------------------- activities
def build_activities():
    path = 'activities/'
    r = rel(1)
    jump = ''.join(f'<a href="#{ev["id"]}">{e(ACT.CHIPS.get(ev["id"], ev["title"]))}</a>' for ev in ACT.EVENTS)
    sections = []
    for ev in ACT.EVENTS:
        cards = ''.join(activity_card(r, ev, p, f'https://www.instagram.com/p/{p[0]}/', external=True) for p in ev['posts'])
        sections.append(f'''<section class="event" id="{ev['id']}">
  <header class="event__head reveal">
    <div><div class="event__meta"><span>{e(ev['when'])}</span><span>{e(ev['place'])}</span></div><h2>{e(ev['title'])}</h2></div>
    <p class="event__lead">{e(ev['lead'])}</p>
  </header>
  <div class="cards">{cards}</div>
</section>''')
    body = page_hero(r, 'ACTIVITIES', '最近の活動',
                     'G20YEA Japan Councilの最近の活動をご紹介します。ウィーン、トロント、コロンボでの国際会議や、東京での交流会の様子を、公式Instagramの投稿からまとめました。',
                     [(None, '最近の活動')]) + f'''
<section class="section">
  <div class="wrap">
    <div class="section-head" style="margin-bottom:28px">
      <nav class="jump" aria-label="活動一覧" style="margin:0">{jump}</nav>
      <a class="btn btn--red btn--sm ig-follow" href="{ACT.IG}" target="_blank" rel="noopener">{ICON['ig']} @g20yea_japan_council をフォロー</a>
    </div>
    {''.join(sections)}
    <p style="font-size:13px;color:var(--sub)">写真・文章は <a href="{ACT.IG}" target="_blank" rel="noopener">公式Instagram（@g20yea_japan_council）</a> の投稿をもとにしています。最新の投稿はInstagramでご覧ください。</p>
  </div>
</section>
{cta(r)}'''
    write(path, layout(path, '最近の活動', body, active=path,
                       desc='G20YEA Japan Councilの最近の活動。ウィーンサミット、トロント・コロンボのLeadership Assembly、Fortune Generationとの東京交流会などを写真でご紹介します。',
                       og_image=UP + 'instagram/' + ACT.EVENTS[0]['posts'][0][0] + '.jpg'))


# ---------------------------------------------------------------- ask
def build_ask():
    path = 'ask/'
    r = rel(1)
    form = 'https://docs.google.com/forms/d/e/1FAIpQLSduYWVVtLr6vi4h3XRPgATGyQkvHZyRnT0KNNGT8fVew3Jq6A/viewform?embedded=true'
    body = page_hero(r, 'CONTACT', '入会の申し込み・お問い合わせ',
                     'G20YEA Japan Councilに入会をご希望の方は下記フォームからご登録ください。', [(None, '入会の申し込み・お問い合わせ')]) + f'''
<section class="section section--mist">
  <div class="wrap contact">
    <div class="form-card">
      <div class="form-card__head"><i></i>入会申し込みフォーム</div>
      <iframe src="{form}" title="G20YEA Japan Council 入会申し込みフォーム" loading="lazy">読み込んでいます…</iframe>
    </div>
    <aside class="info-card">
      <p class="eyebrow">CONTACT</p>
      <h2>お問い合わせ</h2>
      <p>お問い合わせは{MAIL}までメールください。</p>
      <a class="mail" href="mailto:{MAIL}">{ICON['mail']}{MAIL}</a>
      <p style="margin:24px 0 0;font-size:13px">フォームが表示されない場合は <a href="{form.replace('?embedded=true', '')}" target="_blank" rel="noopener" style="color:#fff">こちら</a> から直接開けます。</p>
    </aside>
  </div>
</section>'''
    write(path, layout(path, '入会の申し込み・お問い合わせ', body, active='ask/',
                       desc='G20YEA Japan Councilへの入会申し込み・お問い合わせ。'))


# ---------------------------------------------------------------- simple pages
def build_placeholder(path, en, title):
    r = rel(path.count('/'))
    body = page_hero(r, en, title, '', [(None, title)]) + f'''
<section class="section"><div class="wrap"><div class="empty"><b>COMING SOON</b>このページは準備中です。<div style="margin-top:28px"><a class="btn btn--line" href="{href(r, '')}">トップへ戻る</a></div></div></div></section>'''
    write(path, layout(path, title, body))


def build_hello():
    path = 'hello-world/'
    r = rel(1)
    body = page_hero(r, 'NEWS', HELLO['title'], '', [('最新情報/', '最新情報'), (None, HELLO['title'])]) + f'''
<section class="section"><div class="wrap prose"><p style="color:var(--sub);font-size:13px">{fmt_date(HELLO['date'])}</p><p>{e(HELLO['text'])}</p></div></section>'''
    write(path, layout(path, HELLO['title'], body))


def archive(path, title, en, posts):
    r = rel(path.count('/'))
    items = []
    for p in posts:
        sub = plain(field(p, '会社名')) if p.get('fields') else ''
        items.append(f'''<li><a href="{href(r, p['slug'] + '/')}"><time datetime="{p['date']}">{p['date'].replace('-', '.')}</time><div><h2>{e(p['title'])}</h2>{f'<p>{e(sub)}</p>' if sub else ''}</div>{ICON['arrow']}</a></li>''')
    inner = f'<ul class="list">{"".join(items)}</ul>' if items else '<div class="empty">記事はありません。</div>'
    body = page_hero(r, en, title, '', [(None, title)]) + f'<section class="section"><div class="wrap">{inner}</div></section>'
    write(path, layout(path, title, body))


def redirect(path, to):
    r = rel(path.count('/'))
    target = href(r, to)
    out = os.path.join(DOCS, path, 'index.html')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(
        f'<!doctype html><meta charset="utf-8"><title>{SITE}</title><link rel="canonical" href="{ORIGIN}{to}">'
        f'<meta http-equiv="refresh" content="0; url={target}"><a href="{target}">移動しました</a>\n')
    WRITTEN.append(path)


def build_archives():
    allp = POSTS + [HELLO]
    archive('最新情報/', '最新情報', 'NEWS', allp)
    archive('category/members-info/', 'メンバー紹介', 'CATEGORY', POSTS)
    archive('category/uncategorized/', '未分類', 'CATEGORY', [HELLO])
    archive('2025/10/', '2025年10月', 'ARCHIVE', [p for p in POSTS if p['date'].startswith('2025-10')])
    archive('2025/06/', '2025年6月', 'ARCHIVE', [HELLO])
    redirect('最新情報/page/2/', '最新情報/')
    redirect('2025/10/page/2/', '2025/10/')
    redirect('category/members-info/page/2/', 'category/members-info/')


if __name__ == '__main__':
    build_top()
    build_members()
    build_staff()
    build_profiles()
    build_activities()
    build_ask()
    build_placeholder('org/', 'ORGANIZATION', '組織')
    build_placeholder('org-2/', 'ORGANIZATION', 'G20YEA Japan Councilの組織')
    build_placeholder('summit2025/', 'SUMMIT', 'G20YEA Summit 2025')
    build_hello()
    build_archives()
    print(len(WRITTEN), 'pages written')
