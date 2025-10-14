#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""Constants and configuration for the counting bot."""

import math

# Mathematical constants
MATH_CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'phi': (1 + math.sqrt(5)) / 2,
    'tau': 2 * math.pi,
    'euler': math.e,
    'golden': (1 + math.sqrt(5)) / 2
}

# Achievement emoji mappings
ACHIEVEMENT_EMOJIS = {
    'en': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
    'nl': '🇳🇱',
    'fr': '🇫🇷',
    'de': '🇩🇪',
    'se': '🇸🇪',
    'tr': '🇹🇷',
    'dk': '🇩🇰',
    'cy': '🏴󠁧󠁢󠁷󠁬󠁳󠁿',
    'no': '🇳🇴',
    'math': '🧮',
    'factorial': '❗',
    'constants': '🔬',
    'sqrt': '🌿',
    'random': '🎲',
    'decimal': '📐',
    'polyglot': '🗣️',
    'text': '🔤',
}

# Language flags
LANGUAGE_FLAGS = {
    'nl': '🇳🇱',
    'fr': '🇫🇷',
    'de': '🇩🇪',
    'se': '🇸🇪',
    'en': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
    'tr': '🇹🇷',
    'dk': '🇩🇰',
    'cy': '🏴󠁧󠁢󠁷󠁬󠁳󠁿',
    'no': '🇳🇴',
}

