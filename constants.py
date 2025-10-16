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
    'es': '🇪🇸',
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
    'es': '🇪🇸',
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

    # Spanish (0 - 100)
    'cero': (0, {'es'}),
    'uno': (1, {'es'}), 'un': (1, {'es'}),
    'dos': (2, {'es'}), 'tres': (3, {'es'}), 'cuatro': (4, {'es'}), 'cinco': (5, {'es'}),
    'seis': (6, {'es'}), 'siete': (7, {'es'}), 'ocho': (8, {'es'}), 'nueve': (9, {'es'}),
    'diez': (10, {'es'}), 'once': (11, {'es'}), 'doce': (12, {'es'}), 'trece': (13, {'es'}),
    'catorce': (14, {'es'}), 'quince': (15, {'es'}), 'dieciseis': (16, {'es'}), 'dieciséis': (16, {'es'}),
    'diecisiete': (17, {'es'}), 'dieciocho': (18, {'es'}), 'diecinueve': (19, {'es'}), 'veinte': (20, {'es'}),

    # 21-29 variants
    'veintiuno': (21, {'es'}), 'veintiún': (21, {'es'}), 'veintidos': (22, {'es'}), 'veintidós': (22, {'es'}),
    'veintitres': (23, {'es'}), 'veintitrés': (23, {'es'}), 'veinticuatro': (24, {'es'}), 'veinticinco': (25, {'es'}),
    'veintiseis': (26, {'es'}), 'veintiséis': (26, {'es'}), 'veintisiete': (27, {'es'}), 'veintiocho': (28, {'es'}), 'veintinueve': (29, {'es'}),

    # Tens and combinations with ' y '
    'treinta': (30, {'es'}), 'treinta y uno': (31, {'es'}), 'treinta y dos': (32, {'es'}), 'treinta y tres': (33, {'es'}),
    'treinta y cuatro': (34, {'es'}), 'treinta y cinco': (35, {'es'}), 'treinta y seis': (36, {'es'}), 'treinta y siete': (37, {'es'}),
    'treinta y ocho': (38, {'es'}), 'treinta y nueve': (39, {'es'}),
    'cuarenta': (40, {'es'}), 'cuarenta y uno': (41, {'es'}), 'cuarenta y dos': (42, {'es'}), 'cuarenta y tres': (43, {'es'}),
    'cuarenta y cuatro': (44, {'es'}), 'cuarenta y cinco': (45, {'es'}), 'cuarenta y seis': (46, {'es'}), 'cuarenta y siete': (47, {'es'}),
    'cuarenta y ocho': (48, {'es'}), 'cuarenta y nueve': (49, {'es'}),
    'cincuenta': (50, {'es'}), 'cincuenta y uno': (51, {'es'}), 'cincuenta y dos': (52, {'es'}), 'cincuenta y tres': (53, {'es'}),
    'cincuenta y cuatro': (54, {'es'}), 'cincuenta y cinco': (55, {'es'}), 'cincuenta y seis': (56, {'es'}), 'cincuenta y siete': (57, {'es'}),
    'cincuenta y ocho': (58, {'es'}), 'cincuenta y nueve': (59, {'es'}),
    'sesenta': (60, {'es'}), 'sesenta y uno': (61, {'es'}), 'sesenta y dos': (62, {'es'}), 'sesenta y tres': (63, {'es'}),
    'sesenta y cuatro': (64, {'es'}), 'sesenta y cinco': (65, {'es'}), 'sesenta y seis': (66, {'es'}), 'sesenta y siete': (67, {'es'}),
    'sesenta y ocho': (68, {'es'}), 'sesenta y nueve': (69, {'es'}),
    'setenta': (70, {'es'}), 'setenta y uno': (71, {'es'}), 'setenta y dos': (72, {'es'}), 'setenta y tres': (73, {'es'}),
    'setenta y cuatro': (74, {'es'}), 'setenta y cinco': (75, {'es'}), 'setenta y seis': (76, {'es'}), 'setenta y siete': (77, {'es'}),
    'setenta y ocho': (78, {'es'}), 'setenta y nueve': (79, {'es'}),
    'ochenta': (80, {'es'}), 'ochenta y uno': (81, {'es'}), 'ochenta y dos': (82, {'es'}), 'ochenta y tres': (83, {'es'}),
    'ochenta y cuatro': (84, {'es'}), 'ochenta y cinco': (85, {'es'}), 'ochenta y seis': (86, {'es'}), 'ochenta y siete': (87, {'es'}),
    'ochenta y ocho': (88, {'es'}), 'ochenta y nueve': (89, {'es'}),
    'noventa': (90, {'es'}), 'noventa y uno': (91, {'es'}), 'noventa y dos': (92, {'es'}), 'noventa y tres': (93, {'es'}),
    'noventa y cuatro': (94, {'es'}), 'noventa y cinco': (95, {'es'}), 'noventa y seis': (96, {'es'}), 'noventa y siete': (97, {'es'}),
    'noventa y ocho': (98, {'es'}), 'noventa y nueve': (99, {'es'}),
    'cien': (100, {'es'}), 'ciento': (100, {'es'}),

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
    # NOTE: some words overlap with other languages (e.g. 'nul' and 'tres').
    # Merge language tags so overlapping words include all relevant language codes.
    'nul': (0, {'dk', 'nl'}), 'en': (1, {'dk', 'no'}), 'et': (1, {'dk'}), 'to': (2, {'dk', 'no'}), 'fire': (4, {'dk', 'no'}),
    'seks': (6, {'dk', 'no'}), 'syv': (7, {'dk', 'no'}), 'otte': (8, {'dk'}), 'ni': (9, {'dk', 'no'}), 'ti': (10, {'dk', 'no'}),
    'elleve': (11, {'dk', 'no'}), 'tretten': (13, {'dk', 'no'}), 'fjorten': (14, {'dk', 'no'}), 'femten': (15, {'dk'}),
    'seksten': (16, {'dk', 'no'}), 'sytten': (17, {'dk', 'no'}), 'søtten': (17, {'no'}), 'atten': (18, {'dk', 'no'}), 'nitten': (19, {'dk', 'no'}), 'tyve': (20, {'dk', 'no'}),
    'enogtyve': (21, {'dk'}), 'toog': (22, {'dk'}), 'treogtyve': (23, {'dk'}), 'fireogtyve': (24, {'dk'}),
    'femogtyve': (25, {'dk'}), 'seksogtyve': (26, {'dk'}), 'syvogtyve': (27, {'dk'}), 'otteogtyve': (28, {'dk'}),
    'niogtyve': (29, {'dk'}), 'tredive': (30, {'dk'}), 'fyrre': (40, {'dk'}), 'fyrretyve': (40, {'dk'}),
    'halvtreds': (50, {'dk'}), 'tres': (60, {'dk', 'es'}), 'halvfjerds': (70, {'dk'}), 'firs': (80, {'dk'}),
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