#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""Number parsing and interpretation logic for the counting bot."""

import re
import math
import random
import concurrent.futures
from word2number import w2n
from simpleeval import simple_eval, NumberTooHigh
from constants import MATH_CONSTANTS, MULTILANG_NUMBERS, ROMAN_NUMERALS, AMBIGUOUS_NUMBERS

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


def calculate_fibonacci(n):
    """Calculate the nth Fibonacci number, with safety limits."""
    if n < 0 or n > 50:
        return None
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def try_parse_roman_numeral(text):
    """
    Try to parse a Roman numeral (CASE-SENSITIVE - must be UPPERCASE).
    Returns the integer value if valid, None otherwise.
    """
    # Must be uppercase and only contain valid Roman numeral characters
    if not text or not text.isupper():
        return None
    
    if not all(c in 'IVXLCDM' for c in text):
        return None
    
    # Check direct lookup first (for common values up to 100)
    if text in ROMAN_NUMERALS:
        return ROMAN_NUMERALS[text]
    
    # For values > 100 or not in our lookup table, calculate manually
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    
    total = 0
    prev_value = 0
    
    for char in reversed(text):
        value = roman_values.get(char, 0)
        if value == 0:
            return None
        
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    
    return total if total > 0 else None


def process_factorials(text):
    """Process factorial expressions in text."""
    pattern = r'(\d+)!'
    
    def replace_factorial(match):
        result = calculate_factorial(int(match.group(1)))
        return str(result) if result is not None else match.group(0)
    
    return re.sub(pattern, replace_factorial, text)


def process_binary_hex(text):
    """
    Process binary (0b...) and hexadecimal (0x...) numbers in text.
    
    Returns: (processed_text, used_programmer_notation)
    
    Examples:
    - 0b1010 -> 10
    - 0xFF -> 255
    - 0x2A -> 42
    """
    used_programmer = False
    result = text
    
    # Process hexadecimal: 0x followed by hex digits (case insensitive)
    hex_pattern = r'0x([0-9a-fA-F]+)'
    
    def replace_hex(match):
        nonlocal used_programmer
        try:
            value = int(match.group(1), 16)
            used_programmer = True
            return str(value)
        except ValueError:
            return match.group(0)
    
    result = re.sub(hex_pattern, replace_hex, result)
    
    # Process binary: 0b followed by binary digits
    binary_pattern = r'0b([01]+)'
    
    def replace_binary(match):
        nonlocal used_programmer
        try:
            value = int(match.group(1), 2)
            used_programmer = True
            return str(value)
        except ValueError:
            return match.group(0)
    
    result = re.sub(binary_pattern, replace_binary, result, flags=re.IGNORECASE)
    
    # Process octal: 0o followed by octal digits (bonus feature)
    octal_pattern = r'0o([0-7]+)'
    
    def replace_octal(match):
        nonlocal used_programmer
        try:
            value = int(match.group(1), 8)
            used_programmer = True
            return str(value)
        except ValueError:
            return match.group(0)
    
    result = re.sub(octal_pattern, replace_octal, result, flags=re.IGNORECASE)
    
    return result, used_programmer


def try_parse_multilang_number(text, expected_number=None):
    """
    Try to parse a number in various languages.
    If expected_number is provided, use it to disambiguate words with multiple meanings.
    """
    clean_text = text.lower().strip()
    
    def add_english_if_matches(value, langs):
        """Add 'en' to languages if word is also valid English with same value."""
        result_langs = set(langs)  # Create a copy to avoid modifying original
        try:
            english_value = w2n.word_to_num(clean_text)
            if english_value == value:
                result_langs.add('en')
        except ValueError:
            pass
        return result_langs
    
    # Check for ambiguous numbers first
    if clean_text in AMBIGUOUS_NUMBERS:
        possible_values = AMBIGUOUS_NUMBERS[clean_text]
        
        # If we have context (expected_number), try to find a matching interpretation
        if expected_number is not None:
            for value, langs in possible_values:
                if value == expected_number:
                    return (value, add_english_if_matches(value, langs))
        
        # Without context or no match, return the first one as default
        value, langs = possible_values[0]
        return (value, add_english_if_matches(value, langs))
    
    if clean_text in MULTILANG_NUMBERS:
        value, langs = MULTILANG_NUMBERS[clean_text]
        return (value, add_english_if_matches(value, langs))
    
    normalized = clean_text.replace(' et ', '-et-').replace(' ', '-')
    if normalized in MULTILANG_NUMBERS:
        value, langs = MULTILANG_NUMBERS[normalized]
        return (value, add_english_if_matches(value, langs))
    
    words = clean_text.split()
    if len(words) == 2:
        tens_word, ones_word = words[0], words[1]
        if tens_word in MULTILANG_NUMBERS and ones_word in MULTILANG_NUMBERS:
            tens_val, tens_langs = MULTILANG_NUMBERS[tens_word]
            ones_val, ones_langs = MULTILANG_NUMBERS[ones_word]
            combined_langs = tens_langs.union(ones_langs)
            if tens_val in [20, 30, 40, 50, 60, 70, 80, 90] and 1 <= ones_val <= 9:
                combined_val = tens_val + ones_val
                return (combined_val, add_english_if_matches(combined_val, combined_langs))

    # Spanish style 'tens y ones' e.g. 'treinta y cuatro'
    if ' y ' in clean_text:
        parts = [p.strip() for p in clean_text.split(' y ')]
        if len(parts) == 2:
            tens_word, ones_word = parts[0], parts[1]
            if tens_word in MULTILANG_NUMBERS and ones_word in MULTILANG_NUMBERS:
                tens_val, tens_langs = MULTILANG_NUMBERS[tens_word]
                ones_val, ones_langs = MULTILANG_NUMBERS[ones_word]
                combined_langs = tens_langs.union(ones_langs)
                if tens_val in [20, 30, 40, 50, 60, 70, 80, 90] and 1 <= ones_val <= 9:
                    combined_val = tens_val + ones_val
                    return (combined_val, add_english_if_matches(combined_val, combined_langs))
    
    if clean_text.startswith('soixante-'):
        remainder = clean_text[9:]
        if remainder in MULTILANG_NUMBERS:
            rem_val, rem_langs = MULTILANG_NUMBERS[remainder]
            if 10 <= rem_val <= 19:
                combined_val = 60 + rem_val
                return (combined_val, add_english_if_matches(combined_val, {'fr'}.union(rem_langs)))
    
    if clean_text.startswith('quatre-vingt-'):
        remainder = clean_text[13:]
        if remainder in MULTILANG_NUMBERS:
            rem_val, rem_langs = MULTILANG_NUMBERS[remainder]
            if 1 <= rem_val <= 19:
                combined_val = 80 + rem_val
                return (combined_val, add_english_if_matches(combined_val, {'fr'}.union(rem_langs)))
    
    return None


