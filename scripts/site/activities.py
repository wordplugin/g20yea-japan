"""「最近の活動」ページのデータ。新しい順に並べる。
写真は docs/wp-content/uploads/instagram/<投稿ID>.jpg に置く。
posts の各要素: (Instagram投稿ID, 投稿日, 見出し, 本文, 画像の代替テキスト)"""

IG = 'https://www.instagram.com/g20yea_japan_council/'

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

# ページ内ジャンプ用の短い見出し（EVENTS の id ごと）
CHIPS = {'vienna': '9月 ウィーンサミット', 'toronto': '7月 トロント', 'tokyo': '5月 東京交流会', 'colombo': '2月 コロンボ'}
