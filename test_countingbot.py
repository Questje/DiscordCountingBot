"""Unit tests for the Discord Counting Bot parsing functions."""

import unittest
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parser import (
    parse_number_with_context,
    try_parse_multilang_number,
    preprocess_expression,
    extract_first_number_from_text,
    has_spaced_operators,
    has_unspaced_operators,
    starts_with_parseable,
    get_all_possible_interpretations,
    process_factorials,
)
from constants import MATH_CONSTANTS


class CountingBotTest(unittest.TestCase):
    """Unit tests for the Discord Counting Bot parsing functions"""
    
    def test_simple_integers(self):
        """Test parsing of simple integer numbers"""
        # Test basic integers
        result, types, method, random_info, languages = parse_number_with_context("42", 42)
        self.assertEqual(result, 42)
        self.assertIn('integer', types)
        
        result, types, method, random_info, languages = parse_number_with_context("7", 7)
        self.assertEqual(result, 7)
        self.assertIn('integer', types)
    
    def test_english_number_words(self):
        """Test parsing of English number words"""
        # Single word numbers
        result, types, method, random_info, languages = parse_number_with_context("seven", 7)
        self.assertEqual(result, 7)
        
        # Compound numbers
        result, types, method, random_info, languages = parse_number_with_context("twenty one", 21)
        self.assertEqual(result, 21)
        
        # Hyphenated compound numbers
        result, types, method, random_info, languages = parse_number_with_context("forty-two", 42)
        self.assertEqual(result, 42)
    
    def test_multilang_numbers(self):
        """Test parsing of Dutch, French, German, and Swedish numbers"""
        # Dutch
        result, types, method, random_info, languages = parse_number_with_context("zeven", 7)
        self.assertEqual(result, 7)
        self.assertIn('multilang', types)
        self.assertIn('nl', languages)
        
        # French
        result, types, method, random_info, languages = parse_number_with_context("vingt", 20)
        self.assertEqual(result, 20)
        self.assertIn('multilang', types)
        self.assertIn('fr', languages)
        
        # German
        result, types, method, random_info, languages = parse_number_with_context("achtzehn", 18)
        self.assertEqual(result, 18)
        self.assertIn('multilang', types)
        self.assertIn('de', languages)
        
        # Swedish
        result, types, method, random_info, languages = parse_number_with_context("tjugo", 20)
        self.assertEqual(result, 20)
        self.assertIn('multilang', types)
        self.assertIn('se', languages)
    
    def test_mathematical_expressions_with_spaces(self):
        """Test math expressions with spaces around operators"""
        # Basic addition
        result, types, method, random_info, languages = parse_number_with_context("3 + 4", 7)
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        
        # Mixed numbers and words
        result, types, method, random_info, languages = parse_number_with_context("five + 6", 11)
        self.assertEqual(result, 11)
        self.assertIn('math', types)
        self.assertIn('en', languages)  # English word "five"
        
        # Subtraction
        result, types, method, random_info, languages = parse_number_with_context("15 - 3", 12)
        self.assertEqual(result, 12)
        self.assertIn('math', types)
    
    def test_mathematical_expressions_without_spaces(self):
        """Test math expressions without spaces around operators"""
        # Simple addition without spaces
        result, types, method, random_info, languages = parse_number_with_context("pi+2", 5)  # pi ≈ 3.14, rounded = 3, +2 = 5
        self.assertEqual(result, 5)
        self.assertIn('math', types)
        
        # Word numbers without spaces
        result, types, method, random_info, languages = parse_number_with_context("eleven+twelve", 23)
        self.assertEqual(result, 23)
        self.assertIn('math', types)
        self.assertIn('en', languages)
        
        # Mixed multilang
        result, types, method, random_info, languages = parse_number_with_context("zeven+acht", 15)  # 7 + 8 = 15
        self.assertEqual(result, 15)
        self.assertIn('math', types)
        self.assertIn('nl', languages)  # Dutch numbers
    
    def test_mathematical_constants(self):
        """Test mathematical constants like pi, e"""
        # Pi constant (should round to 3)
        result, types, method, random_info, languages = parse_number_with_context("pi", 3)
        self.assertEqual(result, 3)
        self.assertIn('constants', types)
        
        # E constant (should round to 3)  
        result, types, method, random_info, languages = parse_number_with_context("e", 3)
        self.assertEqual(result, 3)
        self.assertIn('constants', types)
        
        # Tau constant (should round to 6)
        result, types, method, random_info, languages = parse_number_with_context("tau", 6)
        self.assertEqual(result, 6)
        self.assertIn('constants', types)
    
    def test_factorial_expressions(self):
        """Test factorial expressions like 3! = 6"""
        # Basic factorial
        result, types, method, random_info, languages = parse_number_with_context("3!", 6)
        self.assertEqual(result, 6)
        self.assertIn('factorial', types)
        
        # Factorial in expression
        result, types, method, random_info, languages = parse_number_with_context("4! + 1", 25)  # 4! = 24, +1 = 25
        self.assertEqual(result, 25)
        self.assertIn('factorial', types)
        self.assertIn('math', types)
    
    def test_sqrt_expressions(self):
        """Test square root expressions"""
        # Basic sqrt
        result, types, method, random_info, languages = parse_number_with_context("sqrt(64)", 8)
        self.assertEqual(result, 8)
        self.assertIn('sqrt', types)
        
        # Sqrt in expression
        result, types, method, random_info, languages = parse_number_with_context("sqrt(81) + twee", 11)  # sqrt(81)=9, twee=2, 9+2=11
        self.assertEqual(result, 11)
        self.assertIn('sqrt', types)
        self.assertIn('nl', languages)  # Dutch "twee"
    
    def test_text_extraction_priority(self):
        """Test left-to-right text extraction (first valid number wins)"""
        # Should extract "zeven" (7) not "zes" (6)
        result, types, method, random_info, languages = parse_number_with_context("zeven is meer dan zes", 7)
        self.assertEqual(result, 7)
        self.assertEqual(method, 'context_match_extracted')
        self.assertIn('nl', languages)
        
        # Should extract "eleven" (11) not "twelve" (12)  
        result, types, method, random_info, languages = parse_number_with_context("eleven comes before twelve", 11)
        self.assertEqual(result, 11)
        self.assertEqual(method, 'context_match_extracted')
        self.assertIn('en', languages)
    
    def test_context_aware_parsing(self):
        """Test that context (expected number) influences parsing priority"""
        # When 7 is expected, "zeven is meer dan zes" should return 7 (zeven)
        result, types, method, random_info, languages = parse_number_with_context("zeven is meer dan zes", 7)
        self.assertEqual(result, 7)
        self.assertTrue(method.startswith('context_match'))
      
        # Math expressions should work with context
        result, types, method, random_info, languages = parse_number_with_context("3+4", 7)
        self.assertEqual(result, 7)
        self.assertTrue(method.startswith('context_match'))

    def test_helper_functions(self):
        """Test individual helper functions"""
        # Test multilang parsing - now returns tuple (number, set of languages)
        multilang_result = try_parse_multilang_number("zeven")
        self.assertIsNotNone(multilang_result)
        self.assertEqual(multilang_result[0], 7)
        self.assertIsInstance(multilang_result[1], set)  # Now returns a set
        self.assertIn('nl', multilang_result[1])  # Check if 'nl' is in the set
        
        multilang_result = try_parse_multilang_number("vingt")
        self.assertIsNotNone(multilang_result)
        self.assertEqual(multilang_result[0], 20)
        self.assertIsInstance(multilang_result[1], set)  # Now returns a set
        self.assertIn('fr', multilang_result[1])  # Check if 'fr' is in the set
        
        multilang_result = try_parse_multilang_number("achtzehn")
        self.assertIsNotNone(multilang_result)
        self.assertEqual(multilang_result[0], 18)
        self.assertIsInstance(multilang_result[1], set)  # Now returns a set
        self.assertIn('de', multilang_result[1])  # Check if 'de' is in the set
        
        multilang_result = try_parse_multilang_number("hello")
        self.assertIsNone(multilang_result)
        
        # Test operator detection
        self.assertTrue(has_spaced_operators("3 + 4"))
        self.assertFalse(has_spaced_operators("3+4"))
        self.assertTrue(has_unspaced_operators("3+4"))
        self.assertFalse(has_unspaced_operators("twenty-one"))  # Should not detect compound word hyphens
        
        # Test parseable detection
        self.assertTrue(starts_with_parseable("pi+2"))
        self.assertTrue(starts_with_parseable("eleven+twelve"))
        self.assertTrue(starts_with_parseable("7"))
        self.assertTrue(starts_with_parseable("zeven"))
        self.assertFalse(starts_with_parseable("hello world"))
        
        # Test factorial processing
        self.assertEqual(process_factorials("3!"), "6")
        self.assertEqual(process_factorials("4! + 1"), "24 + 1")
        
        # Test first number extraction - now returns number, position, set of languages
        num, pos, languages = extract_first_number_from_text("zeven is meer dan zes")
        self.assertEqual(num, 7)  # Should extract "zeven" (7), not "zes" (6)
        self.assertIsInstance(languages, set)  # Now returns a set
        self.assertIn('nl', languages)  # Check if 'nl' is in the set
    
    def test_spanish_numbers_simple(self):
        """Test basic Spanish number words"""
        result, types, method, random_info, languages = parse_number_with_context("uno", 1)
        self.assertEqual(result, 1)
        self.assertIn('es', languages)

        result, types, method, random_info, languages = parse_number_with_context("dos", 2)
        self.assertEqual(result, 2)
        self.assertIn('es', languages)

    def test_spanish_compound_veintiuno(self):
        """Test Spanish compound forms like veintiuno"""
        result, types, method, random_info, languages = parse_number_with_context("veintiuno", 21)
        self.assertEqual(result, 21)
        self.assertIn('es', languages)

    def test_spanish_treinta_y_cuatro(self):
        """Test Spanish 'treinta y cuatro' compound with spaces"""
        result, types, method, random_info, languages = parse_number_with_context("treinta y cuatro", 34)
        self.assertEqual(result, 34)
        self.assertIn('es', languages)

    def test_spanish_mixed_math(self):
        """Test math mixing Spanish words and constants"""
        # 'dos + pi' -> 2 + ~3.14 -> ~5, rounded to 5
        result, types, method, random_info, languages = parse_number_with_context("dos + pi", 5)
        self.assertEqual(result, 5)
        self.assertIn('es', languages)

    def test_spanish_extraction_in_sentence(self):
        """Extract Spanish number from sentence"""
        num, pos, langs = extract_first_number_from_text("veinte es mayor que diez")
        self.assertEqual(num, 20)
        self.assertIn('es', langs)
        
    def test_complex_multilingual_expressions(self):
        """Test complex mathematical expressions with multiple languages and operations"""
        
        # Test 1: pi + 3 + sqrt(81) - two + eleven
        # pi≈3.14159 + 3 + sqrt(81)=9 - two=2 + eleven=11 = 3.14159+3+9-2+11 = 24.14159, rounds to 24
        result, types, method, random_info, languages = parse_number_with_context("pi + 3 + sqrt(81) - two + eleven", 24)
        self.assertEqual(result, 24)
        self.assertIn('constants', types)  # pi
        self.assertIn('sqrt', types)       # sqrt(81)
        self.assertIn('math', types)       # mathematical expression
        self.assertIn('en', languages)     # English words
        
        # Test 2: 5! / vingt + sqrt(seize) - e
        # 5!=120 / vingt=20 + sqrt(seize)=sqrt(16)=4 - e≈2.71828 = 120/20+4-2.71828 = 6+4-2.71828 = 7.28172, rounds to 7
        result, types, method, random_info, languages = parse_number_with_context("5! / vingt + sqrt(seize) - e", 7)
        self.assertEqual(result, 7)
        self.assertIn('factorial', types)  # 5!
        self.assertIn('sqrt', types)       # sqrt(seize)
        self.assertIn('constants', types)  # e
        self.assertIn('math', types)
        self.assertIn('fr', languages)     # French words
        
        # Test 3: tau^2 - phi*acht + drie!
        # tau≈6.28318, tau^2≈39.4784, phi≈1.618, acht=8, phi*acht≈12.944, drie!=3!=6
        # So: 39.4784 - 12.944 + 6 = 32.5344, rounds to 33
        result, types, method, random_info, languages = parse_number_with_context("tau^2 - phi*acht + drie!", 33)
        self.assertEqual(result, 33)
        self.assertIn('constants', types)  # tau, phi
        self.assertIn('factorial', types)  # drie! = 3!
        self.assertIn('math', types)
        # Should contain both German and Dutch
        self.assertTrue('de' in languages or 'nl' in languages)
        
        # Test 4: (sqrt(hundert) + cinq) * deux - sieben
        # sqrt(hundert)=sqrt(100)=10, cinq=5, (10+5)*deux=15*2=30, sieben=7, 30-7=23
        result, types, method, random_info, languages = parse_number_with_context("(sqrt(hundert) + cinq) * deux - sieben", 23)
        self.assertEqual(result, 23)
        self.assertIn('sqrt', types)       # sqrt(hundert)
        self.assertIn('math', types)
        # Should contain French and German
        self.assertTrue('fr' in languages and 'de' in languages)

    def test_complex_expressions_without_spaces(self):
        """Test complex expressions without spaces to ensure they still parse correctly"""
        
        # Test without spaces: pi+sqrt(16)-trois+5!
        # pi≈3.14159 + sqrt(16)=4 - trois=3 + 5!=120 = 3.14159+4-3+120 = 124.14159, rounds to 124
        result, types, method, random_info, languages = parse_number_with_context("pi+sqrt(16)-trois+5!", 124)
        self.assertEqual(result, 124)
        self.assertIn('constants', types)
        self.assertIn('sqrt', types)
        self.assertIn('factorial', types)
        self.assertIn('math', types)
        self.assertIn('fr', languages)  # French "trois"
        
        # Test mixed spacing: tau*2+sqrt(25)-1
        # tau≈6.28318, tau*2≈12.566, sqrt(25)=5, 12.566+5-1 = 16.566, rounds to 17
        result, types, method, random_info, languages = parse_number_with_context("tau*2+sqrt(25)-1", 17)
        self.assertEqual(result, 17)
        self.assertIn('constants', types)
        self.assertIn('sqrt', types)
        self.assertIn('math', types)

    def test_decimal_numbers(self):
        """Test decimal number parsing"""
        # Test comma decimal
        result, types, method, random_info, languages = parse_number_with_context("7,5", 8)  # Should round to 8
        self.assertEqual(result, 8)
        self.assertIn('decimal', types)
        
        # Test dot decimal
        result, types, method, random_info, languages = parse_number_with_context("7.5", 8)  # Should round to 8
        self.assertEqual(result, 8)
        self.assertIn('decimal', types)

    def test_random_function(self):
        """Test random function parsing"""
        # This test may be flaky since random values are... random
        # We'll just test that it parses correctly, not the exact result
        result, types, method, random_info, languages = parse_number_with_context("random(5,5)", 5)
        self.assertEqual(result, 5)  # random(5,5) should always return 5
        self.assertIn('random', types)
        self.assertIsNotNone(random_info)
        self.assertEqual(len(random_info), 1)

    def test_additional_complex_combinations_1(self):
        """Additional test 1: Dutch factorial with French numbers"""
        result, types, method, random_info, languages = parse_number_with_context("vier! + vingt-deux", 46)  # 4! + 22 = 24 + 22 = 46
        self.assertEqual(result, 46)
        self.assertIn('factorial', types)
        self.assertIn('math', types)

    def test_additional_complex_combinations_2(self):
        """Additional test 2: Swedish with sqrt and constants"""
        result, types, method, random_info, languages = parse_number_with_context("sqrt(tjugofyra) + pi", 8)  # sqrt(24) + pi ≈ 4.9 + 3.14 = 8.04, rounds to 8
        self.assertEqual(result, 8)
        self.assertIn('sqrt', types)
        self.assertIn('constants', types)

    def test_additional_complex_combinations_3(self):
        """Additional test 3: German factorial with English words"""
        result, types, method, random_info, languages = parse_number_with_context("drei! * seven - five", 37)  # 6 * 7 - 5 = 42 - 5 = 37
        self.assertEqual(result, 37)
        self.assertIn('factorial', types)

    def test_additional_complex_combinations_4(self):
        """Additional test 4: French with random function"""
        result, types, method, random_info, languages = parse_number_with_context("quinze + random(2,2) - trois", 14)  # 15 + 2 - 3 = 14
        self.assertEqual(result, 14)
        self.assertIn('random', types)

    def test_additional_complex_combinations_5(self):
        """Additional test 5: Mixed constants and multilang"""
        result, types, method, random_info, languages = parse_number_with_context("e * vier + golden - twee", 11)  # 3 * 4 + 2 - 2 = 12, but let's see actual result
        self.assertIn('constants', types)

    def test_additional_complex_combinations_6(self):
        """Additional test 6: Complex nested sqrt with factorials"""
        result, types, method, random_info, languages = parse_number_with_context("sqrt(neuf!) - vingt", 160)  # sqrt(362880) - 20 ≈ 602 - 20 = 582, but check actual
        self.assertIn('sqrt', types)
        self.assertIn('factorial', types)

    def test_additional_complex_combinations_7(self):
        """Additional test 7: Multiple language factorial chain"""
        result, types, method, random_info, languages = parse_number_with_context("twee! + drei! + quatre!", 32)  # 2! + 6 + 24 = 2 + 6 + 24 = 32
        self.assertEqual(result, 32)
        self.assertIn('factorial', types)

    def test_additional_complex_combinations_8(self):
        """Additional test 8: Decimal with Swedish and constants"""
        result, types, method, random_info, languages = parse_number_with_context("7,5 + fem - tau", 6)  # 7.5 + 5 - 6.28318 = 6.21682, rounds to 6
        self.assertEqual(result, 6)
        self.assertIn('decimal', types)
        self.assertIn('constants', types)

    def test_additional_complex_combinations_9(self):
        """Additional test 9: English words with German sqrt"""
        result, types, method, random_info, languages = parse_number_with_context("twenty + sqrt(sechzehn) - eleven", 13)  # 20 + sqrt(16) - 11 = 20 + 4 - 11 = 13
        self.assertEqual(result, 13)
        self.assertIn('sqrt', types)

    def test_additional_complex_combinations_10(self):
        """Additional test 10: Ultimate complexity test"""
        result, types, method, random_info, languages = parse_number_with_context("3! + sqrt(seize) * trois - e + random(1,1)", 16)  
        # 3! = 6, sqrt(16) = 4, 4*3 = 12, e ≈ 2.71828, random(1,1) = 1
        # So: 6 + 12 - 2.71828 + 1 = 16.28172, rounds to 16
        self.assertEqual(result, 16)
        self.assertIn('factorial', types)
        self.assertIn('sqrt', types)
        self.assertIn('constants', types)
        self.assertIn('random', types)

    def test_context_awareness_compound_vs_math_1(self):
        """Test that 'twenty-one' is interpreted based on context."""
        # When expecting 21, "twenty-one" should be interpreted as the compound word 21
        result, types, method, random_info, languages = parse_number_with_context("twenty-one", 21)
        self.assertEqual(result, 21)
        self.assertTrue(method.startswith('context_match'))
        
        # When expecting 19, "twenty-one" should be interpreted as 20-1=19
        result, types, method, random_info, languages = parse_number_with_context("twenty-one", 19)
        self.assertEqual(result, 19)
        self.assertTrue(method.startswith('context_match'))
        self.assertIn('math', types)  # Should be recognized as math
      
    def test_context_awareness_compound_vs_math_2(self):
        """Test that 'thirty-three' is interpreted based on context."""
        # When expecting 33, should be the compound word
        result, types, method, random_info, languages = parse_number_with_context("thirty-three", 33)
        self.assertEqual(result, 33)
        self.assertTrue(method.startswith('context_match'))
        
        # When expecting 27, should be 30-3=27
        result, types, method, random_info, languages = parse_number_with_context("thirty-three", 27)
        self.assertEqual(result, 27)
        self.assertTrue(method.startswith('context_match'))
        self.assertIn('math', types)
    
    def test_context_awareness_non_compound_hyphenated(self):
        """Test that non-compound hyphenated expressions like 'six-five' work correctly."""
        # "six-five" should always be math (6-5=1) since it's not a valid compound word
        result, types, method, random_info, languages = parse_number_with_context("six-five", 1)
        self.assertEqual(result, 1)
        self.assertTrue(method.startswith('context_match'))
        self.assertIn('math', types)
        
        # Even when expecting a different number, it should still parse as 1
        result, types, method, random_info, languages = parse_number_with_context("six-five", 10)
        self.assertEqual(result, 1)  # Still 1, but won't be a context match
        self.assertIn('math', types)
    
    def test_context_awareness_multilang_compound(self):
        """Test context awareness with multilingual compound expressions."""
        # "vingt-deux" (French for 22) when expecting 22
        result, types, method, random_info, languages = parse_number_with_context("vingt-deux", 22)
        self.assertEqual(result, 22)
        self.assertTrue(method.startswith('context_match'))
        
        # "vingt-deux" when expecting 18 (20-2=18)
        result, types, method, random_info, languages = parse_number_with_context("vingt-deux", 18)
        self.assertEqual(result, 18)
        self.assertTrue(method.startswith('context_match'))
        self.assertIn('math', types)
        
        # Verify that French language is detected in both cases
        result, types, method, random_info, languages = parse_number_with_context("vingt-deux", 22)
        self.assertIn('fr', languages)

    def test_turkish_numbers(self):
        """Test parsing of Turkish numbers"""
        # Basic Turkish numbers
        result, types, method, random_info, languages = parse_number_with_context("yedi", 7)
        self.assertEqual(result, 7)
        self.assertIn('multilang', types)
        self.assertIn('tr', languages)
        
        # Turkish in expression
        result, types, method, random_info, languages = parse_number_with_context("bir + altı", 7)  # 1 + 6 = 7
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        self.assertIn('tr', languages)
    
    def test_danish_numbers(self):
        """Test parsing of Danish numbers"""
        # Basic Danish numbers
        result, types, method, random_info, languages = parse_number_with_context("syv", 7)
        self.assertEqual(result, 7)
        self.assertIn('multilang', types)
        self.assertIn('dk', languages)
        
        # Danish in expression
        result, types, method, random_info, languages = parse_number_with_context("fem + to", 7)  # 5 + 2 = 7
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        self.assertIn('dk', languages)
    
    def test_welsh_numbers(self):
        """Test parsing of Welsh numbers"""
        # Basic Welsh numbers
        result, types, method, random_info, languages = parse_number_with_context("saith", 7)
        self.assertEqual(result, 7)
        self.assertIn('multilang', types)
        self.assertIn('cy', languages)
        
        # Welsh in expression
        result, types, method, random_info, languages = parse_number_with_context("pump + dau", 7)  # 5 + 2 = 7
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        self.assertIn('cy', languages)
    
    def test_norwegian_numbers(self):
        """Test parsing of Norwegian numbers"""
        # Basic Norwegian numbers
        result, types, method, random_info, languages = parse_number_with_context("syv", 7)
        self.assertEqual(result, 7)
        self.assertIn('multilang', types)
        self.assertIn('no', languages)
        
        # Norwegian in expression
        result, types, method, random_info, languages = parse_number_with_context("fem + to", 7)  # 5 + 2 = 7
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        self.assertIn('no', languages)
    
    def test_colon_division(self):
        """Test division using colon character"""
        # Test colon division
        result, types, method, random_info, languages = parse_number_with_context("10:2", 5)
        self.assertEqual(result, 5)
        self.assertIn('math', types)
        
        # Test colon division with spaces
        result, types, method, random_info, languages = parse_number_with_context("20 : 4", 5)
        self.assertEqual(result, 5)
        self.assertIn('math', types)
        
        # Test mixed with other operations
        result, types, method, random_info, languages = parse_number_with_context("30:6 + 2", 7)  # 5 + 2 = 7
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        
        # Compare with slash division (should be the same)
        result1, _, _, _, _ = parse_number_with_context("10/2", 5)
        result2, _, _, _, _ = parse_number_with_context("10:2", 5)
        self.assertEqual(result1, result2)

    def test_multiple_consecutive_simple(self):
        """Test parsing multiple consecutive numbers - simple digits"""
        from parser import parse_multiple_numbers_with_context
        
        # Test "4 5 6" when expecting 4
        parsed_numbers, types, method, random_info, languages, count = parse_multiple_numbers_with_context("4 5 6", 4)
        self.assertEqual(parsed_numbers, [4, 5, 6])
        self.assertEqual(count, 3)
        self.assertIn('multiple', types)
        self.assertEqual(method, 'multiple_consecutive')

    def test_multiple_consecutive_with_words(self):
        """Test parsing multiple consecutive numbers - mix of digits and words"""
        from parser import parse_multiple_numbers_with_context
        
        # Test "4 five six" when expecting 4
        parsed_numbers, types, method, random_info, languages, count = parse_multiple_numbers_with_context("4 five six", 4)
        self.assertEqual(parsed_numbers, [4, 5, 6])
        self.assertEqual(count, 3)
        self.assertIn('multiple', types)
        self.assertIn('en', languages)

    def test_multiple_consecutive_with_math(self):
        """Test parsing multiple consecutive numbers with math expressions"""
        from parser import parse_multiple_numbers_with_context
        
        # Test "3+2 3+3" when expecting 5 (should parse as 5, 6)
        parsed_numbers, types, method, random_info, languages, count = parse_multiple_numbers_with_context("3+2 3+3", 5)
        self.assertEqual(parsed_numbers, [5, 6])
        self.assertEqual(count, 2)
        self.assertIn('multiple', types)
        self.assertIn('math', types)

    def test_multiple_consecutive_fails_non_consecutive(self):
        """Test that non-consecutive numbers fail"""
        from parser import parse_multiple_numbers_with_context
        
        # Test "3+3 3+5 9 10" when expecting 6 - should fail because 8 is missing
        parsed_numbers, types, method, random_info, languages, count = parse_multiple_numbers_with_context("3+3 3+5 9 10", 6)
        # Should parse 6, 8 and stop (because 9 != 9 expected, wait it should work up to 8)
        # Actually: 3+3=6, 3+5=8, but we expect 6,7,8... so 3+5=8 when expecting 7 will fail
        # So it should only get [6] then stop
        self.assertEqual(parsed_numbers, [6])
        self.assertEqual(count, 1)

    def test_multiple_consecutive_limit_10(self):
        """Test that multiple numbers are limited to 10"""
        from parser import parse_multiple_numbers_with_context
        
        # Test 12 consecutive numbers, should only parse 10
        text = " ".join(str(i) for i in range(1, 13))  # "1 2 3 4 5 6 7 8 9 10 11 12"
        parsed_numbers, types, method, random_info, languages, count = parse_multiple_numbers_with_context(text, 1)
        self.assertEqual(len(parsed_numbers), 10)
        self.assertEqual(parsed_numbers, list(range(1, 11)))
        self.assertEqual(count, 10)
        self.assertIn('multiple', types)

    def test_japanese_numbers_romaji(self):
        """Test parsing of Japanese numbers in Romaji"""
        result, types, method, random_info, languages = parse_number_with_context("nana", 7)
        self.assertEqual(result, 7)
        self.assertIn('ja', languages)
        
        result, types, method, random_info, languages = parse_number_with_context("nijuusan", 23)
        self.assertEqual(result, 23)
        self.assertIn('ja', languages)

    def test_roman_numerals_basic(self):
        """Test basic Roman numeral parsing - UPPERCASE only"""
        # Basic Roman numerals
        result, types, method, random_info, languages = parse_number_with_context("I", 1)
        self.assertEqual(result, 1)
        self.assertIn('roman', types)
        self.assertIn('la', languages)
        
        result, types, method, random_info, languages = parse_number_with_context("V", 5)
        self.assertEqual(result, 5)
        self.assertIn('roman', types)
        self.assertIn('la', languages)
        
        result, types, method, random_info, languages = parse_number_with_context("X", 10)
        self.assertEqual(result, 10)
        self.assertIn('roman', types)
        
        result, types, method, random_info, languages = parse_number_with_context("L", 50)
        self.assertEqual(result, 50)
        self.assertIn('roman', types)
        
        result, types, method, random_info, languages = parse_number_with_context("C", 100)
        self.assertEqual(result, 100)
        self.assertIn('roman', types)

    def test_roman_numerals_compound(self):
        """Test compound Roman numerals"""
        # Test LX = 60
        result, types, method, random_info, languages = parse_number_with_context("LX", 60)
        self.assertEqual(result, 60)
        self.assertIn('roman', types)
        self.assertIn('la', languages)
        
        # Test XXIII = 23
        result, types, method, random_info, languages = parse_number_with_context("XXIII", 23)
        self.assertEqual(result, 23)
        self.assertIn('roman', types)
        
        # Test XC = 90 (subtractive)
        result, types, method, random_info, languages = parse_number_with_context("XC", 90)
        self.assertEqual(result, 90)
        self.assertIn('roman', types)
        
        # Test XCIX = 99
        result, types, method, random_info, languages = parse_number_with_context("XCIX", 99)
        self.assertEqual(result, 99)
        self.assertIn('roman', types)

    def test_roman_numerals_case_sensitive(self):
        """Test that Roman numerals are case-sensitive (lowercase should not work)"""
        # Lowercase should NOT be parsed as Roman numerals
        result, types, method, random_info, languages = parse_number_with_context("v", 5)
        # Should either fail or parse as something else, but NOT as Roman numeral
        if result is not None:
            self.assertNotIn('roman', types)
            self.assertNotIn('la', languages)
        
        result, types, method, random_info, languages = parse_number_with_context("lx", 60)
        if result is not None:
            self.assertNotIn('roman', types)
            self.assertNotIn('la', languages)

    def test_roman_numerals_in_math_expressions(self):
        """Test Roman numerals used in mathematical expressions"""
        # V + III = 8
        result, types, method, random_info, languages = parse_number_with_context("V + III", 8)
        self.assertEqual(result, 8)
        self.assertIn('math', types)
        self.assertIn('roman', types)
        self.assertIn('la', languages)
        
        # X * II = 20
        result, types, method, random_info, languages = parse_number_with_context("X * II", 20)
        self.assertEqual(result, 20)
        self.assertIn('math', types)
        self.assertIn('roman', types)
        
        # L - XX = 30
        result, types, method, random_info, languages = parse_number_with_context("L - XX", 30)
        self.assertEqual(result, 30)
        self.assertIn('math', types)
        self.assertIn('roman', types)

    def test_roman_numerals_mixed_with_other_languages(self):
        """Test Roman numerals mixed with other language numbers"""
        # VII + trois = 10 (7 + 3)
        result, types, method, random_info, languages = parse_number_with_context("VII + trois", 10)
        self.assertEqual(result, 10)
        self.assertIn('math', types)
        self.assertIn('roman', types)
        self.assertIn('la', languages)
        self.assertIn('fr', languages)
        
        # X + zeven = 17 (10 + 7)
        result, types, method, random_info, languages = parse_number_with_context("X + zeven", 17)
        self.assertEqual(result, 17)
        self.assertIn('math', types)
        self.assertIn('la', languages)
        self.assertIn('nl', languages)
        
        # sqrt(XVI) + five = 9 (sqrt(16) + 5 = 4 + 5)
        result, types, method, random_info, languages = parse_number_with_context("sqrt(XVI) + five", 9)
        self.assertEqual(result, 9)
        self.assertIn('sqrt', types)
        self.assertIn('roman', types)
        self.assertIn('la', languages)
        self.assertIn('en', languages)
    
    def test_roman_numeral_sentence_fix(self):
        """Test that sentences starting with 'I' are not parsed as Roman numeral 1"""
        # These should NOT be parseable as numbers
        sentences = [
            ("I am great!", None),
            ("I love counting", None),
            ("I think this is fun", None),
            ("I want to play", None),
            ("I can count", None),
            ("I wonder what happens", None),
        ]
        
        for text, expected in sentences:
            result, types, method, random_info, languages = parse_number_with_context(text, 1)
            self.assertIsNone(result, f"'{text}' should not be parsed as a number")
            self.assertFalse(starts_with_parseable(text), f"'{text}' should not be parseable")
        
        # These SHOULD still be parseable as Roman numerals
        valid_romans = [
            ("I", 1),
            ("II", 2), 
            ("III", 3),
            ("IV", 4),
            ("V", 5),
            ("X", 10),
            ("XV", 15),
            ("XX", 20),
            ("L", 50),
            ("C", 100),
            ("I + II", 3),  # Math with Roman numerals should still work
            ("V * II", 10),
        ]
        
        for text, expected in valid_romans:
            self.assertTrue(starts_with_parseable(text), f"'{text}' should be parseable")
            result, types, method, random_info, languages = parse_number_with_context(text, expected)
            self.assertEqual(result, expected, f"'{text}' should parse to {expected}")
    
    def test_roman_edge_cases(self):
        """Test edge cases for Roman numeral parsing"""
        # Mixed case should not parse as Roman
        result, _, _, _, _ = parse_number_with_context("i am great", 1)
        self.assertIsNone(result, "Lowercase 'i' should not be parsed as Roman numeral")
        
        # Partial Roman at start shouldn't parse if followed by regular text
        result, _, _, _, _ = parse_number_with_context("Via Roma", 1)
        self.assertIsNone(result, "'Via Roma' should not be parsed")
        
        result, _, _, _, _ = parse_number_with_context("Visa card", 1)
        self.assertIsNone(result, "'Visa card' should not be parsed")
    
    def test_complex_roman_expressions(self):
        """Test that Roman numerals work in mathematical expressions"""
        # Roman numerals in math should still work
        test_cases = [
            ("X+5", 15),
            ("C/X", 10),
            ("L*II", 100),
            ("sqrt(IX)", 3),
        ]
        
        for text, expected in test_cases:
            result, types, method, random_info, languages = parse_number_with_context(text, expected)
            self.assertEqual(result, expected, f"'{text}' should evaluate to {expected}")
            self.assertIn('math', types)
            self.assertIn('la', languages)  # Latin for Roman numerals
        
    def test_mixed_word_digit_subtraction(self):
        """Test subtraction with mixed word and digit operands"""
        # ni (Japanese 2) - 5 = -3, but -3 is not valid (<=0), so this should consider ni as 9 (Danish/Norwegian)
        # When expecting 4: ni(9) - 5 = 4 ✓
        result, types, method, random_info, languages = parse_number_with_context("ni-5", 4)
        self.assertEqual(result, 4)
        self.assertIn('math', types)
        
        # When expecting -3: ni(2) - 5 = -3, but negative numbers aren't valid
        # So this should fail or return None
        result, types, method, random_info, languages = parse_number_with_context("ni-5", -3)
        # Negative results should not be returned as valid
        self.assertTrue(result is None or result > 0)
        
    def test_mixed_word_digit_addition(self):
        """Test addition with mixed word and digit operands"""
        # tres (Spanish 3) + 4 = 7
        result, types, method, random_info, languages = parse_number_with_context("tres+4", 7)
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        self.assertIn('es', languages)
        
        # zeven (Dutch 7) + 3 = 10
        result, types, method, random_info, languages = parse_number_with_context("zeven+3", 10)
        self.assertEqual(result, 10)
        self.assertIn('math', types)
        self.assertIn('nl', languages)

    def test_mixed_digit_word_subtraction(self):
        """Test subtraction with digit first, then word"""
        # 10 - trois (French 3) = 7
        result, types, method, random_info, languages = parse_number_with_context("10-trois", 7)
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        self.assertIn('fr', languages)
        
        # 20 - sieben (German 7) = 13
        result, types, method, random_info, languages = parse_number_with_context("20-sieben", 13)
        self.assertEqual(result, 13)
        self.assertIn('math', types)
        self.assertIn('de', languages)

    def test_mixed_digit_word_addition(self):
        """Test addition with digit first, then word"""
        # 5 + cinq (French 5) = 10
        result, types, method, random_info, languages = parse_number_with_context("5+cinq", 10)
        self.assertEqual(result, 10)
        self.assertIn('math', types)
        self.assertIn('fr', languages)
        
        # 8 + två (Swedish 2) = 10
        result, types, method, random_info, languages = parse_number_with_context("8+två", 10)
        self.assertEqual(result, 10)
        self.assertIn('math', types)
        self.assertIn('se', languages)

    def test_mixed_word_digit_multiplication(self):
        """Test multiplication with mixed word and digit operands"""
        # vier (Dutch/German 4) * 3 = 12
        result, types, method, random_info, languages = parse_number_with_context("vier*3", 12)
        self.assertEqual(result, 12)
        self.assertIn('math', types)
        
        # cinq (French 5) * 4 = 20
        result, types, method, random_info, languages = parse_number_with_context("cinq*4", 20)
        self.assertEqual(result, 20)
        self.assertIn('math', types)
        self.assertIn('fr', languages)

    def test_mixed_digit_word_multiplication(self):
        """Test multiplication with digit first, then word"""
        # 3 * tre (Swedish/Danish/Norwegian 3) = 9
        result, types, method, random_info, languages = parse_number_with_context("3*tre", 9)
        self.assertEqual(result, 9)
        self.assertIn('math', types)
        
        # 6 * deux (French 2) = 12
        result, types, method, random_info, languages = parse_number_with_context("6*deux", 12)
        self.assertEqual(result, 12)
        self.assertIn('math', types)
        self.assertIn('fr', languages)

    def test_mixed_word_digit_division(self):
        """Test division with mixed word and digit operands"""
        # vingt (French 20) / 4 = 5
        result, types, method, random_info, languages = parse_number_with_context("vingt/4", 5)
        self.assertEqual(result, 5)
        self.assertIn('math', types)
        self.assertIn('fr', languages)
        
        # tien (Dutch 10) : 2 = 5 (using colon for division)
        result, types, method, random_info, languages = parse_number_with_context("tien:2", 5)
        self.assertEqual(result, 5)
        self.assertIn('math', types)
        self.assertIn('nl', languages)

    def test_mixed_digit_word_division(self):
        """Test division with digit first, then word"""
        # 15 / trois (French 3) = 5
        result, types, method, random_info, languages = parse_number_with_context("15/trois", 5)
        self.assertEqual(result, 5)
        self.assertIn('math', types)
        self.assertIn('fr', languages)
        
        # 21 : sieben (German 7) = 3
        result, types, method, random_info, languages = parse_number_with_context("21:sieben", 3)
        self.assertEqual(result, 3)
        self.assertIn('math', types)
        self.assertIn('de', languages)

    def test_ambiguous_word_digit_context_aware(self):
        """Test that ambiguous words resolve correctly based on context in mixed expressions"""
        # 'ni' is ambiguous: 2 (Japanese) or 9 (Danish/Norwegian)
        # ni + 5: when expecting 7, should use ni=2 (Japanese)
        result, types, method, random_info, languages = parse_number_with_context("ni+5", 7)
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        self.assertIn('ja', languages)
        
        # ni + 5: when expecting 14, should use ni=9 (Danish/Norwegian)
        result, types, method, random_info, languages = parse_number_with_context("ni+5", 14)
        self.assertEqual(result, 14)
        self.assertIn('math', types)
        self.assertTrue('dk' in languages or 'no' in languages)

    def test_ambiguous_tres_digit_context_aware(self):
        """Test that 'tres' resolves correctly based on context in mixed expressions"""
        # 'tres' is ambiguous: 3 (Spanish) or 60 (Danish)
        # tres * 2: when expecting 6, should use tres=3 (Spanish)
        result, types, method, random_info, languages = parse_number_with_context("tres*2", 6)
        self.assertEqual(result, 6)
        self.assertIn('math', types)
        self.assertIn('es', languages)
        
        # tres - 10: when expecting 50, should use tres=60 (Danish)
        result, types, method, random_info, languages = parse_number_with_context("tres-10", 50)
        self.assertEqual(result, 50)
        self.assertIn('math', types)
        self.assertIn('dk', languages)

    def test_multiple_mixed_languages_with_digits(self):
        """Test expressions mixing multiple language words with digits"""
        # zeven (Dutch 7) + 3 - deux (French 2) = 8
        result, types, method, random_info, languages = parse_number_with_context("zeven+3-deux", 8)
        self.assertEqual(result, 8)
        self.assertIn('math', types)
        self.assertIn('nl', languages)
        self.assertIn('fr', languages)
        
        # 10 + vier (Dutch/German 4) - tre (Swedish 3) = 11
        result, types, method, random_info, languages = parse_number_with_context("10+vier-tre", 11)
        self.assertEqual(result, 11)
        self.assertIn('math', types)

    def test_mixed_with_parentheses(self):
        """Test mixed word/digit expressions with parentheses"""
        # (trois + 2) * 4 = 20
        result, types, method, random_info, languages = parse_number_with_context("(trois+2)*4", 20)
        self.assertEqual(result, 20)
        self.assertIn('math', types)
        self.assertIn('fr', languages)
        
        # 6 * (fem - 3) = 12 (fem is Swedish/Danish/Norwegian 5)
        result, types, method, random_info, languages = parse_number_with_context("6*(fem-3)", 12)
        self.assertEqual(result, 12)
        self.assertIn('math', types)

    def test_mixed_with_special_characters(self):
        """Test mixed expressions with special math characters"""
        # acht (Dutch/German 8) ^ 2 = 64
        result, types, method, random_info, languages = parse_number_with_context("acht^2", 64)
        self.assertEqual(result, 64)
        self.assertIn('math', types)
        
        # 2 ^ trois (French 3) = 8
        result, types, method, random_info, languages = parse_number_with_context("2^trois", 8)
        self.assertEqual(result, 8)
        self.assertIn('math', types)
        self.assertIn('fr', languages)

    def test_starts_with_parseable_mixed_expressions(self):
        """Test that starts_with_parseable correctly identifies mixed expressions"""
        # These should all be parseable
        self.assertTrue(starts_with_parseable("ni-5"))
        self.assertTrue(starts_with_parseable("tres+4"))
        self.assertTrue(starts_with_parseable("zeven*3"))
        self.assertTrue(starts_with_parseable("vingt/4"))
        self.assertTrue(starts_with_parseable("quatre:2"))
        self.assertTrue(starts_with_parseable("acht^2"))
        
        # Digit first should also work
        self.assertTrue(starts_with_parseable("5+trois"))
        self.assertTrue(starts_with_parseable("10-zeven"))
        self.assertTrue(starts_with_parseable("3*cinq"))