def try_parse_multilang_number_all_interpretations(text):
    """
    Try to parse a number in various languages and return ALL possible interpretations.
    Returns a list of (value, languages) tuples.
    """
    clean_text = text.lower().strip()
    results = []
    
    def add_english_if_matches(value, langs):
        """Add 'en' to languages if word is also valid English with same value."""
        result_langs = set(langs)  # Create a copy to avoid modifying original
        try:
            english_value = w2n.word_to_num(clean_text)
            if english_value == value:
                result_langs.add('en')
        except ValueError:
            pass
        return result_langs
    
    # Check for ambiguous numbers first
    if clean_text in AMBIGUOUS_NUMBERS:
        for value, langs in AMBIGUOUS_NUMBERS[clean_text]:
            results.append((value, add_english_if_matches(value, langs)))
    
    # Also check regular multilang numbers
    if clean_text in MULTILANG_NUMBERS:
        value, langs = MULTILANG_NUMBERS[clean_text]
        # Avoid duplicates
        if not any(v == value for v, _ in results):
            results.append((value, add_english_if_matches(value, langs)))
    
    # Check normalized form
    normalized = clean_text.replace(' et ', '-et-').replace(' ', '-')
    if normalized in MULTILANG_NUMBERS and normalized != clean_text:
        value, langs = MULTILANG_NUMBERS[normalized]
        if not any(v == value for v, _ in results):
            results.append((value, add_english_if_matches(value, langs)))
    
    # Two-word combinations
    words = clean_text.split()
    if len(words) == 2:
        tens_word, ones_word = words[0], words[1]
        if tens_word in MULTILANG_NUMBERS and ones_word in MULTILANG_NUMBERS:
            tens_val, tens_langs = MULTILANG_NUMBERS[tens_word]
            ones_val, ones_langs = MULTILANG_NUMBERS[ones_word]
            combined_langs = tens_langs.union(ones_langs)
            if tens_val in [20, 30, 40, 50, 60, 70, 80, 90] and 1 <= ones_val <= 9:
                combined_val = tens_val + ones_val
                if not any(v == combined_val for v, _ in results):
                    results.append((combined_val, add_english_if_matches(combined_val, combined_langs)))

    # Spanish style 'tens y ones'
    if ' y ' in clean_text:
        parts = [p.strip() for p in clean_text.split(' y ')]
        if len(parts) == 2:
            tens_word, ones_word = parts[0], parts[1]
            if tens_word in MULTILANG_NUMBERS and ones_word in MULTILANG_NUMBERS:
                tens_val, tens_langs = MULTILANG_NUMBERS[tens_word]
                ones_val, ones_langs = MULTILANG_NUMBERS[ones_word]
                combined_langs = tens_langs.union(ones_langs)
                if tens_val in [20, 30, 40, 50, 60, 70, 80, 90] and 1 <= ones_val <= 9:
                    combined_val = tens_val + ones_val
                    if not any(v == combined_val for v, _ in results):
                        results.append((combined_val, add_english_if_matches(combined_val, combined_langs)))
    
    # French special forms
    if clean_text.startswith('soixante-'):
        remainder = clean_text[9:]
        if remainder in MULTILANG_NUMBERS:
            rem_val, rem_langs = MULTILANG_NUMBERS[remainder]
            if 10 <= rem_val <= 19:
                combined_val = 60 + rem_val
                if not any(v == combined_val for v, _ in results):
                    results.append((combined_val, add_english_if_matches(combined_val, {'fr'}.union(rem_langs))))
    
    if clean_text.startswith('quatre-vingt-'):
        remainder = clean_text[13:]
        if remainder in MULTILANG_NUMBERS:
            rem_val, rem_langs = MULTILANG_NUMBERS[remainder]
            if 1 <= rem_val <= 19:
                combined_val = 80 + rem_val
                if not any(v == combined_val for v, _ in results):
                    results.append((combined_val, add_english_if_matches(combined_val, {'fr'}.union(rem_langs))))
    
    return results


