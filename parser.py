#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""Number parsing and interpretation logic for the counting bot."""

import re
import math
import random
import concurrent.futures
from word2number import w2n
from simpleeval import simple_eval, NumberTooHigh
from constants import MATH_CONSTANTS, MULTILANG_NUMBERS

# Thread pool for safe expression evaluation
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)


def evaluate_expression_safe(expression):
    """Safely evaluate a mathematical expression."""
    if len(expression) > 200:
        raise ValueError("Expression is too long.")
    # Replace colon with division operator
    expression = expression.replace(':', '/')
    return simple_eval(expression.replace(',', '.'), functions={'sqrt': math.sqrt})


def calculate_factorial(n):
    """Calculate factorial of n, with safety limits."""
    if n < 0 or n > 20:
        return None
    return math.factorial(n)


def process_factorials(text):
    """Process factorial expressions in text."""
    pattern = r'(\d+)!'
    
    def replace_factorial(match):
        result = calculate_factorial(int(match.group(1)))
        return str(result) if result is not None else match.group(0)
    
    return re.sub(pattern, replace_factorial, text)


def try_parse_multilang_number(text):
    """Try to parse a number in various languages."""
    clean_text = text.lower().strip()
    
    if clean_text in MULTILANG_NUMBERS:
        return MULTILANG_NUMBERS[clean_text]
    
    normalized = clean_text.replace(' et ', '-et-').replace(' ', '-')
    if normalized in MULTILANG_NUMBERS:
        return MULTILANG_NUMBERS[normalized]
    
    words = clean_text.split()
    if len(words) == 2:
        tens_word, ones_word = words[0], words[1]
        if tens_word in MULTILANG_NUMBERS and ones_word in MULTILANG_NUMBERS:
            tens_val, tens_langs = MULTILANG_NUMBERS[tens_word]
            ones_val, ones_langs = MULTILANG_NUMBERS[ones_word]
            # Combine languages from both parts
            combined_langs = tens_langs.union(ones_langs)
            if tens_val in [20, 30, 40, 50, 60, 70, 80, 90] and 1 <= ones_val <= 9:
                return (tens_val + ones_val, combined_langs)
    
    if clean_text.startswith('soixante-'):
        remainder = clean_text[9:]
        if remainder in MULTILANG_NUMBERS:
            rem_val, rem_langs = MULTILANG_NUMBERS[remainder]
            if 10 <= rem_val <= 19:
                return (60 + rem_val, {'fr'}.union(rem_langs))
    
    if clean_text.startswith('quatre-vingt-'):
        remainder = clean_text[13:]
        if remainder in MULTILANG_NUMBERS:
            rem_val, rem_langs = MULTILANG_NUMBERS[remainder]
            if 1 <= rem_val <= 19:
                return (80 + rem_val, {'fr'}.union(rem_langs))
    
    return None

def is_compound_number_word(text):
    """Check if a hyphenated word is a compound number word (like twenty-one)."""
    # Common compound patterns that should NOT be treated as math
    compound_patterns = [
        r'^(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)-(one|two|three|four|five|six|seven|eight|nine)$',
        r'^(vingt|trente|quarante|cinquante|soixante)-(et-)?(un|deux|trois|quatre|cinq|six|sept|huit|neuf)$',
        r'^(dix)-(sept|huit|neuf)$',
        # Add more compound patterns for other languages as needed
    ]
    
    for pattern in compound_patterns:
        if re.match(pattern, text.lower()):
            return True
    return False


def starts_with_parseable(text):
    """Check if text starts with something parseable."""
    text = text.strip().lower()
    
    if re.match(r'^\d', text) or re.match(r'^[(\-+:]', text) or text.startswith(('sqrt(', 'random(')):
        return True
    
    first_token_match = re.match(r'^([a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+)*)[+\-*/:()%^]?', text)
    if first_token_match:
        first_word = first_token_match.group(1)
        clean_word = re.sub(r'[^\w\-]', '', first_word)
        
        if clean_word.lower() in MATH_CONSTANTS or clean_word in MULTILANG_NUMBERS:
            return True
        
        try:
            w2n.word_to_num(clean_word)
            return True
        except ValueError:
            pass
    
    return False


def has_math_operators(text):
    """Check if text contains math operators."""
    return bool(re.search(r'[+\-*/:()%^!]', text)) or 'sqrt(' in text.lower()


def has_spaced_operators(text):
    """Check if text has operators with spaces around them."""
    return bool(re.search(r'\s[+\-*/:()%^]\s', text))