# Multilingual number mappings - now returns tuple of (value, set of languages)
MULTILANG_NUMBERS = {
    # Dutch
    'nul': (0, {'nl'}), 'een': (1, {'nl'}), 'twee': (2, {'nl'}), 'drie': (3, {'nl'}), 'vier': (4, {'nl', 'de'}), 'vijf': (5, {'nl'}),
    'zes': (6, {'nl'}), 'zeven': (7, {'nl'}), 'acht': (8, {'nl', 'de'}), 'negen': (9, {'nl'}), 'tien': (10, {'nl'}),
    'elf': (11, {'nl', 'de'}), 'twaalf': (12, {'nl', 'de'}), 'dertien': (13, {'nl'}), 'veertien': (14, {'nl'}), 'vijftien': (15, {'nl'}),
    'zestien': (16, {'nl'}), 'zeventien': (17, {'nl'}), 'achttien': (18, {'nl'}), 'negentien': (19, {'nl'}), 'twintig': (20, {'nl'}),
    'eenentwintig': (21, {'nl'}), 'tweeëntwintig': (22, {'nl'}), 'drieëntwintig': (23, {'nl'}), 'vierentwintig': (24, {'nl'}),
    'vijfentwintig': (25, {'nl'}), 'zesentwintig': (26, {'nl'}), 'zevenentwintig': (27, {'nl'}), 'achtentwintig': (28, {'nl'}),
    'negenentwintig': (29, {'nl'}), 'dertig': (30, {'nl'}), 'veertig': (40, {'nl', 'de'}), 'vijftig': (50, {'nl'}),
    'zestig': (60, {'nl', 'de'}), 'zeventig': (70, {'nl', 'de'}), 'tachtig': (80, {'nl', 'de'}), 'negentig': (90, {'nl', 'de'}), 'honderd': (100, {'nl'}),
    
    # French
    'zéro': (0, {'fr'}), 'zero': (0, {'fr'}), 'un': (1, {'fr', 'cy'}), 'une': (1, {'fr'}), 'deux': (2, {'fr'}), 'trois': (3, {'fr'}), 
    'quatre': (4, {'fr'}), 'cinq': (5, {'fr'}), 'six': (6, {'fr'}), 'sept': (7, {'fr'}), 'huit': (8, {'fr'}), 'neuf': (9, {'fr'}), 
    'dix': (10, {'fr'}), 'onze': (11, {'fr'}), 'douze': (12, {'fr'}), 'treize': (13, {'fr'}), 'quatorze': (14, {'fr'}), 
    'quinze': (15, {'fr'}), 'seize': (16, {'fr'}), 'dix-sept': (17, {'fr'}), 'dix-huit': (18, {'fr'}), 'dix-neuf': (19, {'fr'}), 
    'vingt': (20, {'fr'}), 'vingt-et-un': (21, {'fr'}), 'vingt-deux': (22, {'fr'}), 'vingt-trois': (23, {'fr'}), 
    'vingt-quatre': (24, {'fr'}), 'vingt-cinq': (25, {'fr'}), 'vingt-six': (26, {'fr'}), 'vingt-sept': (27, {'fr'}), 
    'vingt-huit': (28, {'fr'}), 'vingt-neuf': (29, {'fr'}), 'trente': (30, {'fr'}), 'quarante': (40, {'fr'}), 
    'cinquante': (50, {'fr'}), 'soixante': (60, {'fr'}), 'soixante-dix': (70, {'fr'}), 'quatre-vingt': (80, {'fr'}), 
    'quatre-vingt-dix': (90, {'fr'}), 'quatre-vingts': (80, {'fr'}), 'cent': (100, {'fr', 'cy'}),
    
    # German
    'null': (0, {'de', 'no'}), 'eins': (1, {'de'}), 'zwei': (2, {'de'}), 'drei': (3, {'de', 'nl'}), 
    'fünf': (5, {'de'}), 'fuenf': (5, {'de'}), 'funf': (5, {'de'}), 
    'sechs': (6, {'de'}), 'sieben': (7, {'de'}), 'neun': (9, {'de'}), 
    'zehn': (10, {'de'}), 'zwölf': (12, {'de'}), 'zwoelf': (12, {'de'}), 'dreizehn': (13, {'de'}), 'vierzehn': (14, {'de'}), 
    'fünfzehn': (15, {'de'}), 'fuenfzehn': (15, {'de'}), 'sechzehn': (16, {'de'}), 'siebzehn': (17, {'de'}), 
    'achtzehn': (18, {'de'}), 'neunzehn': (19, {'de'}), 'zwanzig': (20, {'de'}), 'einundzwanzig': (21, {'de'}), 
    'zweiundzwanzig': (22, {'de'}), 'dreiundzwanzig': (23, {'de'}), 'vierundzwanzig': (24, {'de'}),
    'fünfundzwanzig': (25, {'de'}), 'fuenfundzwanzig': (25, {'de'}), 'sechsundzwanzig': (26, {'de'}), 
    'siebenundzwanzig': (27, {'de'}), 'achtundzwanzig': (28, {'de'}), 'neunundzwanzig': (29, {'de'}), 'dreißig': (30, {'de'}), 
    'dreissig': (30, {'de'}), 
    'fünfzig': (50, {'de'}), 'fuenfzig': (50, {'de'}), 
    'siebzig': (70, {'de'}), 'achtzig': (80, {'de'}), 'neunzig': (90, {'de'}), 'hundert': (100, {'de'}), 'einhundert': (100, {'de'}),
    
    # Swedish
    'noll': (0, {'se'}), 'ett': (1, {'se', 'no'}), 'två': (2, {'se'}), 'tva': (2, {'se'}), 'tre': (3, {'se', 'dk', 'no'}), 'fyra': (4, {'se'}), 
    'fem': (5, {'se', 'dk', 'no'}), 'sex': (6, {'se'}), 'sju': (7, {'se', 'no'}), 'åtta': (8, {'se'}), 'atta': (8, {'se'}), 'nio': (9, {'se', 'no'}), 
    'tio': (10, {'se'}), 'elva': (11, {'se'}), 'tolv': (12, {'se', 'dk', 'no'}), 'tretton': (13, {'se', 'dk', 'no'}), 'fjorton': (14, {'se', 'no'}), 
    'femton': (15, {'se', 'no'}), 'sexton': (16, {'se'}), 'sjutton': (17, {'se'}), 'arton': (18, {'se', 'no'}), 'nitton': (19, {'se'}), 
    'tjugo': (20, {'se'}), 'tjugoett': (21, {'se'}), 'tjugotvå': (22, {'se'}), 'tjugotva': (22, {'se'}), 'tjugotre': (23, {'se'}),
    'tjugofyra': (24, {'se'}), 'tjugofem': (25, {'se'}), 'tjugosex': (26, {'se'}), 'tjugosju': (27, {'se'}), 'tjugoåtta': (28, {'se'}),
    'tjugoatta': (28, {'se'}), 'tjugonio': (29, {'se'}), 'trettio': (30, {'se', 'no'}), 'fyrtio': (40, {'se'}), 'femtio': (50, {'se', 'no'}),
    'sextio': (60, {'se', 'no'}), 'sjuttio': (70, {'se'}), 'åttio': (80, {'se'}), 'attio': (80, {'se'}), 'nittio': (90, {'se', 'no'}), 
    'hundra': (100, {'se'}), 'etthundra': (100, {'se'}),
    
    # Turkish
    'sıfır': (0, {'tr'}), 'sifir': (0, {'tr'}), 'bir': (1, {'tr'}), 'iki': (2, {'tr'}), 'üç': (3, {'tr'}), 'uc': (3, {'tr'}),
    'dört': (4, {'tr'}), 'dort': (4, {'tr'}), 'beş': (5, {'tr'}), 'bes': (5, {'tr'}), 'altı': (6, {'tr'}), 'alti': (6, {'tr'}),
    'yedi': (7, {'tr'}), 'sekiz': (8, {'tr'}), 'dokuz': (9, {'tr'}), 'on': (10, {'tr'}), 'on bir': (11, {'tr'}),
    'on iki': (12, {'tr'}), 'on üç': (13, {'tr'}), 'on uc': (13, {'tr'}), 'on dört': (14, {'tr'}), 'on dort': (14, {'tr'}),
    'on beş': (15, {'tr'}), 'on bes': (15, {'tr'}), 'on altı': (16, {'tr'}), 'on alti': (16, {'tr'}),
    'on yedi': (17, {'tr'}), 'on sekiz': (18, {'tr'}), 'on dokuz': (19, {'tr'}), 'yirmi': (20, {'tr'}),
    'yirmi bir': (21, {'tr'}), 'yirmi iki': (22, {'tr'}), 'yirmi üç': (23, {'tr'}), 'yirmi uc': (23, {'tr'}),
    'yirmi dört': (24, {'tr'}), 'yirmi dort': (24, {'tr'}), 'yirmi beş': (25, {'tr'}), 'yirmi bes': (25, {'tr'}),
    'yirmi altı': (26, {'tr'}), 'yirmi alti': (26, {'tr'}), 'yirmi yedi': (27, {'tr'}), 'yirmi sekiz': (28, {'tr'}),
    'yirmi dokuz': (29, {'tr'}), 'otuz': (30, {'tr'}), 'kırk': (40, {'tr'}), 'kirk': (40, {'tr'}),
    'elli': (50, {'tr'}), 'altmış': (60, {'tr'}), 'altmis': (60, {'tr'}), 'yetmiş': (70, {'tr'}), 'yetmis': (70, {'tr'}),
    'seksen': (80, {'tr'}), 'doksan': (90, {'tr'}), 'yüz': (100, {'tr'}), 'yuz': (100, {'tr'}),
    
    # Danish (shared words already defined above, only Danish-specific words here)
    'nul': (0, {'dk'}), 'en': (1, {'dk', 'no'}), 'et': (1, {'dk'}), 'to': (2, {'dk', 'no'}), 'fire': (4, {'dk', 'no'}),
    'seks': (6, {'dk', 'no'}), 'syv': (7, {'dk', 'no'}), 'otte': (8, {'dk'}), 'ni': (9, {'dk', 'no'}), 'ti': (10, {'dk', 'no'}),
    'elleve': (11, {'dk', 'no'}), 'tretten': (13, {'dk', 'no'}), 'fjorten': (14, {'dk', 'no'}), 'femten': (15, {'dk'}),
    'seksten': (16, {'dk', 'no'}), 'sytten': (17, {'dk', 'no'}), 'søtten': (17, {'no'}), 'atten': (18, {'dk', 'no'}), 'nitten': (19, {'dk', 'no'}), 'tyve': (20, {'dk', 'no'}),
    'enogtyve': (21, {'dk'}), 'toogtyve': (22, {'dk'}), 'treogtyve': (23, {'dk'}), 'fireogtyve': (24, {'dk'}),
    'femogtyve': (25, {'dk'}), 'seksogtyve': (26, {'dk'}), 'syvogtyve': (27, {'dk'}), 'otteogtyve': (28, {'dk'}),
    'niogtyve': (29, {'dk'}), 'tredive': (30, {'dk'}), 'fyrre': (40, {'dk'}), 'fyrretyve': (40, {'dk'}),
    'halvtreds': (50, {'dk'}), 'tres': (60, {'dk'}), 'halvfjerds': (70, {'dk'}), 'firs': (80, {'dk'}),
    'halvfems': (90, {'dk'}), 'hundrede': (100, {'dk'}),
    
    # Welsh
    'dim': (0, {'cy'}), 'sero': (0, {'cy'}), 'dau': (2, {'cy'}), 'dwy': (2, {'cy'}),
    'tri': (3, {'cy'}), 'tair': (3, {'cy'}), 'pedwar': (4, {'cy'}), 'pedair': (4, {'cy'}),
    'pump': (5, {'cy'}), 'pum': (5, {'cy'}), 'chwech': (6, {'cy'}), 'chwe': (6, {'cy'}),
    'saith': (7, {'cy'}), 'wyth': (8, {'cy'}), 'naw': (9, {'cy'}), 'deg': (10, {'cy'}), 'deng': (10, {'cy'}),
    'un ar ddeg': (11, {'cy'}), 'deuddeg': (12, {'cy'}), 'tri ar ddeg': (13, {'cy'}), 'pedwar ar ddeg': (14, {'cy'}),
    'pymtheg': (15, {'cy'}), 'un ar bymtheg': (16, {'cy'}), 'dau ar bymtheg': (17, {'cy'}), 'deunaw': (18, {'cy'}),
    'pedwar ar bymtheg': (19, {'cy'}), 'ugain': (20, {'cy'}), 'un ar hugain': (21, {'cy'}), 'dau ar hugain': (22, {'cy'}),
    'tri ar hugain': (23, {'cy'}), 'pedwar ar hugain': (24, {'cy'}), 'pump ar hugain': (25, {'cy'}),
    'deg ar hugain': (30, {'cy'}), 'deugain': (40, {'cy'}), 'hanner cant': (50, {'cy'}), 'trigain': (60, {'cy'}),
    'deg a thrigain': (70, {'cy'}), 'pedwar ugain': (80, {'cy'}), 'deg a phedwar ugain': (90, {'cy'}),
    'cant': (100, {'cy'}),
    
    # Norwegian (only Norwegian-specific words, shared words already defined above)
    'tjueen': (21, {'no'}), 'tjueto': (22, {'no'}), 'tjuetre': (23, {'no'}), 'tjuefire': (24, {'no'}), 'tjuefem': (25, {'no'}),
    'tjueseks': (26, {'no'}), 'tjuesyv': (27, {'no'}), 'tjueåtte': (28, {'no'}), 'tjueatte': (28, {'no'}),
    'tjueni': (29, {'no'}), 'tredve': (30, {'no'}), 'førti': (40, {'no'}), 'forti': (40, {'no'}),
    'seksti': (60, {'no'}), 'søtti': (70, {'no'}), 'sytti': (70, {'no'}),
    'åtti': (80, {'no'}), 'atti': (80, {'no'}), 'nitti': (90, {'no'}), 'hundre': (100, {'no'}), 'tjue': (20, {'no'}),
}

