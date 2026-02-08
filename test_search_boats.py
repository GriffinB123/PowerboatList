"""
Unit tests for search_boats.py functions
"""
import unittest
from unittest.mock import Mock, patch
import json
from search_boats import filter_boats, extract_specs, generate_search_queries


class TestFilterBoats(unittest.TestCase):
    """Test the filter_boats function"""

    def test_filter_valid_boats(self):
        """Test filtering boats that meet criteria"""
        boats = [
            {'make': 'Boston Whaler', 'model': '130 Sport', 'length_ft': 13.5, 'max_hp': 40},
            {'make': 'Carolina Skiff', 'model': 'JVX 13', 'length_ft': 13.8, 'max_hp': 50},
            {'make': 'Too Small', 'model': 'Mini', 'length_ft': 12.0, 'max_hp': 50},
            {'make': 'Too Large', 'model': 'Huge', 'length_ft': 15.0, 'max_hp': 60},
            {'make': 'Too Weak', 'model': 'LowPower', 'length_ft': 13.7, 'max_hp': 30},
        ]

        result = filter_boats(boats)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['make'], 'Boston Whaler')
        self.assertEqual(result[1]['make'], 'Carolina Skiff')

    def test_filter_removes_duplicates(self):
        """Test that duplicate boats are removed"""
        boats = [
            {'make': 'Boston Whaler', 'model': '130 Sport', 'length_ft': 13.5, 'max_hp': 40},
            {'make': 'Boston Whaler', 'model': '130 Sport', 'length_ft': 13.5, 'max_hp': 40},
            {'make': 'boston whaler', 'model': '130 sport', 'length_ft': 13.5, 'max_hp': 40},
        ]

        result = filter_boats(boats)

        self.assertEqual(len(result), 1)

    def test_filter_boundary_conditions(self):
        """Test exact boundary lengths"""
        boats = [
            {'make': 'Test1', 'model': 'Min', 'length_ft': 13.5, 'max_hp': 40},
            {'make': 'Test2', 'model': 'Max', 'length_ft': 13.92, 'max_hp': 40},
            {'make': 'Test3', 'model': 'JustUnder', 'length_ft': 13.49, 'max_hp': 40},
            {'make': 'Test4', 'model': 'JustOver', 'length_ft': 13.93, 'max_hp': 40},
        ]

        result = filter_boats(boats)

        self.assertEqual(len(result), 2)
        self.assertIn('Min', [b['model'] for b in result])
        self.assertIn('Max', [b['model'] for b in result])

    def test_filter_handles_invalid_data(self):
        """Test handling of invalid or missing data"""
        boats = [
            {'make': 'Valid', 'model': 'Good', 'length_ft': 13.5, 'max_hp': 40},
            {'make': 'NoLength', 'model': 'Bad1', 'max_hp': 40},
            {'make': 'NoHP', 'model': 'Bad2', 'length_ft': 13.5},
            {'make': 'InvalidLength', 'model': 'Bad3', 'length_ft': 'thirteen', 'max_hp': 40},
        ]

        result = filter_boats(boats)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['model'], 'Good')


class TestGenerateSearchQueries(unittest.TestCase):
    """Test the generate_search_queries function"""

    @patch('search_boats.client')
    def test_generate_queries_with_claude(self, mock_client):
        """Test query generation with Claude API"""
        # Mock Claude response
        mock_response = Mock()
        mock_response.content = [Mock(text='["query1", "query2", "query3"]')]
        mock_client.messages.create.return_value = mock_response

        result = generate_search_queries("Boston Whaler")

        self.assertEqual(len(result), 3)
        self.assertIsInstance(result, list)

    @patch('search_boats.client', None)
    def test_generate_queries_fallback(self):
        """Test fallback when Claude is not available"""
        result = generate_search_queries("Boston Whaler")

        self.assertEqual(len(result), 3)
        self.assertTrue(all("Boston Whaler" in q for q in result))

    @patch('search_boats.client')
    def test_generate_queries_handles_json_with_code_blocks(self, mock_client):
        """Test handling of JSON wrapped in code blocks"""
        # Mock Claude response with code blocks
        mock_response = Mock()
        mock_response.content = [Mock(text='```json\n["query1", "query2"]\n```')]
        mock_client.messages.create.return_value = mock_response

        result = generate_search_queries("Test Manufacturer")

        self.assertEqual(len(result), 2)


class TestExtractSpecs(unittest.TestCase):
    """Test the extract_specs function"""

    @patch('search_boats.client')
    def test_extract_specs_valid_boat(self, mock_client):
        """Test extracting specs from valid text"""
        mock_response = Mock()
        mock_response.content = [Mock(text=json.dumps({
            'make': 'Boston Whaler',
            'model': '130 Sport',
            'length_ft': 13.5,
            'max_hp': 40
        }))]
        mock_client.messages.create.return_value = mock_response

        result = extract_specs("Some text about a Boston Whaler 130 Sport")

        self.assertIsNotNone(result)
        self.assertEqual(result['make'], 'Boston Whaler')
        self.assertEqual(result['length_ft'], 13.5)

    @patch('search_boats.client')
    def test_extract_specs_no_match(self, mock_client):
        """Test when no matching boat is found"""
        mock_response = Mock()
        mock_response.content = [Mock(text='null')]
        mock_client.messages.create.return_value = mock_response

        result = extract_specs("Text with no boat specs")

        self.assertIsNone(result)

    @patch('search_boats.client', None)
    def test_extract_specs_no_client(self):
        """Test behavior when Claude client is not available"""
        result = extract_specs("Some text")

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
