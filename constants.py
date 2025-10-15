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
    'ja': '🇯🇵',
    'la': '🏛️', 
    'math': '🧮',
    'factorial': '❗',
    'constants': '🔬',
    'sqrt': '🌿',
    'random': '🎲',
    'decimal': '📐',
    'polyglot': '🗣️',
    'text': '🔤',
    'multiple': '🔢',
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
    'ja': '🇯🇵',
    'la': '🏛️',
}

# Roman numeral mappings (must be UPPERCASE)
ROMAN_NUMERALS = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
    'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15, 'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20,
    'XXI': 21, 'XXII': 22, 'XXIII': 23, 'XXIV': 24, 'XXV': 25, 'XXVI': 26, 'XXVII': 27, 'XXVIII': 28, 'XXIX': 29, 'XXX': 30,
    'XXXI': 31, 'XXXII': 32, 'XXXIII': 33, 'XXXIV': 34, 'XXXV': 35, 'XXXVI': 36, 'XXXVII': 37, 'XXXVIII': 38, 'XXXIX': 39, 'XL': 40,
    'XLI': 41, 'XLII': 42, 'XLIII': 43, 'XLIV': 44, 'XLV': 45, 'XLVI': 46, 'XLVII': 47, 'XLVIII': 48, 'XLIX': 49, 'L': 50,
    'LI': 51, 'LII': 52, 'LIII': 53, 'LIV': 54, 'LV': 55, 'LVI': 56, 'LVII': 57, 'LVIII': 58, 'LIX': 59, 'LX': 60,
    'LXI': 61, 'LXII': 62, 'LXIII': 63, 'LXIV': 64, 'LXV': 65, 'LXVI': 66, 'LXVII': 67, 'LXVIII': 68, 'LXIX': 69, 'LXX': 70,
    'LXXI': 71, 'LXXII': 72, 'LXXIII': 73, 'LXXIV': 74, 'LXXV': 75, 'LXXVI': 76, 'LXXVII': 77, 'LXXVIII': 78, 'LXXIX': 79, 'LXXX': 80,
    'LXXXI': 81, 'LXXXII': 82, 'LXXXIII': 83, 'LXXXIV': 84, 'LXXXV': 85, 'LXXXVI': 86, 'LXXXVII': 87, 'LXXXVIII': 88, 'LXXXIX': 89, 'XC': 90,
    'XCI': 91, 'XCII': 92, 'XCIII': 93, 'XCIV': 94, 'XCV': 95, 'XCVI': 96, 'XCVII': 97, 'XCVIII': 98, 'XCIX': 99, 'C': 100,
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
    'enogtyve': (21, {'dk'}), 'toog': (22, {'dk'}), 'treogtyve': (23, {'dk'}), 'fireogtyve': (24, {'dk'}),
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
    
    # Japanese - Hiragana
    'ぜろ': (0, {'ja'}), 'れい': (0, {'ja'}), 'いち': (1, {'ja'}), 'に': (2, {'ja'}), 'さん': (3, {'ja'}),
    'よん': (4, {'ja'}), 'し': (4, {'ja'}), 'ご': (5, {'ja'}), 'ろく': (6, {'ja'}), 'なな': (7, {'ja'}), 
    'しち': (7, {'ja'}), 'はち': (8, {'ja'}), 'きゅう': (9, {'ja'}), 'く': (9, {'ja'}), 'じゅう': (10, {'ja'}),
    'じゅういち': (11, {'ja'}), 'じゅうに': (12, {'ja'}), 'じゅうさん': (13, {'ja'}), 'じゅうよん': (14, {'ja'}),
    'じゅうし': (14, {'ja'}), 'じゅうご': (15, {'ja'}), 'じゅうろく': (16, {'ja'}), 'じゅうなな': (17, {'ja'}),
    'じゅうしち': (17, {'ja'}), 'じゅうはち': (18, {'ja'}), 'じゅうきゅう': (19, {'ja'}), 'じゅうく': (19, {'ja'}),
    'にじゅう': (20, {'ja'}), 'にじゅういち': (21, {'ja'}), 'にじゅうに': (22, {'ja'}), 'にじゅうさん': (23, {'ja'}),
    'にじゅうよん': (24, {'ja'}), 'にじゅうし': (24, {'ja'}), 'にじゅうご': (25, {'ja'}), 'にじゅうろく': (26, {'ja'}),
    'にじゅうなな': (27, {'ja'}), 'にじゅうしち': (27, {'ja'}), 'にじゅうはち': (28, {'ja'}), 'にじゅうきゅう': (29, {'ja'}),
    'にじゅうく': (29, {'ja'}), 'さんじゅう': (30, {'ja'}), 'さんじゅういち': (31, {'ja'}), 'さんじゅうに': (32, {'ja'}),
    'さんじゅうさん': (33, {'ja'}), 'さんじゅうよん': (34, {'ja'}), 'さんじゅうご': (35, {'ja'}), 'さんじゅうろく': (36, {'ja'}),
    'さんじゅうなな': (37, {'ja'}), 'さんじゅうはち': (38, {'ja'}), 'さんじゅうきゅう': (39, {'ja'}), 'よんじゅう': (40, {'ja'}),
    'よんじゅういち': (41, {'ja'}), 'よんじゅうに': (42, {'ja'}), 'よんじゅうさん': (43, {'ja'}), 'よんじゅうよん': (44, {'ja'}),
    'よんじゅうご': (45, {'ja'}), 'よんじゅうろく': (46, {'ja'}), 'よんじゅうなな': (47, {'ja'}), 'よんじゅうはち': (48, {'ja'}),
    'よんじゅうきゅう': (49, {'ja'}), 'ごじゅう': (50, {'ja'}), 'ごじゅういち': (51, {'ja'}), 'ごじゅうに': (52, {'ja'}),
    'ごじゅうさん': (53, {'ja'}), 'ごじゅうよん': (54, {'ja'}), 'ごじゅうご': (55, {'ja'}), 'ごじゅうろく': (56, {'ja'}),
    'ごじゅうなな': (57, {'ja'}), 'ごじゅうはち': (58, {'ja'}), 'ごじゅうきゅう': (59, {'ja'}), 'ろくじゅう': (60, {'ja'}),
    'ろくじゅういち': (61, {'ja'}), 'ろくじゅうに': (62, {'ja'}), 'ろくじゅうさん': (63, {'ja'}), 'ろくじゅうよん': (64, {'ja'}),
    'ろくじゅうご': (65, {'ja'}), 'ろくじゅうろく': (66, {'ja'}), 'ろくじゅうなな': (67, {'ja'}), 'ろくじゅうはち': (68, {'ja'}),
    'ろくじゅうきゅう': (69, {'ja'}), 'ななじゅう': (70, {'ja'}), 'しちじゅう': (70, {'ja'}), 'ななじゅういち': (71, {'ja'}),
    'ななじゅうに': (72, {'ja'}), 'ななじゅうさん': (73, {'ja'}), 'ななじゅうよん': (74, {'ja'}), 'ななじゅうご': (75, {'ja'}),
    'ななじゅうろく': (76, {'ja'}), 'ななじゅうなな': (77, {'ja'}), 'ななじゅうはち': (78, {'ja'}), 'ななじゅうきゅう': (79, {'ja'}),
    'はちじゅう': (80, {'ja'}), 'はちじゅういち': (81, {'ja'}), 'はちじゅうに': (82, {'ja'}), 'はちじゅうさん': (83, {'ja'}),
    'はちじゅうよん': (84, {'ja'}), 'はちじゅうご': (85, {'ja'}), 'はちじゅうろく': (86, {'ja'}), 'はちじゅうなな': (87, {'ja'}),
    'はちじゅうはち': (88, {'ja'}), 'はちじゅうきゅう': (89, {'ja'}), 'きゅうじゅう': (90, {'ja'}), 'きゅうじゅういち': (91, {'ja'}),
    'きゅうじゅうに': (92, {'ja'}), 'きゅうじゅうさん': (93, {'ja'}), 'きゅうじゅうよん': (94, {'ja'}), 'きゅうじゅうご': (95, {'ja'}),
    'きゅうじゅうろく': (96, {'ja'}), 'きゅうじゅうなな': (97, {'ja'}), 'きゅうじゅうはち': (98, {'ja'}), 'きゅうじゅうきゅう': (99, {'ja'}),
    'ひゃく': (100, {'ja'}), 'いっぴゃく': (100, {'ja'}),
    
    # Japanese - Katakana
    'ゼロ': (0, {'ja'}), 'レイ': (0, {'ja'}), 'イチ': (1, {'ja'}), 'ニ': (2, {'ja'}), 'サン': (3, {'ja'}),
    'ヨン': (4, {'ja'}), 'シ': (4, {'ja'}), 'ゴ': (5, {'ja'}), 'ロク': (6, {'ja'}), 'ナナ': (7, {'ja'}),
    'シチ': (7, {'ja'}), 'ハチ': (8, {'ja'}), 'キュウ': (9, {'ja'}), 'ク': (9, {'ja'}), 'ジュウ': (10, {'ja'}),
    'ジュウイチ': (11, {'ja'}), 'ジュウニ': (12, {'ja'}), 'ジュウサン': (13, {'ja'}), 'ジュウヨン': (14, {'ja'}),
    'ジュウシ': (14, {'ja'}), 'ジュウゴ': (15, {'ja'}), 'ジュウロク': (16, {'ja'}), 'ジュウナナ': (17, {'ja'}),
    'ジュウシチ': (17, {'ja'}), 'ジュウハチ': (18, {'ja'}), 'ジュウキュウ': (19, {'ja'}), 'ジュウク': (19, {'ja'}),
    'ニジュウ': (20, {'ja'}), 'ニジュウイチ': (21, {'ja'}), 'ニジュウニ': (22, {'ja'}), 'ニジュウサン': (23, {'ja'}),
    'ニジュウヨン': (24, {'ja'}), 'ニジュウシ': (24, {'ja'}), 'ニジュウゴ': (25, {'ja'}), 'ニジュウロク': (26, {'ja'}),
    'ニジュウナナ': (27, {'ja'}), 'ニジュウシチ': (27, {'ja'}), 'ニジュウハチ': (28, {'ja'}), 'ニジュウキュウ': (29, {'ja'}),
    'ニジュウク': (29, {'ja'}), 'サンジュウ': (30, {'ja'}), 'ヨンジュウ': (40, {'ja'}), 'ゴジュウ': (50, {'ja'}),
    'ロクジュウ': (60, {'ja'}), 'ナナジュウ': (70, {'ja'}), 'シチジュウ': (70, {'ja'}), 'ハチジュウ': (80, {'ja'}),
    'キュウジュウ': (90, {'ja'}), 'ヒャク': (100, {'ja'}), 'イッピャク': (100, {'ja'}),
    
    # Japanese - Kanji
    '零': (0, {'ja'}), '一': (1, {'ja'}), '二': (2, {'ja'}), '三': (3, {'ja'}), '四': (4, {'ja'}),
    '五': (5, {'ja'}), '六': (6, {'ja'}), '七': (7, {'ja'}), '八': (8, {'ja'}), '九': (9, {'ja'}),
    '十': (10, {'ja'}), '十一': (11, {'ja'}), '十二': (12, {'ja'}), '十三': (13, {'ja'}), '十四': (14, {'ja'}),
    '十五': (15, {'ja'}), '十六': (16, {'ja'}), '十七': (17, {'ja'}), '十八': (18, {'ja'}), '十九': (19, {'ja'}),
    '二十': (20, {'ja'}), '二十一': (21, {'ja'}), '二十二': (22, {'ja'}), '二十三': (23, {'ja'}), '二十四': (24, {'ja'}),
    '二十五': (25, {'ja'}), '二十六': (26, {'ja'}), '二十七': (27, {'ja'}), '二十八': (28, {'ja'}), '二十九': (29, {'ja'}),
    '三十': (30, {'ja'}), '三十一': (31, {'ja'}), '三十二': (32, {'ja'}), '三十三': (33, {'ja'}), '三十四': (34, {'ja'}),
    '三十五': (35, {'ja'}), '三十六': (36, {'ja'}), '三十七': (37, {'ja'}), '三十八': (38, {'ja'}), '三十九': (39, {'ja'}),
    '四十': (40, {'ja'}), '四十一': (41, {'ja'}), '四十二': (42, {'ja'}), '四十三': (43, {'ja'}), '四十四': (44, {'ja'}),
    '四十五': (45, {'ja'}), '四十六': (46, {'ja'}), '四十七': (47, {'ja'}), '四十八': (48, {'ja'}), '四十九': (49, {'ja'}),
    '五十': (50, {'ja'}), '五十一': (51, {'ja'}), '五十二': (52, {'ja'}), '五十三': (53, {'ja'}), '五十四': (54, {'ja'}),
    '五十五': (55, {'ja'}), '五十六': (56, {'ja'}), '五十七': (57, {'ja'}), '五十八': (58, {'ja'}), '五十九': (59, {'ja'}),
    '六十': (60, {'ja'}), '六十一': (61, {'ja'}), '六十二': (62, {'ja'}), '六十三': (63, {'ja'}), '六十四': (64, {'ja'}),
    '六十五': (65, {'ja'}), '六十六': (66, {'ja'}), '六十七': (67, {'ja'}), '六十八': (68, {'ja'}), '六十九': (69, {'ja'}),
    '七十': (70, {'ja'}), '七十一': (71, {'ja'}), '七十二': (72, {'ja'}), '七十三': (73, {'ja'}), '七十四': (74, {'ja'}),
    '七十五': (75, {'ja'}), '七十六': (76, {'ja'}), '七十七': (77, {'ja'}), '七十八': (78, {'ja'}), '七十九': (79, {'ja'}),
    '八十': (80, {'ja'}), '八十一': (81, {'ja'}), '八十二': (82, {'ja'}), '八十三': (83, {'ja'}), '八十四': (84, {'ja'}),
    '八十五': (85, {'ja'}), '八十六': (86, {'ja'}), '八十七': (87, {'ja'}), '八十八': (88, {'ja'}), '八十九': (89, {'ja'}),
    '九十': (90, {'ja'}), '九十一': (91, {'ja'}), '九十二': (92, {'ja'}), '九十三': (93, {'ja'}), '九十四': (94, {'ja'}),
    '九十五': (95, {'ja'}), '九十六': (96, {'ja'}), '九十七': (97, {'ja'}), '九十八': (98, {'ja'}), '九十九': (99, {'ja'}),
    '百': (100, {'ja'}), '一百': (100, {'ja'}),
    
    # Japanese - Romaji (for convenience)
    'zero': (0, {'ja', 'fr'}), 'rei': (0, {'ja'}), 'ichi': (1, {'ja'}), 'ni': (2, {'ja', 'dk', 'no'}), 'san': (3, {'ja'}),
    'yon': (4, {'ja'}), 'shi': (4, {'ja'}), 'go': (5, {'ja'}), 'roku': (6, {'ja'}), 'nana': (7, {'ja'}),
    'shichi': (7, {'ja'}), 'hachi': (8, {'ja'}), 'kyuu': (9, {'ja'}), 'kyu': (9, {'ja'}), 'ku': (9, {'ja'}),
    'juu': (10, {'ja'}), 'ju': (10, {'ja'}), 'juuichi': (11, {'ja'}), 'juichi': (11, {'ja'}), 'juuni': (12, {'ja'}), 
    'juni': (12, {'ja'}), 'juusan': (13, {'ja'}), 'jusan': (13, {'ja'}), 'juuyon': (14, {'ja'}), 'juyon': (14, {'ja'}),
    'juushi': (14, {'ja'}), 'jushi': (14, {'ja'}), 'juugo': (15, {'ja'}), 'jugo': (15, {'ja'}), 'juuroku': (16, {'ja'}),
    'juroku': (16, {'ja'}), 'juunana': (17, {'ja'}), 'junana': (17, {'ja'}), 'juushichi': (17, {'ja'}), 'jushichi': (17, {'ja'}),
    'juuhachi': (18, {'ja'}), 'juhachi': (18, {'ja'}), 'juukyuu': (19, {'ja'}), 'jukyu': (19, {'ja'}), 'juuku': (19, {'ja'}),
    'juku': (19, {'ja'}), 'nijuu': (20, {'ja'}), 'niju': (20, {'ja'}), 'nijuuichi': (21, {'ja'}), 'nijuichi': (21, {'ja'}),
    'nijuuni': (22, {'ja'}), 'nijuni': (22, {'ja'}), 'nijuusan': (23, {'ja'}), 'nijusan': (23, {'ja'}), 'nijuuyon': (24, {'ja'}),
    'nijuyon': (24, {'ja'}), 'nijuushi': (24, {'ja'}), 'nijushi': (24, {'ja'}), 'nijuugo': (25, {'ja'}), 'nijugo': (25, {'ja'}),
    'nijuuroku': (26, {'ja'}), 'nijuroku': (26, {'ja'}), 'nijuunana': (27, {'ja'}), 'nijunana': (27, {'ja'}), 
    'nijuushichi': (27, {'ja'}), 'nijushichi': (27, {'ja'}), 'nijuuhachi': (28, {'ja'}), 'nijuhachi': (28, {'ja'}),
    'nijuukyuu': (29, {'ja'}), 'nijukyu': (29, {'ja'}), 'nijuuku': (29, {'ja'}), 'nijuku': (29, {'ja'}), 'sanjuu': (30, {'ja'}),
    'sanju': (30, {'ja'}), 'yonjuu': (40, {'ja'}), 'yonju': (40, {'ja'}), 'shijuu': (40, {'ja'}), 'shiju': (40, {'ja'}),
    'gojuu': (50, {'ja'}), 'goju': (50, {'ja'}), 'rokujuu': (60, {'ja'}), 'rokuju': (60, {'ja'}), 'nanajuu': (70, {'ja'}),
    'nanaju': (70, {'ja'}), 'shichijuu': (70, {'ja'}), 'shichiju': (70, {'ja'}), 'hachijuu': (80, {'ja'}), 'hachiju': (80, {'ja'}),
    'kyuujuu': (90, {'ja'}), 'kyuju': (90, {'ja'}), 'hyaku': (100, {'ja'}), 'ippyaku': (100, {'ja'}),
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