def is_number_word(text):
    """Check if a word is a recognized number word in any language."""
    text_lower = text.lower().strip()
    
    # Check ambiguous numbers
    if text_lower in AMBIGUOUS_NUMBERS:
        return True
    
    # Check multilang numbers
    if text_lower in MULTILANG_NUMBERS:
        return True
    
    # Check math constants
    if text_lower in MATH_CONSTANTS:
        return True
    
    # Check English word2number
    try:
        w2n.word_to_num(text_lower)
        return True
    except ValueError:
        pass
    
    return False


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
    text_stripped = text.strip()
    text_lower = text_stripped.lower()
    
    # Check for digits or opening parenthesis or leading operators
    if re.match(r'^\d', text_stripped) or re.match(r'^[(\-+:]', text_stripped):
        return True
    
    # Check for binary/hex notation
    if re.match(r'^0[bBxXoO]', text_stripped):
        return True
    
    # Check for known functions - these can have word arguments inside
    if re.match(r'^(?:sqrt|random|log|log10|log2|ln|fib|fibonacci)\s*\(', text_lower):
        return True
    
    # Check for Roman numerals - only if the ENTIRE first word/token is Roman numerals
    # This prevents "I am great" from being parsed but allows standalone "I" or "XV"
    # Match Roman numerals followed by space, end of string, or math operator
    # IMPORTANT: Use text_stripped (NOT text_lower) because Roman numerals must be uppercase
    first_roman_match = re.match(r'^([IVXLCDM]+)(?:\s|$|[+\-*/:()%^])', text_stripped)
    if first_roman_match:
        full_roman = first_roman_match.group(1)
        remaining_text = text_stripped[len(full_roman):]
        
        # Only consider it parseable if:
        # 1. It's the entire text (e.g., just "I" or "XV")
        # 2. It's followed immediately by a math operator (e.g., "X+2")
        # 3. It's NOT followed by regular words with a space (prevents "I am" from being parsed)
        
        if not remaining_text:  # Standalone Roman numeral
            if try_parse_roman_numeral(full_roman) is not None:
                return True
        elif remaining_text[0:1] in r'+-*/:()%^':  # Immediately followed by operator
            if try_parse_roman_numeral(full_roman) is not None:
                return True
        # If followed by space and then a word, check if it's a math operation
        elif remaining_text.startswith(' ') and len(remaining_text.strip()) > 0:
            # Check if what follows is an operator or number, not regular text
            next_part = remaining_text.strip()
            if re.match(r'^[+\-*/:()%^]', next_part) or re.match(r'^\d', next_part):
                if try_parse_roman_numeral(full_roman) is not None:
                    return True
            # Otherwise it's regular text like "I am", don't parse
    
    # Check if text starts with a word that could be a number
    # This handles cases like "ni-5", "tres+4", "zeven*3"
    first_word_match = re.match(r'^([a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+)', text_lower)
    
    if first_word_match:
        first_word = first_word_match.group(1)
        
        # Check if this first word is a number word (constant, multilang, ambiguous, or english)
        if first_word in MATH_CONSTANTS:
            return True
        
        # Check both regular multilang numbers AND ambiguous numbers
        if first_word in MULTILANG_NUMBERS or first_word in AMBIGUOUS_NUMBERS:
            return True
        
        try:
            w2n.word_to_num(first_word)
            return True
        except ValueError:
            pass
    
    # Also check for compound number words (like "twenty-one")
    first_token_match = re.match(r'^([a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+)+)', text_lower)
    
    if first_token_match:
        compound_word = first_token_match.group(1)
        
        # Check if it's a valid compound number word
        if compound_word in MULTILANG_NUMBERS:
            return True
        
        try:
            w2n.word_to_num(compound_word)
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
    # Check for operators that are clearly math (not hyphens in compound words)
    # First, check for any non-hyphen operators
    if re.search(r'[+*/:()%^]', text):
        return True
    
    # For hyphens, we need to be more careful
    # Check if there's a hyphen that's NOT part of a compound number word
    if '-' in text:
        # Split by spaces first
        parts = text.split()
        for part in parts:
            if '-' in part:
                # Check if this part is a valid compound word
                if not is_valid_compound_word(part):
                    # It has a hyphen but isn't a compound word - likely math
                    # But verify at least one side looks like a number
                    hyphen_parts = part.split('-')
                    for i, hp in enumerate(hyphen_parts):
                        # Check if this part is a number (digit or word)
                        if hp.isdigit():
                            return True
                        if hp.lower() in MULTILANG_NUMBERS or hp.lower() in AMBIGUOUS_NUMBERS:
                            return True
                        if hp.lower() in MATH_CONSTANTS:
                            return True
                        try:
                            w2n.word_to_num(hp.lower())
                            return True
                        except ValueError:
                            pass
    
    return False


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


def find_ambiguous_words_in_expression(text):
    """Find all ambiguous words in a mathematical expression."""
    text_lower = text.lower()
    found_ambiguous = []
    
    for word in AMBIGUOUS_NUMBERS.keys():
        # Use word boundary matching to find the word
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text_lower):
            found_ambiguous.append(word)
    
    return found_ambiguous


def generate_expression_variants(text, ambiguous_words):
    """
    Generate all possible variants of an expression by substituting
    different values for ambiguous words.
    Returns a list of (expression_text, languages_used) tuples.
    """
    if not ambiguous_words:
        return [(text, set())]
    
    variants = []
    
    # Get all combinations of ambiguous word values
    from itertools import product
    
    word_options = []
    for word in ambiguous_words:
        word_options.append([(word, value, langs) for value, langs in AMBIGUOUS_NUMBERS[word]])
    
    for combination in product(*word_options):
        variant_text = text.lower()
        combined_languages = set()
        
        for word, value, langs in combination:
            pattern = r'\b' + re.escape(word) + r'\b'
            variant_text = re.sub(pattern, str(value), variant_text, flags=re.IGNORECASE)
            combined_languages.update(langs)
        
        variants.append((variant_text, combined_languages))
    
    return variants


def extract_balanced_parentheses(text, start_pos):
    """
    Extract content within balanced parentheses starting at start_pos.
    start_pos should be the index of the opening '('.
    Returns (content_inside, end_pos) or (None, -1) if unbalanced.
    """
    if start_pos >= len(text) or text[start_pos] != '(':
        return None, -1
    
    depth = 0
    for i in range(start_pos, len(text)):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                # Found matching closing paren
                content = text[start_pos + 1:i]  # Content between ( and )
                return content, i
    
    return None, -1  # Unbalanced


def preprocess_inner_expression(text, expected_number=None):
    """
    Preprocess an expression to convert words and constants to numbers.
    Used for preprocessing content inside function parentheses like fib() and log().
    Does NOT handle fib/log functions themselves (to avoid recursion).
    
    Returns: (processed_text, languages_used)
    """
    languages_used = set()
    result = text
    
    # Process binary/hex first
    result, used_programmer = process_binary_hex(result)
    # Note: We don't track programmer type here, it's tracked at higher level
    
    result = result.replace('^', '**')
    result = result.replace(':', '/')
    
    # Replace sqrt
    def replace_sqrt(match):
        return f"({match.group(1)})**0.5"
    result = re.sub(r'sqrt\s*\(\s*([^)]+)\s*\)', replace_sqrt, result, flags=re.IGNORECASE)
    
    # Replace constants
    for constant, value in MATH_CONSTANTS.items():
        result = re.sub(r'\b' + re.escape(constant) + r'\b', str(value), result, flags=re.IGNORECASE)
    
    # Replace Roman numerals (CASE-SENSITIVE)
    roman_pattern = r'\b([IVXLCDM]+)\b'
    roman_matches_with_pos = [(m.group(), m.start(), m.end()) 
                               for m in re.finditer(roman_pattern, result)]
    
    for roman_text, start_pos, end_pos in reversed(roman_matches_with_pos):
        roman_value = try_parse_roman_numeral(roman_text)
        if roman_value is not None:
            result = result[:start_pos] + str(roman_value) + result[end_pos:]
            languages_used.add('la')
    
    # Replace ambiguous words with context
    for word in AMBIGUOUS_NUMBERS.keys():
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, result, re.IGNORECASE):
            multilang_result = try_parse_multilang_number(word, expected_number)
            if multilang_result:
                value, langs = multilang_result
                result = re.sub(pattern, str(value), result, flags=re.IGNORECASE)
                languages_used.update(langs)
    
    # Replace word numbers (multilang and English)
    words_with_pos = [(m.group(), m.start(), m.end()) 
                  for m in re.finditer(r'\b[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+)*\b', result)]

    for word, start_pos, end_pos in reversed(words_with_pos):
        multilang_result = try_parse_multilang_number(word.lower(), expected_number)
        if multilang_result is not None:
            num_val, langs = multilang_result
            result = result[:start_pos] + str(num_val) + result[end_pos:]
            languages_used.update(langs)
            continue
        
        try:
            number = w2n.word_to_num(word.lower())
            result = result[:start_pos] + str(number) + result[end_pos:]
            languages_used.add('en')
        except ValueError:
            continue
    
    return result, languages_used