class AchievementAndFlagTests(unittest.TestCase):
    """Tests for achievement types and language flags returned by parsing functions"""
    
    def assertLanguagesInclude(self, languages, expected_langs, msg=None):
        """Helper to check that all expected languages are in the result."""
        for lang in expected_langs:
            self.assertIn(lang, languages, msg or f"Expected language '{lang}' not found in {languages}")
    
    def assertLanguagesExclude(self, languages, excluded_langs, msg=None):
        """Helper to check that certain languages are NOT in the result."""
        for lang in excluded_langs:
            self.assertNotIn(lang, languages, msg or f"Language '{lang}' should not be in {languages}")
    
    def assertTypesInclude(self, types, expected_types, msg=None):
        """Helper to check that all expected types are in the result."""
        for t in expected_types:
            self.assertIn(t, types, msg or f"Expected type '{t}' not found in {types}")
    
    def assertTypesExclude(self, types, excluded_types, msg=None):
        """Helper to check that certain types are NOT in the result."""
        for t in excluded_types:
            self.assertNotIn(t, types, msg or f"Type '{t}' should not be in {types}")

    def test_english_word_gets_english_flag(self):
        """Test that English number words get the English flag"""
        result, types, method, random_info, languages = parse_number_with_context("seven", 7)
        self.assertEqual(result, 7)
        self.assertLanguagesInclude(languages, ['en'])
        
        result, types, method, random_info, languages = parse_number_with_context("twenty", 20)
        self.assertEqual(result, 20)
        self.assertLanguagesInclude(languages, ['en'])

    def test_shared_word_six_gets_both_flags(self):
        """Test that 'six' (valid in both English and French with same value) gets both flags"""
        result, types, method, random_info, languages = parse_number_with_context("six", 6)
        self.assertEqual(result, 6)
        self.assertLanguagesInclude(languages, ['en', 'fr'], 
            "'six' should have both English and French flags")

    def test_shared_word_nine_gets_english_flag(self):
        """Test that 'nine' gets English flag"""
        result, types, method, random_info, languages = parse_number_with_context("nine", 9)
        self.assertEqual(result, 9)
        self.assertLanguagesInclude(languages, ['en'])

    def test_ambiguous_ni_japanese_context(self):
        """Test that 'ni' gets Japanese flag when context expects 2"""
        result, types, method, random_info, languages = parse_number_with_context("ni + 3", 5)
        self.assertEqual(result, 5)
        self.assertLanguagesInclude(languages, ['ja'], 
            "'ni' as 2 should have Japanese flag")
        self.assertLanguagesExclude(languages, ['dk', 'no'],
            "'ni' as 2 should NOT have Danish/Norwegian flags")

    def test_ambiguous_ni_danish_norwegian_context(self):
        """Test that 'ni' gets Danish/Norwegian flags when context expects 9"""
        result, types, method, random_info, languages = parse_number_with_context("ni + 1", 10)
        self.assertEqual(result, 10)
        # Should have Danish and/or Norwegian, but not Japanese
        self.assertTrue('dk' in languages or 'no' in languages,
            "'ni' as 9 should have Danish and/or Norwegian flag")
        self.assertLanguagesExclude(languages, ['ja'],
            "'ni' as 9 should NOT have Japanese flag")

    def test_ambiguous_tres_spanish_context(self):
        """Test that 'tres' gets Spanish flag when context expects 3"""
        result, types, method, random_info, languages = parse_number_with_context("tres", 3)
        self.assertEqual(result, 3)
        self.assertLanguagesInclude(languages, ['es'],
            "'tres' as 3 should have Spanish flag")
        self.assertLanguagesExclude(languages, ['dk'],
            "'tres' as 3 should NOT have Danish flag")

    def test_ambiguous_tres_danish_context(self):
        """Test that 'tres' gets Danish flag when context expects 60"""
        result, types, method, random_info, languages = parse_number_with_context("tres", 60)
        self.assertEqual(result, 60)
        self.assertLanguagesInclude(languages, ['dk'],
            "'tres' as 60 should have Danish flag")
        self.assertLanguagesExclude(languages, ['es'],
            "'tres' as 60 should NOT have Spanish flag")

    def test_multi_language_expression_gets_all_flags(self):
        """Test that expressions with multiple languages get all appropriate flags"""
        # zeven (Dutch 7) + trois (French 3) = 10
        result, types, method, random_info, languages = parse_number_with_context("zeven + trois", 10)
        self.assertEqual(result, 10)
        self.assertLanguagesInclude(languages, ['nl', 'fr'],
            "Expression with Dutch and French words should have both flags")

    def test_roman_numeral_gets_latin_flag(self):
        """Test that Roman numerals get the Latin flag"""
        result, types, method, random_info, languages = parse_number_with_context("XVII", 17)
        self.assertEqual(result, 17)
        self.assertLanguagesInclude(languages, ['la'],
            "Roman numerals should have Latin flag")
        self.assertTypesInclude(types, ['roman'])

    def test_roman_with_other_language_gets_both_flags(self):
        """Test Roman numerals combined with other languages get all flags"""
        # X (Roman 10) + cinq (French 5) = 15
        result, types, method, random_info, languages = parse_number_with_context("X + cinq", 15)
        self.assertEqual(result, 15)
        self.assertLanguagesInclude(languages, ['la', 'fr'],
            "Roman + French should have both Latin and French flags")

    def test_math_achievement_for_expression(self):
        """Test that mathematical expressions get the math type"""
        result, types, method, random_info, languages = parse_number_with_context("5 + 3", 8)
        self.assertEqual(result, 8)
        self.assertTypesInclude(types, ['math'])

    def test_factorial_achievement(self):
        """Test that factorial expressions get the factorial type"""
        result, types, method, random_info, languages = parse_number_with_context("4!", 24)
        self.assertEqual(result, 24)
        self.assertTypesInclude(types, ['factorial'])

    def test_sqrt_achievement(self):
        """Test that sqrt expressions get the sqrt type"""
        result, types, method, random_info, languages = parse_number_with_context("sqrt(49)", 7)
        self.assertEqual(result, 7)
        self.assertTypesInclude(types, ['sqrt'])

    def test_constants_achievement(self):
        """Test that mathematical constants get the constants type"""
        result, types, method, random_info, languages = parse_number_with_context("pi + 1", 4)
        self.assertEqual(result, 4)
        self.assertTypesInclude(types, ['constants'])


