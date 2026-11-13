#!/usr/bin/env python3
"""docs/org-2 をテンプレートに docs/activities/index.html を生成する。
使い方: python3 build_activities.py <repo の docs ディレクトリ>"""
import os, sys, html

docs = sys.argv[1]
tpl = open(os.path.join(docs, 'org-2/index.html'), encoding='utf-8').read()

IG = 'https://www.instagram.com/g20yea_japan_council/'
IMG = '../wp-content/uploads/instagram/'

# 新しい順。date は Instagram 投稿日。
EVENTS = [
    {
        'id': 'vienna',
        'title': 'G20YEA Vienna Summit 2026',
        'place': 'オーストリア・ウィーン',
        'when': '2026年9月15日〜19日',
        'lead': '世界各国の若手起業家が集う年次サミット。MOU署名式、Leadership Assembly、B2Bマッチングなどが行われました。',
        'posts': [
            ('Dec-qO2h1VO', '2026-10-13', 'ウィーンから日本、そしてその先へ',
             'サミットを経て、2027年は日本でのLeadership Assembly開催が検討されています。ブラジルでのLeadership Assembly、英国でのG20YEA Summitに向けた準備も進行中です。',
             '「What\'s Next?」ウィーンサミットの壇上。2027年の日本・ブラジル・英国の開催予定を告知する画像'),
            ('DebD3ksgXsp', '2026-10-13', 'MOU署名式とLeadership Assembly',
             '各国代表によるMOU署名式を実施。Leadership Assemblyでは、G20公式エンゲージメントグループ化を目指す取り組みや、今後のサミットの質の向上、中長期戦略を議論しました。',
             'ウィーンサミットでのMOU署名とLeadership Assemblyの様子'),
            ('DeZCquBBTl7', '2026-10-12', 'ウィーンサミット開催',
             '開会式、パネルディスカッション、B2Bマッチング、ピッチコンペ、ガラディナーなど多彩なプログラム。B2Bマッチングでは新たに業種別マッチングが導入されました。',
             'G20YEA Vienna Summit 2026 のレポート画像'),
        ],
    },
    {
        'id': 'toronto',
        'title': 'G20YEA Leadership Assembly（トロント）',
        'place': 'カナダ・トロント／ナイアガラ',
        'when': '2026年7月20日〜',
        'lead': 'UNICEF「Generation Unlimited」との連携や、ウィーンサミット・2027年ロンドンサミットの準備を議論。最終日はナイアガラ地域のイノベーション拠点を視察しました。',
        'posts': [
            ('DbkYM7IgQpz', '2026-08-02', 'Day 3：ナイアガラのイノベーション・エコシステム',
             'Brock University、Innovate Niagara、Niagara Falls Innovation Hubなどを視察。大学・行政・支援機関が連携してスタートアップを育成する仕組みを学びました。',
             'Leadership Assembly Day 3 ナイアガラ視察のレポート画像'),
            ('DbfISg6BdZg', '2026-07-31', 'Day 2：G20YEAの今後に向けた議論',
             'UNICEF「Generation Unlimited」との連携、ウィーン・ロンドンのサミット準備、G20とのさらなる連携強化、組織運営やスポンサーシップについて意見交換しました。',
             'Leadership Assembly Day 2 のレポート画像'),
            ('DbNHA4qgbx0', '2026-07-24', 'Day 1：朝食会・大臣とのパネル・商工会議所交流',
             '2026年7月20日、Futurpreneurにて開幕。朝食ミーティング、大臣を迎えたパネルディスカッション、現地商工会議所とのネットワーキングを実施しました。',
             'Leadership Assembly Day 1 のレポート画像。会場の様子と集合写真'),
        ],
    },
    {
        'id': 'tokyo',
        'title': 'Fortune Generation × G20YEA Japan Council 交流会',
        'place': '日本・東京',
        'when': '2026年5月',
        'lead': '中国の次世代ファミリービジネス経営者ネットワーク「Fortune Generation」を日本に迎え、日中合わせて60名以上の次世代リーダーが交流しました。',
        'posts': [
            ('DYVxDwZgZzs', '2026-05-15', '寿司を囲んだネットワーキング',
             '交流会後半は、職人によるライブ寿司パフォーマンスとともに懇親。エネルギー、AI、医療、不動産、物流、製造業など多様な業種の経営者が語り合いました。',
             '交流会後半のネットワーキング、寿司パフォーマンスの様子'),
            ('DYVzTILASpd', '2026-05-14', 'Company Visit：三木森グループ',
             'Fortune GenerationのメンバーとともにMikimori Groupを訪問し、日本の新エネルギー事業や不動産分野について理解を深めました。',
             '三木森グループ訪問の集合写真'),
            ('DYTvl_ZAe6Z', '2026-05-14', 'ビジネス＆カルチャー交流会を開催',
             'テーマは「ファミリー企業をどう次世代へ繋ぐか」。基調講演では株式会社チエノワ代表取締役・田中雅也様に、日本の長寿企業に学ぶ長期経営の知恵をお話しいただきました。',
             'Fortune Generation との交流会の告知画像'),
        ],
    },
    {
        'id': 'colombo',
        'title': 'G20YEA Leadership Assembly（コロンボ）',
        'place': 'スリランカ・コロンボ',
        'when': '2026年2月5日〜6日',
        'lead': 'G20YEAの公式エンゲージメントグループ化を見据えたガバナンス強化、加盟国拡大、ウィーンサミットと2027年UKサミットの準備を議論しました。',
        'posts': [
            ('DVFSZeegcOO', '2026-02-22', 'Leadership Assembly 主な成果',
             '公式エンゲージメントグループ化を視野にしたガバナンス強化、アジアを含む加盟拡大、ウィーンサミット（9月）の準備、2027年UKサミットと次回トロント開催を確認しました。',
             'Leadership Assembly Key Outcomes のレポート画像'),
            ('DVDDHPeASpY', '2026-02-21', 'Day 2：ポートシティ視察とJETRO訪問',
             '中国の再エネ・ビジネスマッチングの発表、2027年UKサミットの計画を議論。ポートシティ・コロンボの視察と副大臣との対話、日本団としてJETROも訪問しました。',
             'Leadership Assembly Day 2 コロンボのレポート画像'),
            ('DVAmCCEgcO-', '2026-02-20', 'Day 1：アライアンスの基盤強化',
             '公式エンゲージメントグループ化の可能性、ガバナンスとFoundational MoUの見直し、加盟国拡大戦略（豪州・インドネシア・韓国・米国）などを協議しました。',
             'Leadership Assembly Day 1 コロンボのレポート画像'),
        ],
    },
]