def process_fibonacci_functions(text, expected_number=None):
    """
    Process fib(n) and fibonacci(n) functions in text.
    
    Handles:
    - fib(10) - simple integers
    - fib(een) - word numbers  
    - fib(two + 3) - expressions inside
    - fib(log2(huit)) - nested functions
    
    Returns: (processed_text, languages_used)
    """
    languages_collected = set()
    result = text
    
    # Keep processing until no more fib/fibonacci functions are found
    max_iterations = 10  # Safety limit
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        # Find fib( or fibonacci( 
        match = re.search(r'(?:fib|fibonacci)\s*\(', result, re.IGNORECASE)
        if not match:
            break
        
        func_start = match.start()
        paren_start = match.end() - 1  # Position of '('
        
        # Extract balanced content
        inner_content, paren_end = extract_balanced_parentheses(result, paren_start)
        if inner_content is None:
            break  # Unbalanced, stop processing
        
        # Process the inner content recursively (handles nested functions)
        processed_inner = inner_content
        
        # First, recursively process any nested fib/log functions
        processed_inner, nested_langs = process_fibonacci_functions(processed_inner, expected_number)
        languages_collected.update(nested_langs)
        
        processed_inner, nested_langs = process_log_functions(processed_inner, expected_number)
        languages_collected.update(nested_langs)
        
        # Now preprocess word numbers and evaluate
        try:
            # Try simple integer first
            n = int(processed_inner.strip())
        except ValueError:
            try:
                processed_inner, inner_langs = preprocess_inner_expression(processed_inner, expected_number)
                languages_collected.update(inner_langs)
                
                try:
                    n = int(round(evaluate_expression_safe(processed_inner)))
                except:
                    n = int(round(float(processed_inner.strip())))
            except:
                # Can't evaluate, skip this function call
                break
        
        fib_result = calculate_fibonacci(n)
        if fib_result is None:
            break
        
        # Replace the entire function call with the result
        result = result[:func_start] + str(fib_result) + result[paren_end + 1:]
    
    return result, languages_collected


def process_log_functions(text, expected_number=None):
    """
    Process log functions in text: log(), ln(), log10(), log2(), log(x,base).
    
    Handles word numbers, expressions, and nested functions inside the parentheses.
    
    Returns: (processed_text, languages_used)
    """
    languages_collected = set()
    result = text
    
    def preprocess_arg(arg_text):
        """Preprocess a function argument and return its numeric value."""
        nonlocal languages_collected
        arg_stripped = arg_text.strip()
        
        # First, recursively process any nested fib/log functions
        processed, nested_langs = process_fibonacci_functions(arg_stripped, expected_number)
        languages_collected.update(nested_langs)
        
        processed, nested_langs = process_log_functions(processed, expected_number)
        languages_collected.update(nested_langs)
        
        try:
            return float(processed)
        except ValueError:
            processed, langs = preprocess_inner_expression(processed, expected_number)
            languages_collected.update(langs)
            try:
                return float(evaluate_expression_safe(processed))
            except:
                return float(processed.strip())
    
    # Process each log function type
    # We need to handle them iteratively to deal with nested functions
    
    max_iterations = 10
    
    for _ in range(max_iterations):
        modified = False
        
        # Handle log with base: log(value, base)
        match = re.search(r'log\s*\(', result, re.IGNORECASE)
        if match:
            paren_start = match.end() - 1
            inner_content, paren_end = extract_balanced_parentheses(result, paren_start)
            
            if inner_content is not None and ',' in inner_content:
                # Split by comma - but be careful of nested functions with commas
                # Find the top-level comma
                depth = 0
                comma_pos = -1
                for i, ch in enumerate(inner_content):
                    if ch == '(':
                        depth += 1
                    elif ch == ')':
                        depth -= 1
                    elif ch == ',' and depth == 0:
                        comma_pos = i
                        break
                
                if comma_pos > 0:
                    try:
                        value_str = inner_content[:comma_pos]
                        base_str = inner_content[comma_pos + 1:]
                        value = preprocess_arg(value_str)
                        base = preprocess_arg(base_str)
                        
                        if value > 0 and base > 0 and base != 1:
                            log_result = math.log(value, base)
                            result = result[:match.start()] + str(log_result) + result[paren_end + 1:]
                            modified = True
                            continue
                    except:
                        pass
        
        # Handle ln(x)
        match = re.search(r'ln\s*\(', result, re.IGNORECASE)
        if match:
            paren_start = match.end() - 1
            inner_content, paren_end = extract_balanced_parentheses(result, paren_start)
            
            if inner_content is not None:
                try:
                    value = preprocess_arg(inner_content)
                    if value > 0:
                        log_result = math.log(value)
                        result = result[:match.start()] + str(log_result) + result[paren_end + 1:]
                        modified = True
                        continue
                except:
                    pass
        
        # Handle log10(x)
        match = re.search(r'log10\s*\(', result, re.IGNORECASE)
        if match:
            paren_start = match.end() - 1
            inner_content, paren_end = extract_balanced_parentheses(result, paren_start)
            
            if inner_content is not None:
                try:
                    value = preprocess_arg(inner_content)
                    if value > 0:
                        log_result = math.log10(value)
                        result = result[:match.start()] + str(log_result) + result[paren_end + 1:]
                        modified = True
                        continue
                except:
                    pass
        
        # Handle log2(x)
        match = re.search(r'log2\s*\(', result, re.IGNORECASE)
        if match:
            paren_start = match.end() - 1
            inner_content, paren_end = extract_balanced_parentheses(result, paren_start)
            
            if inner_content is not None:
                try:
                    value = preprocess_arg(inner_content)
                    if value > 0:
                        log_result = math.log2(value)
                        result = result[:match.start()] + str(log_result) + result[paren_end + 1:]
                        modified = True
                        continue
                except:
                    pass
        
        # Handle simple log(x) - defaults to base 10
        # Must check this AFTER log10/log2 to avoid conflicts
        match = re.search(r'log\s*\(', result, re.IGNORECASE)
        if match:
            paren_start = match.end() - 1
            inner_content, paren_end = extract_balanced_parentheses(result, paren_start)
            
            if inner_content is not None and ',' not in inner_content:
                try:
                    value = preprocess_arg(inner_content)
                    if value > 0:
                        log_result = math.log10(value)
                        result = result[:match.start()] + str(log_result) + result[paren_end + 1:]
                        modified = True
                        continue
                except:
                    pass
        
        if not modified:
            break
    
    return result, languages_collected