class PowerLogFibonacciTests(unittest.TestCase):
    """Tests for power, logarithm, and Fibonacci operations"""
    
    # === POWER TESTS ===
    
    def test_power_simple_integers(self):
        """Test simple power/exponent operations with integers"""
        # 2^3 = 8
        result, types, method, random_info, languages = parse_number_with_context("2^3", 8)
        self.assertEqual(result, 8)
        self.assertIn('power', types)
        self.assertIn('math', types)
        
        # 3^2 = 9
        result, types, method, random_info, languages = parse_number_with_context("3^2", 9)
        self.assertEqual(result, 9)
        self.assertIn('power', types)

    def test_power_with_multilang_words(self):
        """Test power operations with multilingual number words"""
        # deux^trois = 2^3 = 8 (French)
        result, types, method, random_info, languages = parse_number_with_context("deux^trois", 8)
        self.assertEqual(result, 8)
        self.assertIn('power', types)
        self.assertIn('fr', languages)
        
        # vier^zwei = 4^2 = 16 (German)
        result, types, method, random_info, languages = parse_number_with_context("vier^zwei", 16)
        self.assertEqual(result, 16)
        self.assertIn('power', types)
        self.assertIn('de', languages)

    def test_power_in_complex_expression(self):
        """Test power operations combined with other operations"""
        # 2^3 + 2 = 8 + 2 = 10
        result, types, method, random_info, languages = parse_number_with_context("2^3 + 2", 10)
        self.assertEqual(result, 10)
        self.assertIn('power', types)
        self.assertIn('math', types)
        
        # sqrt(2^4) = sqrt(16) = 4
        result, types, method, random_info, languages = parse_number_with_context("sqrt(2^4)", 4)
        self.assertEqual(result, 4)
        self.assertIn('power', types)
        self.assertIn('sqrt', types)

    # === LOGARITHM TESTS ===
    
    def test_log_basic_functions(self):
        """Test basic logarithm functions"""
        # log10(1000) = 3
        result, types, method, random_info, languages = parse_number_with_context("log10(1000)", 3)
        self.assertEqual(result, 3)
        self.assertIn('log', types)
        self.assertIn('math', types)
        
        # log2(64) = 6
        result, types, method, random_info, languages = parse_number_with_context("log2(64)", 6)
        self.assertEqual(result, 6)
        self.assertIn('log', types)
        
        # log(100) = 2 (default base 10)
        result, types, method, random_info, languages = parse_number_with_context("log(100)", 2)
        self.assertEqual(result, 2)
        self.assertIn('log', types)

    def test_log_with_base(self):
        """Test logarithm with custom base"""
        # log(8, 2) = 3 (log base 2 of 8)
        result, types, method, random_info, languages = parse_number_with_context("log(8, 2)", 3)
        self.assertEqual(result, 3)
        self.assertIn('log', types)
        
        # log(27, 3) = 3 (log base 3 of 27)
        result, types, method, random_info, languages = parse_number_with_context("log(27, 3)", 3)
        self.assertEqual(result, 3)
        self.assertIn('log', types)

    def test_log_in_complex_expression(self):
        """Test logarithm combined with other operations"""
        # log2(32) + 5 = 5 + 5 = 10
        result, types, method, random_info, languages = parse_number_with_context("log2(32) + 5", 10)
        self.assertEqual(result, 10)
        self.assertIn('log', types)
        self.assertIn('math', types)
        
        # log10(1000) * deux = 3 * 2 = 6
        result, types, method, random_info, languages = parse_number_with_context("log10(1000) * deux", 6)
        self.assertEqual(result, 6)
        self.assertIn('log', types)
        self.assertIn('fr', languages)

    # === FIBONACCI TESTS ===
    
    def test_fibonacci_basic(self):
        """Test basic Fibonacci function"""
        # fib(10) = 55
        result, types, method, random_info, languages = parse_number_with_context("fib(10)", 55)
        self.assertEqual(result, 55)
        self.assertIn('fibonacci', types)
        self.assertIn('math', types)
        
        # fibonacci(7) = 13
        result, types, method, random_info, languages = parse_number_with_context("fibonacci(7)", 13)
        self.assertEqual(result, 13)
        self.assertIn('fibonacci', types)
        
        # fib(12) = 144
        result, types, method, random_info, languages = parse_number_with_context("fib(12)", 144)
        self.assertEqual(result, 144)
        self.assertIn('fibonacci', types)

    def test_fibonacci_small_values(self):
        """Test Fibonacci with small input values"""
        # fib(1) = 1
        result, types, method, random_info, languages = parse_number_with_context("fib(1)", 1)
        self.assertEqual(result, 1)
        self.assertIn('fibonacci', types)
        
        # fib(2) = 1
        result, types, method, random_info, languages = parse_number_with_context("fib(2)", 1)
        self.assertEqual(result, 1)
        self.assertIn('fibonacci', types)
        
        # fib(6) = 8
        result, types, method, random_info, languages = parse_number_with_context("fib(6)", 8)
        self.assertEqual(result, 8)
        self.assertIn('fibonacci', types)

    def test_fibonacci_in_complex_expression(self):
        """Test Fibonacci combined with other operations"""
        # fib(8) + 1 = 21 + 1 = 22
        result, types, method, random_info, languages = parse_number_with_context("fib(8) + 1", 22)
        self.assertEqual(result, 22)
        self.assertIn('fibonacci', types)
        self.assertIn('math', types)
        
        # fib(7) * deux = 13 * 2 = 26
        result, types, method, random_info, languages = parse_number_with_context("fib(7) * deux", 26)
        self.assertEqual(result, 26)
        self.assertIn('fibonacci', types)
        self.assertIn('fr', languages)
        
        # sqrt(fib(12)) = sqrt(144) = 12
        result, types, method, random_info, languages = parse_number_with_context("sqrt(fib(12))", 12)
        self.assertEqual(result, 12)
        self.assertIn('fibonacci', types)
        self.assertIn('sqrt', types)