def fmt(d):
    y, m, dd = d.split('-')
    return f'{y}年{int(m)}月{int(dd)}日'

def card(code, date, title, text, alt):
    url = f'https://www.instagram.com/p/{code}/'
    return f'''<article class="ga-card">
<a class="ga-card__img" href="{url}" target="_blank" rel="noopener"><img src="{IMG}{code}.jpg" alt="{html.escape(alt)}" width="512" height="640" loading="lazy"></a>
<div class="ga-card__body">
<time class="ga-card__date" datetime="{date}">{fmt(date)}</time>
<h4 class="ga-card__title">{html.escape(title)}</h4>
<p class="ga-card__text">{html.escape(text)}</p>
<a class="ga-card__link" href="{url}" target="_blank" rel="noopener"><i class="fa-brands fa-instagram"></i> Instagramで見る</a>
</div>
</article>'''

sections = []
for e in EVENTS:
    cards = '\n'.join(card(*p) for p in e['posts'])
    sections.append(f'''<section class="ga-event" id="{e['id']}">
<header class="ga-event__head">
<p class="ga-event__meta"><span>{e['when']}</span><span>{e['place']}</span></p>
<h3 class="ga-event__title">{html.escape(e['title'])}</h3>
<p class="ga-event__lead">{html.escape(e['lead'])}</p>
</header>
<div class="ga-grid">
{cards}
</div>
</section>''')

CHIPS = {'vienna': '9月 ウィーンサミット', 'toronto': '7月 トロント', 'tokyo': '5月 東京交流会', 'colombo': '2月 コロンボ'}
jump = ''.join(f'<a href="#{e["id"]}">{CHIPS[e["id"]]}</a>' for e in EVENTS)