def preprocess_expression(text, expected_number=None):
    """Preprocess mathematical expression for evaluation."""
    languages_used = set()
    
    # Process binary/hex first
    text, used_programmer = process_binary_hex(text)
    if used_programmer:
        # We'll add 'programmer' type later in analyze_input_types
        pass
    
    text = text.replace('^', '**')
    text = text.replace(':', '/')
    
    # Process Fibonacci functions (handles word numbers and expressions inside)
    text, fib_langs = process_fibonacci_functions(text, expected_number)
    languages_used.update(fib_langs)
    
    # Process logarithm functions (handles word numbers and expressions inside)
    text, log_langs = process_log_functions(text, expected_number)
    languages_used.update(log_langs)
    
    def replace_sqrt(match):
        return f"({match.group(1)})**0.5"
    
    text = re.sub(r'sqrt\s*\(\s*([^)]+)\s*\)', replace_sqrt, text, flags=re.IGNORECASE)
    
    for constant, value in MATH_CONSTANTS.items():
        text = re.sub(r'\b' + re.escape(constant) + r'\b', str(value), text, flags=re.IGNORECASE)
    
    # Extract and replace Roman numerals (CASE-SENSITIVE - must find uppercase sequences)
    roman_pattern = r'\b([IVXLCDM]+)\b'
    roman_matches_with_pos = [(m.group(), m.start(), m.end()) 
                               for m in re.finditer(roman_pattern, text)]
    
    for roman_text, start_pos, end_pos in reversed(roman_matches_with_pos):
        roman_value = try_parse_roman_numeral(roman_text)
        if roman_value is not None:
            text = text[:start_pos] + str(roman_value) + text[end_pos:]
            languages_used.add('la')  # Latin
    
    # Handle ambiguous words with context
    for word in AMBIGUOUS_NUMBERS.keys():
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            # Get the best value based on context (this will be refined later)
            result = try_parse_multilang_number(word, expected_number)
            if result:
                value, langs = result
                text = re.sub(pattern, str(value), text, flags=re.IGNORECASE)
                languages_used.update(langs)
    
    words_with_pos = [(m.group(), m.start(), m.end()) 
                  for m in re.finditer(r'\b[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+)*\b', text)]

    for word, start_pos, end_pos in reversed(words_with_pos):
        multilang_result = try_parse_multilang_number(word.lower(), expected_number)
        if multilang_result is not None:
            num_val, langs = multilang_result
            text = text[:start_pos] + str(num_val) + text[end_pos:]
            languages_used.update(langs)
            continue
        
        try:
            number = w2n.word_to_num(word.lower())
            text = text[:start_pos] + str(number) + text[end_pos:]
            languages_used.add('en')
        except ValueError:
            continue
    
    return text, languages_used


def preprocess_expression_all_variants(text):
    """
    Preprocess a mathematical expression and return ALL possible variants
    when ambiguous words are present.
    Returns a list of (processed_text, languages_used) tuples.
    """
    # Find ambiguous words in the expression
    ambiguous_words = find_ambiguous_words_in_expression(text)
    
    # Generate all variants
    variants = generate_expression_variants(text, ambiguous_words)
    
    results = []
    for variant_text, ambiguous_langs in variants:
        # Now preprocess each variant (without the ambiguous words, since they're already replaced)
        languages_used = set(ambiguous_langs)
        
        processed = variant_text
        
        # Process binary/hex first
        processed, used_programmer = process_binary_hex(processed)
        
        processed = processed.replace('^', '**')
        processed = processed.replace(':', '/')
        
        # Process Fibonacci functions (handles word numbers and expressions inside)
        processed, fib_langs = process_fibonacci_functions(processed)
        languages_used.update(fib_langs)
        
        # Process logarithm functions (handles word numbers and expressions inside)
        processed, log_langs = process_log_functions(processed)
        languages_used.update(log_langs)
        
        def replace_sqrt(match):
            return f"({match.group(1)})**0.5"
        
        processed = re.sub(r'sqrt\s*\(\s*([^)]+)\s*\)', replace_sqrt, processed, flags=re.IGNORECASE)
        
        for constant, value in MATH_CONSTANTS.items():
            processed = re.sub(r'\b' + re.escape(constant) + r'\b', str(value), processed, flags=re.IGNORECASE)
        
        # Extract and replace Roman numerals
        roman_pattern = r'\b([IVXLCDM]+)\b'
        # Need to check original text for Roman numerals since variant_text is lowercase
        original_roman_matches = [(m.group(), m.start(), m.end()) 
                                   for m in re.finditer(roman_pattern, text)]
        
        for roman_text, _, _ in original_roman_matches:
            roman_value = try_parse_roman_numeral(roman_text)
            if roman_value is not None:
                processed = re.sub(r'\b' + roman_text.lower() + r'\b', str(roman_value), processed, flags=re.IGNORECASE)
                languages_used.add('la')
        
        # Replace remaining word numbers
        words_with_pos = [(m.group(), m.start(), m.end()) 
                      for m in re.finditer(r'\b[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+)*\b', processed)]

        for word, start_pos, end_pos in reversed(words_with_pos):
            multilang_result = try_parse_multilang_number(word.lower())
            if multilang_result is not None:
                num_val, langs = multilang_result
                processed = processed[:start_pos] + str(num_val) + processed[end_pos:]
                languages_used.update(langs)
                continue
            
            try:
                number = w2n.word_to_num(word.lower())
                processed = processed[:start_pos] + str(number) + processed[end_pos:]
                languages_used.add('en')
            except ValueError:
                continue
        
        results.append((processed, languages_used))
    
    return results