def has_unspaced_operators(text):
    """Check if text has operators without spaces, excluding compound words."""
    temp_text = text
    
    # Remove compound number words to avoid false positives
    for pattern in [r'\b(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)-\w+\b',
                    r'\b\w+-(one|two|three|four|five|six|seven|eight|nine|teen|ty)\b',
                    r'\bvingt-(et-)?\w+\b', r'\bdix-(sept|huit|neuf)\b']:
        temp_text = re.sub(pattern, '__COMPOUND__', temp_text, flags=re.IGNORECASE)
    
    return bool(re.search(r'[+\-*/:()%^]', temp_text))


def process_random_functions(text):
    """Process random(min,max) functions in text."""
    random_values = []
    pattern = r'random\s*\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)'
    
    def replace_random(match):
        min_val, max_val = float(match.group(1)), float(match.group(2))
        if min_val > max_val:
            min_val, max_val = max_val, min_val
        random_num = random.randint(int(min_val), int(max_val))
        random_values.append((min_val, max_val, random_num))
        return str(random_num)
    
    return re.sub(pattern, replace_random, text, flags=re.IGNORECASE), random_values


def preprocess_expression(text):
    """Preprocess mathematical expression for evaluation."""
    languages_used = set()
    text = text.replace('^', '**')
    # Replace colon with division
    text = text.replace(':', '/')
    
    def replace_sqrt(match):
        return f"({match.group(1)})**0.5"
    
    text = re.sub(r'sqrt\s*\(\s*([^)]+)\s*\)', replace_sqrt, text, flags=re.IGNORECASE)
    
    for constant, value in MATH_CONSTANTS.items():
        text = re.sub(r'\b' + re.escape(constant) + r'\b', str(value), text, flags=re.IGNORECASE)
    
    words_with_pos = [(m.group(), m.start(), m.end()) 
                      for m in re.finditer(r'\b[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+)*\b', text)]
    
    for word, start_pos, end_pos in reversed(words_with_pos):
        multilang_result = try_parse_multilang_number(word.lower())
        if multilang_result is not None:
            num_val, langs = multilang_result
            text = text[:start_pos] + str(num_val) + text[end_pos:]
            languages_used.update(langs)  # Add all languages for this word
            continue
        
        try:
            number = w2n.word_to_num(word.lower())
            text = text[:start_pos] + str(number) + text[end_pos:]
            languages_used.add('en')
        except ValueError:
            continue
    
    return text, languages_used


def extract_first_number_from_text(text):
    """Extract the first valid number from text."""
    if has_math_operators(text):
        return None, None, set()
    
    found_numbers = []
    languages_used = set()
    current_pos = 0
    
    # Find digit numbers with their positions
    for match in re.finditer(r'\b(\d+)\b', text):
        found_numbers.append((int(match.group(1)), match.start(), 'digit', set()))
    
    # Find multilang numbers
    words = text.lower().split()
    for i, word in enumerate(words):
        clean_word = re.sub(r'[^\w\-]', '', word)
        multilang_result = try_parse_multilang_number(clean_word)
        if multilang_result is not None:
            multilang_num, langs = multilang_result
            word_pos = text.lower().find(word.lower(), current_pos)
            found_numbers.append((multilang_num, word_pos, 'multilang', langs))
            current_pos = word_pos + len(word)
    
    # Try English word2number only if no multilang found
    if not any(entry[2] == 'multilang' for entry in found_numbers):
        current_pos = 0
        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w\-]', '', word)
            # Skip if it's a hyphenated non-compound
            if '-' in clean_word and not is_valid_compound_word(clean_word):
                continue
            try:
                num = w2n.word_to_num(clean_word)
                word_pos = text.lower().find(word.lower(), current_pos)
                found_numbers.append((num, word_pos, 'english', {'en'}))
                current_pos = word_pos + len(word)
                break  # Take the first one
            except ValueError:
                pass
    
    # Filter valid numbers
    valid_numbers = [(num, pos, typ, langs) for num, pos, typ, langs in found_numbers if num > 0]
    
    if valid_numbers:
        # Sort by position to get the first one
        valid_numbers.sort(key=lambda x: x[1])
        first_num, first_pos, first_type, first_langs = valid_numbers[0]
        # CRITICAL: Only return languages from the FIRST extracted number
        return first_num, first_pos, first_langs
    
    return None, None, set()