# Mistake puns organized by severity
MISTAKE_PUNS = {
    'gentle': [
        "Oops! Looks like someone needs to *count* on their fingers! 🖐️",
        "That's not quite right! Don't worry, we all have our *calculated* risks! 📊",
        "Close, but no cigar! Math can be *sum-times* tricky! 🤔",
        "Not quite! But hey, at least you're *trying* to add up! ➕",
        "Whoops! That answer doesn't quite *multiply* the fun! ✖️",
    ],
    'medium': [
        "Another wrong answer? You're really *dividing* the room here! 🤨",
        "Yikes! Your math skills are looking a bit *irrational* today! 📉",
        "Wrong again! Maybe it's time to *subtract* some confidence? 😬",
        "Oh dear! Your counting is more off than a *broken calculator*! 🧮💥",
        "That's incorrect! Are you using *imaginary numbers*? Because this isn't working! 🌪️",
    ],
    'harsh': [
        "SERIOUSLY?! Even a *random number generator* would do better! 🎲💸",
        "Wrong AGAIN! At this point, a *monkey with a calculator* has better odds! 🐵🧮",
        "Are you even TRYING?! Your math skills are more *negative* than your success rate! ➖😤",
        "This is painful to watch! You're making *division by zero* look reasonable! 💥🤯",
        "OH COME ON! You're so bad at this, you make *infinity minus infinity* look logical! ♾️💀",
    ],
    'brutal': [
        "I can't even... Your counting is SO BAD that mathematicians are *crying*! 😭📚",
        "This is EMBARRASSING! You've made numbers afraid of being counted! 🔢😱",
        "STOP! You're hurting my circuits! Even *ERROR 404* is more accurate than you! 🤖💥",
        "I'm calling the MATH POLICE! This level of wrongness should be *ILLEGAL*! 🚔📊",
        "You know what? I'm going to pretend I didn't see that. For the sake of *mathematics everywhere*! 🙈🧮",
    ]
}

# Streak messages
STREAK_MESSAGES = [
    "🔥 ON FIRE! {} correct in a row! You're absolutely crushing it! 🎯",
    "⚡ UNSTOPPABLE! {} straight correct answers! You're a counting MACHINE! 🤖✨",
    "🌟 INCREDIBLE! {} in a row! Your math skills are OUT OF THIS WORLD! 🚀",
    "💎 LEGENDARY! {} perfect answers! You're the COUNT MASTER! 👑",
    "🎊 PHENOMENAL! {} consecutive wins! The numbers bow before your greatness! 🙌",
    "🦄 MYTHICAL! {} straight victories! You've achieved COUNTING NIRVANA! ✨",
    "🌈 MAGICAL! {} in a row! You're making mathematics look like child's play! 🎪",
    "🏆 CHAMPION! {} correct streak! You're the ULTIMATE COUNTING LEGEND! 👑✨",
]