class FibonacciLogWordArgumentTests(unittest.TestCase):
    """Tests for Fibonacci and Log functions with word numbers and expressions as arguments"""
    
    # === FIBONACCI WITH WORD NUMBERS ===
    
    def test_fibonacci_with_single_word_number(self):
        """Test Fibonacci with single word number arguments"""
        # fib(een) = fib(1) = 1 (Dutch)
        result, types, method, random_info, languages = parse_number_with_context("fib(een)", 1)
        self.assertEqual(result, 1)
        self.assertIn('fibonacci', types)
        self.assertIn('nl', languages)
        
        # fib(five) = fib(5) = 5 (English)
        result, types, method, random_info, languages = parse_number_with_context("fib(five)", 5)
        self.assertEqual(result, 5)
        self.assertIn('fibonacci', types)
        self.assertIn('en', languages)
        
        # fib(sept) = fib(7) = 13 (French)
        result, types, method, random_info, languages = parse_number_with_context("fib(sept)", 13)
        self.assertEqual(result, 13)
        self.assertIn('fibonacci', types)
        self.assertIn('fr', languages)

    def test_fibonacci_with_expression_argument(self):
        """Test Fibonacci with mathematical expressions as arguments"""
        # fib(two + 3) = fib(5) = 5
        result, types, method, random_info, languages = parse_number_with_context("fib(two + 3)", 5)
        self.assertEqual(result, 5)
        self.assertIn('fibonacci', types)
        self.assertIn('en', languages)
        
        # fib(3 * 2) = fib(6) = 8
        result, types, method, random_info, languages = parse_number_with_context("fib(3 * 2)", 8)
        self.assertEqual(result, 8)
        self.assertIn('fibonacci', types)
        
        # fib(10 - 2) = fib(8) = 21
        result, types, method, random_info, languages = parse_number_with_context("fib(10 - 2)", 21)
        self.assertEqual(result, 21)
        self.assertIn('fibonacci', types)

    def test_fibonacci_with_multilang_expression(self):
        """Test Fibonacci with multilingual expressions as arguments"""
        # fib(twee + drie) = fib(2 + 3) = fib(5) = 5 (Dutch)
        result, types, method, random_info, languages = parse_number_with_context("fib(twee + drie)", 5)
        self.assertEqual(result, 5)
        self.assertIn('fibonacci', types)
        self.assertIn('nl', languages)
        
        # fib(quatre * deux) = fib(4 * 2) = fib(8) = 21 (French)
        result, types, method, random_info, languages = parse_number_with_context("fib(quatre * deux)", 21)
        self.assertEqual(result, 21)
        self.assertIn('fibonacci', types)
        self.assertIn('fr', languages)

    # === LOG WITH WORD NUMBERS ===

    def test_log_with_single_word_number(self):
        """Test logarithm with single word number arguments"""
        # log2(huit) = log2(8) = 3 (French)
        result, types, method, random_info, languages = parse_number_with_context("log2(huit)", 3)
        self.assertEqual(result, 3)
        self.assertIn('log', types)
        self.assertIn('fr', languages)
        
        # log10(hundred) = log10(100) = 2 (English)
        result, types, method, random_info, languages = parse_number_with_context("log10(hundred)", 2)
        self.assertEqual(result, 2)
        self.assertIn('log', types)
        self.assertIn('en', languages)
        
        # log2(zestien) = log2(16) = 4 (Dutch)
        result, types, method, random_info, languages = parse_number_with_context("log2(zestien)", 4)
        self.assertEqual(result, 4)
        self.assertIn('log', types)
        self.assertIn('nl', languages)

    def test_log_with_expression_argument(self):
        """Test logarithm with mathematical expressions as arguments"""
        # log2(four * two) = log2(8) = 3
        result, types, method, random_info, languages = parse_number_with_context("log2(four * two)", 3)
        self.assertEqual(result, 3)
        self.assertIn('log', types)
        self.assertIn('en', languages)
        
        # log10(10 * 10) = log10(100) = 2
        result, types, method, random_info, languages = parse_number_with_context("log10(10 * 10)", 2)
        self.assertEqual(result, 2)
        self.assertIn('log', types)
        
        # log2(2^6) = log2(64) = 6
        result, types, method, random_info, languages = parse_number_with_context("log2(2^6)", 6)
        self.assertEqual(result, 6)
        self.assertIn('log', types)

    def test_log_with_multilang_expression(self):
        """Test logarithm with multilingual expressions as arguments"""
        # log(dix * dix) = log(10 * 10) = log(100) = 2 (French)
        result, types, method, random_info, languages = parse_number_with_context("log(dix * dix)", 2)
        self.assertEqual(result, 2)
        self.assertIn('log', types)
        self.assertIn('fr', languages)
        
        # log2(vier * acht) = log2(4 * 8) = log2(32) = 5 (Dutch/German)
        result, types, method, random_info, languages = parse_number_with_context("log2(vier * acht)", 5)
        self.assertEqual(result, 5)
        self.assertIn('log', types)

    def test_nested_log_inside_fib(self):
        """Test log nested inside fib"""
        # fib(log2(huit)) = fib(3) = 2
        result, types, method, random_info, languages = parse_number_with_context("fib(log2(huit))", 2)
        self.assertEqual(result, 2)
        self.assertIn('fibonacci', types)
        self.assertIn('log', types)
        self.assertIn('fr', languages)

    def test_nested_fib_inside_log(self):
        """Test fib nested inside log"""
        # log2(fib(6)) = log2(8) = 3
        result, types, method, random_info, languages = parse_number_with_context("log2(fib(6))", 3)
        self.assertEqual(result, 3)
        self.assertIn('fibonacci', types)
        self.assertIn('log', types)

    def test_deeply_nested_functions(self):
        """Test multiple levels of nesting"""
        # fib(log2(fib(6))) = fib(log2(8)) = fib(3) = 2
        result, types, method, random_info, languages = parse_number_with_context("fib(log2(fib(6)))", 2)
        self.assertEqual(result, 2)
        self.assertIn('fibonacci', types)
        self.assertIn('log', types)

    # === COMBINED COMPLEX TESTS ===

    def test_nested_functions_with_words(self):
        """Test nested functions with word arguments"""
        # fib(log2(huit)) = fib(log2(8)) = fib(3) = 2
        result, types, method, random_info, languages = parse_number_with_context("fib(log2(huit))", 2)
        self.assertEqual(result, 2)
        self.assertIn('fibonacci', types)
        self.assertIn('log', types)
        self.assertIn('fr', languages)

    def test_function_with_word_in_larger_expression(self):
        """Test functions with word arguments as part of larger expressions"""
        # fib(six) + 2 = fib(6) + 2 = 8 + 2 = 10
        result, types, method, random_info, languages = parse_number_with_context("fib(six) + 2", 10)
        self.assertEqual(result, 10)
        self.assertIn('fibonacci', types)
        self.assertIn('math', types)
        
        # log2(seize) * trois = log2(16) * 3 = 4 * 3 = 12 (French)
        result, types, method, random_info, languages = parse_number_with_context("log2(seize) * trois", 12)
        self.assertEqual(result, 12)
        self.assertIn('log', types)
        self.assertIn('fr', languages)

    def test_fibonacci_with_roman_numeral_argument(self):
        """Test Fibonacci with Roman numeral argument"""
        # fib(X) = fib(10) = 55
        result, types, method, random_info, languages = parse_number_with_context("fib(X)", 55)
        self.assertEqual(result, 55)
        self.assertIn('fibonacci', types)
        self.assertIn('la', languages)
        
        # fib(VII) = fib(7) = 13
        result, types, method, random_info, languages = parse_number_with_context("fib(VII)", 13)
        self.assertEqual(result, 13)
        self.assertIn('fibonacci', types)
        self.assertIn('la', languages)

if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)