def analyze_input_types(original_text):
    """Analyze and categorize the types of input in the text."""
    types = set()
    
    if re.search(r'(\d+|[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+)*)!', original_text):
        types.add('factorial')
        types.add('math')
    
    if re.search(r'[+\-*/:()%^]', original_text):
        types.add('math')
    
    if re.search(r'sqrt\s*\(', original_text, re.IGNORECASE):
        types.add('sqrt')
    
    if re.search(r'random\s*\(', original_text, re.IGNORECASE):
        types.add('random')
    
    for constant in MATH_CONSTANTS:
        if re.search(r'\b' + re.escape(constant) + r'\b', original_text, re.IGNORECASE):
            types.add('constants')
            break
    
    words = re.findall(r'\b[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+)*\b', original_text)
    for word in words:
        if try_parse_multilang_number(word.lower()) is not None:
            types.add('multilang')
            continue
        try:
            w2n.word_to_num(word.lower())
            types.add('text')
            break
        except ValueError:
            continue
    
    if re.search(r'\d+[.,]\d+', original_text):
        types.add('decimal')
    
    # Ensure 'integer' type is added when we have simple integers
    if not types and re.match(r'^\d+$', original_text.strip()):
        types.add('integer')
    
    return types


def can_be_hyphenated_math(text):
    """Check if hyphenated text could potentially be interpreted as math."""
    parts = text.split('-')
    if len(parts) == 2:
        first_part = parts[0].strip()
        second_part = parts[1].strip()
        
        # Check if both parts are number words
        first_is_number = False
        second_is_number = False
        
        # Check multilang
        if try_parse_multilang_number(first_part) is not None:
            first_is_number = True
        else:
            try:
                w2n.word_to_num(first_part)
                first_is_number = True
            except:
                pass
        
        if try_parse_multilang_number(second_part) is not None:
            second_is_number = True
        else:
            try:
                w2n.word_to_num(second_part)
                second_is_number = True
            except:
                pass
        
        return first_is_number and second_is_number
    
    return False


def is_valid_compound_word(text):
    """Check if a hyphenated word is a valid compound number word in any language."""
    text_lower = text.lower()
    
    # Check if it's directly in MULTILANG_NUMBERS (like "twenty-one", "vingt-deux")
    if text_lower in MULTILANG_NUMBERS:
        return True
    
    # Check English compound patterns (twenty-one through ninety-nine)
    english_tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    english_ones = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    
    parts = text_lower.split('-')
    if len(parts) == 2:
        if parts[0] in english_tens and parts[1] in english_ones:
            return True
    
    # Try w2n to see if it's a valid compound word
    try:
        # Only for simple hyphenated pairs, not complex phrases
        if '-' in text_lower and len(text_lower.split()) == 1:
            num = w2n.word_to_num(text_lower)
            # Verify it's not being misinterpreted as addition
            # Check if the parts separately would add up to the same number
            parts = text_lower.split('-')
            if len(parts) == 2:
                try:
                    first_num = w2n.word_to_num(parts[0])
                    second_num = w2n.word_to_num(parts[1])
                    # If w2n returns the sum, it's misinterpreting; it's not a valid compound
                    if num == first_num + second_num:
                        return False
                    # If it returns something else, it might be a valid compound
                    return True
                except:
                    pass
    except:
        pass
    
    return False