def normalize_expression_spacing(text):
    """
    Normalize spacing in expressions by adding spaces around operators.
    This helps with consistent parsing of expressions like "10+vier-tre".
    NOTE: This does NOT protect compound words - that's handled by generating
    multiple variants in get_all_possible_interpretations().
    """
    result = text
    
    # First, protect sqrt() and random() functions
    result = re.sub(r'sqrt\s*\(', 'SQRT_FUNC(', result, flags=re.IGNORECASE)
    result = re.sub(r'random\s*\(', 'RANDOM_FUNC(', result, flags=re.IGNORECASE)
    
    # Add spaces around operators (except inside function calls)
    # Handle + and * and / and : and ^ and %
    for op in ['+', '*', '/', ':', '^', '%']:
        result = result.replace(op, f' {op} ')
    
    # Handle minus/hyphen - add spaces around all hyphens
    result = re.sub(r'-', ' - ', result)
    
    # Restore functions
    result = result.replace('SQRT_FUNC(', 'sqrt(')
    result = result.replace('RANDOM_FUNC(', 'random(')
    
    # Clean up multiple spaces
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result


def extract_first_number_from_text(text, expected_number=None):
    """Extract the first valid number from text."""
    if has_math_operators(text):
        return None, None, set()
    
    found_numbers = []
    languages_used = set()
    current_pos = 0
    
    # Find digit numbers with their positions
    for match in re.finditer(r'\b(\d+)\b', text):
        found_numbers.append((int(match.group(1)), match.start(), 'digit', set()))
    
    # Find Roman numerals (CASE-SENSITIVE)
    for match in re.finditer(r'\b([IVXLCDM]+)\b', text):
        roman_value = try_parse_roman_numeral(match.group(1))
        if roman_value is not None:
            found_numbers.append((roman_value, match.start(), 'roman', {'la'}))
    
    # Find multilang numbers - now with all interpretations
    words = text.lower().split()
    for i, word in enumerate(words):
        clean_word = re.sub(r'[^\w\-]', '', word)
        
        # Get all possible interpretations
        all_interpretations = try_parse_multilang_number_all_interpretations(clean_word)
        if all_interpretations:
            word_pos = text.lower().find(word.lower(), current_pos)
            for multilang_num, langs in all_interpretations:
                found_numbers.append((multilang_num, word_pos, 'multilang', langs))
            current_pos = word_pos + len(word)
    
    # Try English word2number only if no multilang found
    if not any(entry[2] == 'multilang' for entry in found_numbers):
        current_pos = 0
        for i, word in enumerate(words):
            clean_word = re.sub(r'[^\w\-]', '', word)
            if '-' in clean_word and not is_valid_compound_word(clean_word):
                continue
            try:
                num = w2n.word_to_num(clean_word)
                word_pos = text.lower().find(word.lower(), current_pos)
                found_numbers.append((num, word_pos, 'english', {'en'}))
                current_pos = word_pos + len(word)
                break
            except ValueError:
                pass
    
    # Filter valid numbers
    valid_numbers = [(num, pos, typ, langs) for num, pos, typ, langs in found_numbers if num > 0]
    
    if valid_numbers:
        # If we have an expected number, prioritize matches
        if expected_number is not None:
            matching = [n for n in valid_numbers if n[0] == expected_number]
            if matching:
                matching.sort(key=lambda x: x[1])
                first_num, first_pos, first_type, first_langs = matching[0]
                return first_num, first_pos, first_langs
        
        valid_numbers.sort(key=lambda x: x[1])
        first_num, first_pos, first_type, first_langs = valid_numbers[0]
        return first_num, first_pos, first_langs
    
    return None, None, set()


def analyze_input_types(original_text):
    """Analyze and categorize the types of input in the text."""
    types = set()
    
    # Check for binary/hex notation
    if re.search(r'0x[0-9a-fA-F]+', original_text) or re.search(r'0b[01]+', original_text, re.IGNORECASE) or re.search(r'0o[0-7]+', original_text, re.IGNORECASE):
        types.add('programmer')
        types.add('math')
    
    # Check for Roman numerals
    if re.search(r'\b[IVXLCDM]+\b', original_text):
        # Verify it's actually a valid Roman numeral
        for match in re.finditer(r'\b([IVXLCDM]+)\b', original_text):
            if try_parse_roman_numeral(match.group(1)) is not None:
                types.add('roman')
                break
    
    if re.search(r'(\d+|[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅ]+)*)!', original_text):
        types.add('factorial')
        types.add('math')
    
    if re.search(r'[+\-*/:()%]', original_text):
        types.add('math')
    
    # Check for power/exponent operations (^ or **)
    if re.search(r'\^|\*\*', original_text):
        types.add('power')
        types.add('math')
    
    if re.search(r'sqrt\s*\(', original_text, re.IGNORECASE):
        types.add('sqrt')
        types.add('math')
    
    # Check for logarithm functions
    if re.search(r'(?:log|log10|log2|ln)\s*\(', original_text, re.IGNORECASE):
        types.add('log')
        types.add('math')
    
    # Check for Fibonacci functions
    if re.search(r'(?:fib|fibonacci)\s*\(', original_text, re.IGNORECASE):
        types.add('fibonacci')
        types.add('math')
    
    if re.search(r'random\s*\(', original_text, re.IGNORECASE):
        types.add('random')
    
    for constant in MATH_CONSTANTS:
        if re.search(r'\b' + re.escape(constant) + r'\b', original_text, re.IGNORECASE):
            types.add('constants')
            break
    
    words = re.findall(r'\b[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+(?:-[a-zA-ZÀ-ÿüğşıöçÖÇİĞÜŞøæåØÆÅぁ-んァ-ヶー一-龯]+)*\b', original_text)

    for word in words:
        # Check ambiguous numbers too
        if word.lower() in AMBIGUOUS_NUMBERS or try_parse_multilang_number(word.lower()) is not None:
            types.add('multilang')
            continue
        try:
            w2n.word_to_num(word.lower())
            # Note: 'text' type removed - no longer used
            break
        except ValueError:
            continue
    
    if re.search(r'\d+[.,]\d+', original_text):
        types.add('decimal')
    
    if not types and re.match(r'^\d+$', original_text.strip()):
        types.add('integer')
    
    return types