CSS = '''<style id="ga-activities-css">
body.post-name-activities .main-section{width:100%;max-width:100%;flex:0 0 100%}
body.post-name-activities .sub-section{display:none}
.ga{--ga-accent:var(--vk-color-primary,#337ab7);--ga-line:#e3e8ee;--ga-sub:#5b6773}
.ga-intro{margin:0 0 1.5em;line-height:1.9}
.ga-follow{display:inline-flex;align-items:center;gap:.5em;padding:.6em 1.2em;border-radius:999px;background:var(--ga-accent);color:#fff!important;font-weight:700;text-decoration:none!important;font-size:.95rem}
.ga-follow:hover{opacity:.85}
.ga-jump{display:flex;flex-wrap:wrap;gap:.5em;margin:1.5em 0 2.5em;padding:0;list-style:none}
.ga-jump a{display:inline-block;padding:.35em .9em;border:1px solid var(--ga-line);border-radius:999px;font-size:.85rem;color:inherit;text-decoration:none}
.ga-jump a:hover{border-color:var(--ga-accent);color:var(--ga-accent)}
.ga-event{margin:0 0 3.5em;scroll-margin-top:80px}
.ga-event__head{border-left:4px solid var(--ga-accent);padding-left:1em;margin-bottom:1.5em}
.ga-event__meta{display:flex;flex-wrap:wrap;gap:.4em 1.2em;margin:0 0 .3em;font-size:.85rem;color:var(--ga-sub);font-weight:700}
.ga-event__title{margin:0 0 .4em;padding:0;border:0;background:none;font-size:1.35rem;line-height:1.4}
.ga-event__title::before,.ga-event__title::after{display:none}
.ga-event__lead{margin:0;line-height:1.8;font-size:.95rem}
.ga-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.5em}
.ga-card{display:flex;flex-direction:column;background:#fff;border:1px solid var(--ga-line);border-radius:10px;overflow:hidden}
.ga-card__img{display:block;aspect-ratio:4/5;overflow:hidden;background:#eef1f5}
.ga-card__img img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .3s}
.ga-card__img:hover img{transform:scale(1.03)}
.ga-card__body{display:flex;flex-direction:column;gap:.5em;padding:1em 1.1em 1.2em;flex:1}
.ga-card__date{font-size:.8rem;color:var(--ga-sub)}
.ga-card__title{margin:0;padding:0;border:0;background:none;font-size:1.02rem;line-height:1.5}
.ga-card__title::before,.ga-card__title::after{display:none}
.ga-card__text{margin:0;font-size:.88rem;line-height:1.75;color:#333}
.ga-card__link{margin-top:auto;padding-top:.4em;font-size:.85rem;font-weight:700;color:var(--ga-accent);text-decoration:none}
.ga-card__link:hover{text-decoration:underline}
.ga-note{margin-top:2em;font-size:.8rem;color:var(--ga-sub);line-height:1.7}
@media (max-width:900px){.ga-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.ga-grid{grid-template-columns:1fr}.ga-event__title{font-size:1.2rem}}
</style>'''

content = f'''<div class="entry-body">{CSS}
<div class="ga">
<p class="ga-intro">G20YEA Japan Councilの最近の活動をご紹介します。ウィーン、トロント、コロンボでの国際会議や、東京での交流会の様子を、公式Instagramの投稿からまとめました。</p>
<a class="ga-follow" href="{IG}" target="_blank" rel="noopener"><i class="fa-brands fa-instagram"></i> @g20yea_japan_council をフォロー</a>
<nav class="ga-jump" aria-label="活動一覧">{jump}</nav>
{chr(10).join(sections)}
<p class="ga-note">写真・文章は <a href="{IG}" target="_blank" rel="noopener">公式Instagram（@g20yea_japan_council）</a> の投稿をもとにしています。最新の投稿はInstagramでご覧ください。</p>
</div>
</div>'''

page = tpl
for a, b in [
    ('G20YEA Japan Councilの組織', '最近の活動'),
    ('https://g20yea.jp/org-2/', 'https://g20yea.jp/activities/'),
    ('post-name-org-2', 'post-name-activities'),
]:
    page = page.replace(a, b)

desc = 'G20YEA Japan Councilの最近の活動。ウィーンサミット、トロント・コロンボのLeadership Assembly、Fortune Generationとの東京交流会などを写真でご紹介します。'
page = page.replace('<meta name="description" content="" />', f'<meta name="description" content="{desc}" />')
page = page.replace('<meta property="og:description" content="" />', f'<meta property="og:description" content="{desc}" />')
page = page.replace('<meta name="twitter:description" content="">', f'<meta name="twitter:description" content="{desc}">')
page = page.replace('<meta property="og:type" content="article" />',
                    '<meta property="og:type" content="article" /><meta property="og:image" content="https://g20yea.jp/wp-content/uploads/instagram/Dec-qO2h1VO.jpg" />')

assert '<div class="entry-body"></div>' in page
page = page.replace('<div class="entry-body"></div>', content)

out = os.path.join(docs, 'activities')
os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
print('written', os.path.join(out, 'index.html'), len(page))