def get_all_possible_interpretations(text):
    """Get all possible interpretations of the input text."""
    interpretations = []
    processed_text, random_values = process_random_functions(text)
    all_languages = set()
    
    # Check if it could be interpreted as hyphenated math
    if '-' in processed_text and can_be_hyphenated_math(processed_text):
        try:
            # Try as hyphenated math (e.g., "twenty-one" as 20-1=19)
            math_version = processed_text.replace('-', ' - ')
            expr_processed, expr_languages = preprocess_expression(math_version)
            all_languages_math = set(expr_languages)
            
            future = executor.submit(evaluate_expression_safe, process_factorials(expr_processed))
            result = future.result(timeout=0.5)
            
            if result is not None and isinstance(result, (int, float)):
                rounded = round(result)
                if rounded > 0:
                    interpretations.append((rounded, 'hyphenated_math', 
                                          f'Hyphenated math: {text} → {rounded}', 
                                          random_values, all_languages_math))
        except:
            pass
    
    # Check standard math expressions
    is_math_expression = (has_spaced_operators(processed_text) or 
                         has_unspaced_operators(processed_text) or 
                         '!' in text or 
                         'sqrt(' in processed_text.lower() or 
                         any(const in processed_text.lower() for const in MATH_CONSTANTS))
    
    if is_math_expression:
        try:
            expr_processed, expr_languages = preprocess_expression(processed_text)
            all_languages.update(expr_languages)
            expr_with_factorials = process_factorials(expr_processed)
            
            future = executor.submit(evaluate_expression_safe, expr_with_factorials)
            result = future.result(timeout=0.5)
            
            if result is not None and isinstance(result, (int, float)):
                rounded = round(result)
                if rounded > 0:
                    math_type = 'factorial_math' if '!' in text else 'math_expression'
                    interpretations.append((rounded, math_type, f'Math: {text} → {rounded}', 
                                          random_values, all_languages))
        except (concurrent.futures.TimeoutError, NumberTooHigh):
            interpretations.append((None, 'evaluation_timeout', 
                                  'Calculation was too complex or took too long.', None, set()))
            return interpretations
        except Exception:
            pass
    
    # Try as compound word or written number
    # Only if it's a valid compound word OR doesn't contain hyphens
    if '-' not in processed_text or is_valid_compound_word(processed_text):
        try:
            for attempt_text in [processed_text, 
                                re.sub(r'\s+', ' ', processed_text.strip())]:
                # Skip long phrases that might contain multiple numbers
                if len(attempt_text.split()) > 3:
                    continue
                    
                try:
                    number = w2n.word_to_num(attempt_text.lower())
                    if number > 0:
                        interpretations.append((number, 'written', f'Written: {text} → {number}', 
                                              random_values, {'en'}))
                        break
                except ValueError:
                    continue
        except:
            pass
    
    # Try extraction if not a math expression
    if not is_math_expression or not interpretations:
        extracted_info, _, extract_languages = extract_first_number_from_text(text)
        if extracted_info and extracted_info > 0:
            interpretations.append((extracted_info, 'extracted', 
                                  f'Extracted: {text} → {extracted_info}', None, extract_languages))
        
        clean_text = processed_text.strip().lower()
        if clean_text in MATH_CONSTANTS:
            const_value = MATH_CONSTANTS[clean_text]
            rounded = round(const_value)
            if rounded > 0:
                interpretations.append((rounded, 'constant', f'Constant: {text} → {rounded}', 
                                      random_values, set()))
        
        if not has_spaced_operators(processed_text):
            multilang_result = try_parse_multilang_number(processed_text)
            if multilang_result is not None:
                multilang_num, langs = multilang_result
                if multilang_num > 0:
                    interpretations.append((multilang_num, 'multilang', 
                                          f'Multilang: {text} → {multilang_num}', 
                                          random_values, langs))
    
    return interpretations


def parse_number_with_context(text, expected_number):
    """Parse a number from text with context awareness."""
    text = text.strip()
    
    if not starts_with_parseable(text):
        return None, set(), 'starts_with_non_parseable', None, set()
    
    if re.match(r'^\d+$', text):
        return int(text), {'integer'}, 'simple_integer', None, set()
    
    if re.match(r'^[-+]?\d*[.,]\d+$', text):
        try:
            value = float(text.replace(',', '.'))
            rounded = round(value)
            if rounded > 0:
                return rounded, {'decimal'}, 'simple_decimal', None, set()
        except ValueError:
            pass
    
    interpretations = get_all_possible_interpretations(text)
    
    if not interpretations:
        return None, set(), 'no_valid_interpretation', None, set()
    
    if interpretations[0][1] == 'evaluation_timeout':
        return None, set(), 'evaluation_timeout', None, set()
    
    # CRITICAL: Check for context matches FIRST
    context_matches = [interp for interp in interpretations if interp[0] == expected_number]
    
    if context_matches:
        # When we have a context match, prioritize by type
        # 'written' should be preferred over 'hyphenated_math' for compound words when both match
        priority_order = ['written', 'hyphenated_math', 'math_expression', 'factorial_math', 
                         'extracted', 'constant', 'multilang']
        
        for preferred_type in priority_order:
            for value, interp_type, desc, random_info, languages in context_matches:
                if interp_type == preferred_type:
                    return (value, analyze_input_types(text), f'context_match_{interp_type}', 
                           random_info, languages)
        
        # If no preferred type found, return first context match
        return (context_matches[0][0], analyze_input_types(text), 
               f'context_match_{context_matches[0][1]}', 
               context_matches[0][3], context_matches[0][4])
    
    # No context match - use default priority (prefer written form for compound words)
    for prio_type in ['written', 'hyphenated_math', 'math_expression', 'factorial_math', 
                      'constant', 'extracted', 'multilang']:
        for interp in interpretations:
            if interp[1] == prio_type:
                return (interp[0], analyze_input_types(text), f'priority_{prio_type}', 
                       interp[3], interp[4])
    
    value, interp_type, desc, random_info, languages = interpretations[0]
    return value, analyze_input_types(text), f'fallback_{interp_type}', random_info, languages