def can_be_hyphenated_math(text):
    """Check if hyphenated text could potentially be interpreted as math."""
    parts = text.split('-')
    if len(parts) >= 2:
        # Check if at least two adjacent parts are number words or digits
        for i in range(len(parts) - 1):
            first_part = parts[i].strip()
            second_part = parts[i + 1].strip()
            
            first_is_number = False
            second_is_number = False
            
            # Check first part
            if first_part.isdigit():
                first_is_number = True
            elif first_part.lower() in AMBIGUOUS_NUMBERS or try_parse_multilang_number(first_part) is not None:
                first_is_number = True
            else:
                try:
                    w2n.word_to_num(first_part)
                    first_is_number = True
                except:
                    pass
            
            # Check second part
            if second_part.isdigit():
                second_is_number = True
            elif second_part.lower() in AMBIGUOUS_NUMBERS or try_parse_multilang_number(second_part) is not None:
                second_is_number = True
            else:
                try:
                    w2n.word_to_num(second_part)
                    second_is_number = True
                except:
                    pass
            
            if first_is_number and second_is_number:
                return True
    
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


def get_all_possible_interpretations(text, expected_number=None):
    """Get all possible interpretations of the input text."""
    interpretations = []
    processed_text, random_values = process_random_functions(text)
    all_languages = set()
    
    # Check for binary/hex first
    processed_text, used_programmer = process_binary_hex(processed_text)
    
    # Check for Roman numerals first (before other processing)
    roman_match = re.match(r'^([IVXLCDM]+)(?:\s|$)', processed_text)
    if roman_match:
        roman_value = try_parse_roman_numeral(roman_match.group(1))
        if roman_value is not None and roman_value > 0:
            interpretations.append((roman_value, 'roman', f'Roman: {text} → {roman_value}', 
                                  random_values, {'la'}))
    
    # Check for ambiguous multilang numbers - add all interpretations
    clean_text = processed_text.strip().lower()
    all_multilang_interpretations = try_parse_multilang_number_all_interpretations(clean_text)
    for multilang_num, langs in all_multilang_interpretations:
        if multilang_num > 0:
            interpretations.append((multilang_num, 'multilang', 
                                  f'Multilang: {text} → {multilang_num}', 
                                  random_values, langs))
    
    # Find compound words in the expression
    compound_words_in_expr = find_compound_words_in_expression(processed_text)
    
    # Generate expression variants: with compounds preserved AND with compounds as math
    expression_variants = generate_compound_variants(processed_text, compound_words_in_expr)
    
    # Check if it could be interpreted as hyphenated math
    if '-' in processed_text and can_be_hyphenated_math(processed_text):
        for variant_text, variant_is_compound in expression_variants:
            # Normalize spacing
            normalized = normalize_expression_spacing(variant_text)
            
            # Generate all variants for ambiguous words
            all_variants = preprocess_expression_all_variants(normalized)
            
            for expr_processed, expr_languages in all_variants:
                try:
                    future = executor.submit(evaluate_expression_safe, process_factorials(expr_processed))
                    result = future.result(timeout=0.5)
                    
                    if result is not None and isinstance(result, (int, float)):
                        rounded = round(result)
                        if rounded > 0:
                            # Avoid duplicates
                            if not any(i[0] == rounded and i[1] == 'hyphenated_math' for i in interpretations):
                                interpretations.append((rounded, 'hyphenated_math', 
                                                      f'Hyphenated math: {text} → {rounded}', 
                                                      random_values, expr_languages))
                except:
                    pass
    
    # Check standard math expressions
    is_math_expression = (has_spaced_operators(processed_text) or 
                         has_unspaced_operators(processed_text) or 
                         '!' in text or 
                         'sqrt(' in processed_text.lower() or
                         re.search(r'(?:fib|fibonacci|log|log2|log10|ln)\s*\(', processed_text, re.IGNORECASE) or
                         used_programmer or
                         any(const in processed_text.lower() for const in MATH_CONSTANTS))
    
    if is_math_expression:
        for variant_text, variant_is_compound in expression_variants:
            # Normalize spacing
            normalized = normalize_expression_spacing(variant_text)
            
            # Generate all variants for ambiguous words
            all_variants = preprocess_expression_all_variants(normalized)
            
            for expr_processed, expr_languages in all_variants:
                try:
                    expr_with_factorials = process_factorials(expr_processed)
                    
                    future = executor.submit(evaluate_expression_safe, expr_with_factorials)
                    result = future.result(timeout=0.5)
                    
                    if result is not None and isinstance(result, (int, float)):
                        rounded = round(result)
                        if rounded > 0:
                            math_type = 'factorial_math' if '!' in text else 'math_expression'
                            # Avoid duplicates
                            if not any(i[0] == rounded and i[1] == math_type for i in interpretations):
                                interpretations.append((rounded, math_type, f'Math: {text} → {rounded}', 
                                                      random_values, expr_languages))
                except (concurrent.futures.TimeoutError, NumberTooHigh):
                    interpretations.append((None, 'evaluation_timeout', 
                                          'Calculation was too complex or took too long.', None, set()))
                    return interpretations
                except Exception:
                    pass
    
    # Try as compound word or written number
    if '-' not in processed_text or is_valid_compound_word(processed_text):
        try:
            for attempt_text in [processed_text, 
                                re.sub(r'\s+', ' ', processed_text.strip())]:
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
    
    # Try extraction if not a math expression (with expected_number for context)
    if not is_math_expression or not interpretations:
        extracted_info, _, extract_languages = extract_first_number_from_text(text, expected_number)
        if extracted_info and extracted_info > 0:
            # Avoid duplicate if already added via multilang
            if not any(i[0] == extracted_info and i[1] in ('multilang', 'extracted') for i in interpretations):
                interpretations.append((extracted_info, 'extracted', 
                                      f'Extracted: {text} → {extracted_info}', None, extract_languages))
        
        if clean_text in MATH_CONSTANTS:
            const_value = MATH_CONSTANTS[clean_text]
            rounded = round(const_value)
            if rounded > 0:
                interpretations.append((rounded, 'constant', f'Constant: {text} → {rounded}', 
                                      random_values, set()))
    
    return interpretations


