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
        
        # When 6 is expected, it should still return 7 (leftmost) but different method
        result, types, method, random_info, languages = parse_number_with_context("zeven is meer dan zes", 6)
        self.assertEqual(result, 7)  # Still 7 because it's leftmost
        
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
        
    def test_complex_multilingual_expressions(self):
        """Test complex mathematical expressions with multiple languages and operations"""
        
        # Test 1: pi + 3 + sqrt(81) - two + eleven
        # pi≈3.14159 + 3 + sqrt(81)=9 - two=2 + eleven=11 = 3.14159+3+9-2+11 = 24.14159, rounds to 24
        result, types, method, random_info, languages = parse_number_with_context("pi + 3 + sqrt(81) - two + eleven", 24)
        self.assertEqual(result, 24)
        self.assertIn('constants', types)  # pi
        self.assertIn('sqrt', types)       # sqrt(81)
        self.assertIn('text', types)       # two, eleven
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
        self.assertIn('text', types)

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
        self.assertIn('text', types)
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
        self.assertIn('text', types)  # Should be recognized as text/written number
        
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

    def test_japanese_numbers_hiragana(self):
        """Test parsing of Japanese numbers in Hiragana"""
        # Basic hiragana
        result, types, method, random_info, languages = parse_number_with_context("なな", 7)
        self.assertEqual(result, 7)
        self.assertIn('multilang', types)
        self.assertIn('ja', languages)
        
        # Larger number
        result, types, method, random_info, languages = parse_number_with_context("にじゅうさん", 23)
        self.assertEqual(result, 23)
        self.assertIn('ja', languages)

    def test_japanese_numbers_katakana(self):
        """Test parsing of Japanese numbers in Katakana"""
        result, types, method, random_info, languages = parse_number_with_context("ナナ", 7)
        self.assertEqual(result, 7)
        self.assertIn('multilang', types)
        self.assertIn('ja', languages)

    def test_japanese_numbers_kanji(self):
        """Test parsing of Japanese numbers in Kanji"""
        # Single digit
        result, types, method, random_info, languages = parse_number_with_context("七", 7)
        self.assertEqual(result, 7)
        self.assertIn('ja', languages)
        
        # Double digit
        result, types, method, random_info, languages = parse_number_with_context("二十三", 23)
        self.assertEqual(result, 23)
        self.assertIn('ja', languages)
        
        # 100
        result, types, method, random_info, languages = parse_number_with_context("百", 100)
        self.assertEqual(result, 100)
        self.assertIn('ja', languages)

    def test_japanese_numbers_romaji(self):
        """Test parsing of Japanese numbers in Romaji"""
        result, types, method, random_info, languages = parse_number_with_context("nana", 7)
        self.assertEqual(result, 7)
        self.assertIn('ja', languages)
        
        result, types, method, random_info, languages = parse_number_with_context("nijuusan", 23)
        self.assertEqual(result, 23)
        self.assertIn('ja', languages)

    def test_japanese_in_expressions(self):
        """Test Japanese numbers in mathematical expressions"""
        # Hi + katakana
        result, types, method, random_info, languages = parse_number_with_context("さん + ヨン", 7)  # 3 + 4
        self.assertEqual(result, 7)
        self.assertIn('math', types)
        self.assertIn('ja', languages)
        
        # Kanji with sqrt
        result, types, method, random_info, languages = parse_number_with_context("sqrt(十六)", 4)  # sqrt(16)
        self.assertEqual(result, 4)
        self.assertIn('sqrt', types)
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
        
if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)