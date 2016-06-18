JP = 0
EN = 1
STATUS = -1
TRANSLATED = 1
INPROGRESS = 2

CHAPTERS = {
    1: ["戦乙女の目覚め", "The Awakening of the Battle Maiden", INPROGRESS],
    2: ["魂の律動：剣を振る理由", "Spiritual Concentration: What to Wield the Sword For"],
    3: ["魂の律動：禁じられた歌声", "Spiritual Concentration: Forbidden Voice"],
    4: ["運命の女神", "The Goddess of Destiny"],
    5: ["魂の律動：見果てぬ夢は海を越えて", "Spiritual Concentration: An Unfulfilled Dream Crosses the Sea"],
    6: ["魂の律動：約束", "Spiritual Concentration: Promise"],
    7: ["魂の律動：還るべき場所", "Spiritual Concentration: A Place to Come Home to"],
    # I deliberately remove 先 as it just refers to where the light is guiding (the moon light is guiding Altveer out of the cell)
    8: ["魂の律動：光の導く先へ", "Spiritual Concentration: Guiding Light"],
    9: ["魂の律動：痛みのワケ", "Spiritual Concentration: <i>Why</i> Pain?"],
    10:["魂の律動：命の在処、心の在処", "Spiritual Concentration: The Whereabouts of Life and the Mind"],
    11:["魂の律動：無敵の剣", "Spiritual Concentration: The Invincible Sword"],
    12:["父と子と", "Father and Son"],
    13:["魂の律動：目標を外さなかった男", "Spiritual Concentration: The Man Who Never Missed the Mark"],
    14:["魂の律動：鎧が守りしもの", "He That the Armor Shields"],
    15:["魂の律動：愛はさだめ", "Love is Karma"],
    16:["魂の律動：赦されぬ罪", "Unpardonable Sin"],
    # 誰が為に is an archaic word meaning "For whom". The literal translation of this title is "For whom is the king's might".
    17:["魂の律動：王の力は誰が為に", "Worthy of the King's Might"],
    # I think that "Karmic Repayment" may be a good translation as well. However, it does not fit well with the story, as Altveer never atone for anything (and no one atoned in that story). Altveer was not a sinner to begin with.
    # I think that "巡りて" hints at the circulation of karma, especially to the fact that Altveer and Anelian are united by fate.
    18:["魂の律動：因果は巡りて", "All Is Fated"],
    19:["迷妄の地", "The Land of Illusion"],
    20:["トラキシア戦記", "Traxian Chronicles"],
    21:["轟く雷", "Roaring Thunder"],
    22:["シャイロ二世の誕生", "The Birth of Shiloh II"],
    23:["魂の律動：狂った歯車", "Spiritual Concentration: Machine Running Amok"]
}

EINHERJAR = "EINHERJAR"
STORIES = "STORIES"
SIDE_STORY_CHAPTERS = [
    {EINHERJAR: "那智", STORIES: [
        ["神託の少女", ""],
        ["神様の救い", ""]
    ]},
    {EINHERJAR: "リウ", STORIES: [
        ["忘却の竜", ""],
        ["盗まれた運命", ""]
    ]},
    {EINHERJAR: "ノルン", STORIES: [
        ["運命の歯車", "The Cogs of Destiny"],
        ["運命の子", "The Fated Girl"]
    ]},
    {EINHERJAR: "ルチア", STORIES: [
        ["母の遺した旋律", ""],
        ["ルチアの決意", ""]
    ]},
    {EINHERJAR: "ヴァルヴァロア", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "ランヴァルド", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "クラウシュ", STORIES: [
        ["魔の海域", ""],
        ["", ""]
    ]},
    {EINHERJAR: "クロエ", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "ダリネ", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "アネリアン", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "ジャンヌ", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "イングリット", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "クルト", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "セナ", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "カラドック", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "マクシミリアン", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "カチナ", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "マルヴァイナ", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "アルトフェイル", STORIES: [
        ["", ""],
        ["", ""]
    ]},
    {EINHERJAR: "フリー", STORIES: [
        ["試練の道・初級", ""],
        ["試練の道・中級", ""],
        ["試練の道・上級", ""]
    ]}
]

OTHER_STORIES = {
    1: ["戦乙女再臨！　彼方よりの来訪者", "The Second Advent of the Battle Maiden! A Visitor from Beyond", TRANSLATED],
    2: ["魂の律動：偽るモノ、偽らざるモノ", "Spiritual Concentration: Lies and Truths"],
    3: ["魂の律動：答えなき祈り", "Spiritual Concentration: Unanswered Prayers"]
}

CHARACTERS = {
    "？？？": "???",
    "オーディン": "Odin",
    "レナス": "Lenneth",
    "ゼフィロス": "Zephyros",
    "ヴァン神族": "Vanir",
    "フギン": "Huginn",
    "ムニン": "Muninn",
    "ジャンヌ": "Jeanne",
    # Choose raven over crow because that's how Huginn and Muginn are called in Scandinavian literature.
    "カラス１": "Raven 1",
    "カラス２": "Raven 2",
    # Senna
    "セナ": "Senna",
    "カラドック": "Caradoc",
    "店主": "Shopkeeper",
    "常連客": "Regular customer",
    "ガラの悪い客１": "Ill-bred customer 1",
    "ガラの悪い客２": "Ill-bred customer 2"
}
CHARACTERS.update({
    "那智": "Nachi",
    # Liu sounds Chinese. It could be Riu, I do not really see any difference.
    "リウ": "Liu",
    "ノルン": "Norn",
    # Most likely an Italian name
    "ルチア": "Lucia",
    # Most likely a gratuitous French name. Choose this spelling to look like the House of Valois.
    "ヴァルヴァロア": "Valvalois",
    # Ragnvald is an old norse first name: https://en.wikipedia.org/wiki/Rognvald
    "ランヴァルド": "Ragnvald",
    # The Japanese says Kuraushu. However, I was unable to find anything good to write it in Roman characters. So let's go with the German "Klaus"
    "クラウシュ": "Klaus",
    # A French name?
    "クロエ": "Chloé",
    "ダリネ": "Darine",
    # I chose the R because Anerian sounds more like as a name (at least as a surname, it does exist)
    "アネリアン": "Anerian",
    "イングリット": "Ingrid",
    "クルト": "Kurt",
    "マクシミリアン": "Maximilien",
    # I hesitate between ch and ts. Katsina sounds more exotic. Hopi Spirits are called Kachina or Katsina (two spellings exist) while lots of place in the world are called Katsina.
    "カチナ": "Katsina",
    "マルヴァイナ": "Malvina",
    # Another (gratuitous?) German-like name. I cannot find anything from which it is likely to originate. Altveer is a very rare surname that sounds a like (probably of Dutch origin, see Alteveer, though v is pronounced v, and not f, in Dutch).
    "アルトフェイル": "Altveer",
    "フリー": "Free"
})