def find_compound_words_in_expression(text):
    """Find all potential compound number words in an expression."""
    compound_words = []
    
    # Pattern to find word-word or word-word-word patterns
    pattern = r'\b([a-zA-ZÀ-ÿ]+(?:-[a-zA-ZÀ-ÿ]+)+)\b'
    
    for match in re.finditer(pattern, text, re.IGNORECASE):
        word = match.group(1)
        if is_valid_compound_word(word):
            compound_words.append(word)
    
    return compound_words


def generate_compound_variants(text, compound_words):
    """
    Generate variants of an expression where compound words can be either:
    1. Kept as compound words (e.g., "vingt-deux" = 22)
    2. Treated as math (e.g., "vingt-deux" = "vingt - deux" = 20 - 2 = 18)
    
    Returns a list of (variant_text, has_compounds) tuples.
    """
    if not compound_words:
        return [(text, False)]
    
    from itertools import product
    
    variants = []
    
    # For each compound word, we have two options: keep it or split it
    options_per_word = []
    for word in compound_words:
        # Option 1: Keep as compound (replace with its numeric value as placeholder)
        multilang_result = try_parse_multilang_number(word)
        if multilang_result:
            compound_value = multilang_result[0]
            options_per_word.append([
                (word, str(compound_value), True),   # Keep as compound
                (word, word, False)                   # Treat as math (will be split by normalize_expression_spacing)
            ])
        else:
            # Try English
            try:
                compound_value = w2n.word_to_num(word)
                options_per_word.append([
                    (word, str(compound_value), True),
                    (word, word, False)
                ])
            except ValueError:
                # Can't parse as compound, only math option
                options_per_word.append([(word, word, False)])
    
    # Generate all combinations
    for combination in product(*options_per_word):
        variant_text = text
        has_compound = False
        
        for original_word, replacement, is_compound in combination:
            if is_compound:
                has_compound = True
            # Replace the word with its replacement
            pattern = r'\b' + re.escape(original_word) + r'\b'
            variant_text = re.sub(pattern, replacement, variant_text, flags=re.IGNORECASE)
        
        # Avoid duplicate variants
        if not any(v[0] == variant_text for v in variants):
            variants.append((variant_text, has_compound))
    
    return variants

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
    
    # Check for simple binary/hex
    if re.match(r'^0x[0-9a-fA-F]+$', text):
        try:
            value = int(text, 16)
            if value > 0:
                return value, {'programmer'}, 'simple_hex', None, set()
        except ValueError:
            pass
    
    if re.match(r'^0b[01]+$', text, re.IGNORECASE):
        try:
            value = int(text, 2)
            if value > 0:
                return value, {'programmer'}, 'simple_binary', None, set()
        except ValueError:
            pass
    
    if re.match(r'^0o[0-7]+$', text, re.IGNORECASE):
        try:
            value = int(text, 8)
            if value > 0:
                return value, {'programmer'}, 'simple_octal', None, set()
        except ValueError:
            pass
    
    interpretations = get_all_possible_interpretations(text, expected_number)
    
    if not interpretations:
        return None, set(), 'no_valid_interpretation', None, set()
    
    if interpretations[0][1] == 'evaluation_timeout':
        return None, set(), 'evaluation_timeout', None, set()
    
    # CRITICAL: Check for context matches FIRST
    context_matches = [interp for interp in interpretations if interp[0] == expected_number]
    
    if context_matches:
        # When we have a context match, prioritize by type
        # 'multilang' and 'math_expression' should be high priority for context matches
        priority_order = ['multilang', 'math_expression', 'hyphenated_math', 'written', 'factorial_math', 
                         'extracted', 'constant', 'roman']
        
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


def parse_multiple_numbers_with_context(text, expected_start):
    """
    Parse up to 10 consecutive numbers from text.
    Returns: (list of numbers, combined_types, parse_method, random_info, languages, count)
    Returns None if parsing fails or numbers aren't consecutive.
    """
    text = text.strip()
    
    # Split by common delimiters while preserving math expressions
    # We need to be careful not to split math expressions like "3+2"
    parts = re.split(r'\s+', text)
    
    parsed_numbers = []
    all_types = set()
    all_languages = set()
    all_random_info = []
    
    current_expected = expected_start
    
    for i, part in enumerate(parts):
        if i >= 10:  # Limit to 10 numbers
            break
            
        part = part.strip()
        if not part:
            continue
        
        # Parse this part
        num, types, method, random_info, languages = parse_number_with_context(part, current_expected)
        
        # If parsing failed or number doesn't match expected
        if num is None or num != current_expected:
            # If we haven't parsed any numbers yet, this is a complete failure
            if not parsed_numbers:
                return None, set(), 'failed', None, set(), 0
            # Otherwise, we're done parsing consecutive numbers
            break
        
        # Valid consecutive number
        parsed_numbers.append(num)
        all_types.update(types)
        all_languages.update(languages)
        if random_info:
            all_random_info.extend(random_info)
        
        current_expected += 1
    
    if not parsed_numbers:
        return None, set(), 'failed', None, set(), 0
    
    # Add 'multiple' type if more than one number
    if len(parsed_numbers) > 1:
        all_types.add('multiple')
    
    return (parsed_numbers, all_types, 'multiple_consecutive' if len(parsed_numbers) > 1 else 'single', 
            all_random_info if all_random_info else None, all_languages, len(parsed_numbers))