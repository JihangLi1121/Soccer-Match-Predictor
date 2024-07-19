import unittest
from matchday_calendar import (
    extract_tables_from_pdf, clean_date, clean_and_split_tables,
    filter_bundesliga_matches
)

class TestMatchdayCalendar(unittest.TestCase):
    """Unit tests for matchday_calendar functions."""



    def test_extract_tables_from_pdf(self):

        """Test extracting tables from a sample PDF.
        
        This test checks if tables can be correctly extracted from a given PDF file.
        """


        # Test with a sample PDF path
        pdf_path = '/Users/joathcarrera/Desktop/CSE115A/Soccer-Match-Predictor/2425_Calendars/Bundesliga_Calendar_2023_2024.pdf'
        tables = extract_tables_from_pdf(pdf_path)
        
        # Extract only the first two tables
        first_two_tables = tables[:2]
        
        # Save the extracted tables to a text file
        output_file_path = '/Users/joathcarrera/Desktop/CSE115A/Soccer-Match-Predictor/2425_Calendars/extracted_tables.txt'
        with open(output_file_path, 'w') as f:
            for i, table in enumerate(first_two_tables):
                f.write(f"Table {i+1}:\n")
                for row in table:
                    f.write(f"{row}\n")
                f.write("\n")
        
        self.assertIsInstance(first_two_tables, list)
        self.assertEqual(len(first_two_tables), 2)


    def test_clean_date(self):

        """Test date cleaning for various formats.
        
        This test verifies that the clean_date function correctly converts various
        date formats to the expected standardized format. mm/dd/yyyy
        """

        
        self.assertEqual(clean_date('31.05.-01.06.2024'), '05/31/2024 - 06/01/2024')
        self.assertEqual(clean_date('30./31.05.2024'), '05/30/2024 - 05/31/2024')
        self.assertEqual(clean_date('30.-31.05.2024'), '05/30/2024 - 05/31/2024')
        self.assertEqual(clean_date('30.05.2024'), '05/30/2024')
    
    def test_clean_and_split_tables(self):

        """Test cleaning and splitting tables.
        
        This test checks if the clean_and_split_tables function correctly processes
        a sample input table into the expected cleaned and split format.
        """

        self.maxDiff = None
        
        # Sample input table
        tables = [
            ['18.08.2023 - Fr', '20:30', '1', '1', 'SV Werder Bremen', 'FC Bayern München'],
            ['19./20.08.2023', '', '1', '2', 'Borussia Dortmund', '1. FC Köln'],
            ['19./20.08.2023', '', '1', '3', '1. FC Union Berlin', '1. FSV Mainz 05'],
            ['19./20.08.2023', '', '1', '4', 'Bayer 04 Leverkusen', 'RB Leipzig'],
            ['19./20.08.2023', '', '1', '5', 'Eintracht Frankfurt', 'SV Darmstadt 98'],
            ['19./20.08.2023', '', '1', '6', 'VfL Wolfsburg', '1. FC Heidenheim 1846'],
            ['19./20.08.2023', '', '1', '7', 'TSG Hoffenheim', 'Sport-Club Freiburg'],
            ['19./20.08.2023', '', '1', '8', 'FC Augsburg', 'Borussia Mönchengladbach'],
            ['19./20.08.2023', '', '1', '9', 'VfB Stuttgart', 'VfL Bochum 1848'],
            ['25.-27.08.2023', '', '2', '10', 'FC Bayern München', 'FC Augsburg'],
            ['25.-27.08.2023', '', '2', '11', 'RB Leipzig', 'VfB Stuttgart'],
            ['25.-27.08.2023', '', '2', '12', 'Sport-Club Freiburg', 'SV Werder Bremen'],
            ['25.-27.08.2023', '', '2', '13', '1. FSV Mainz 05', 'Eintracht Frankfurt'],
            ['25.-27.08.2023', '', '2', '14', 'Borussia Mönchengladbach', 'Bayer 04 Leverkusen'],
            ['25.-27.08.2023', '', '2', '15', '1. FC Köln', 'VfL Wolfsburg'],
            ['25.-27.08.2023', '', '2', '16', 'VfL Bochum 1848', 'Borussia Dortmund'],
            ['25.-27.08.2023', '', '2', '17', '1. FC Heidenheim 1846', 'TSG Hoffenheim'],
            ['25.-27.08.2023', '', '2', '18', 'SV Darmstadt 98', '1. FC Union Berlin'],
        ]
        
        # Expected output format
        expected_output = {
            "01": [
                ['08/18/2023', '20:30', '1', '1', 'SV Werder Bremen', 'FC Bayern München'],
                ['08/19/2023 - 08/20/2023', '', '1', '2', 'Borussia Dortmund', '1. FC Köln'],
                ['08/19/2023 - 08/20/2023', '', '1', '3', '1. FC Union Berlin', '1. FSV Mainz 05'],
                ['08/19/2023 - 08/20/2023', '', '1', '4', 'Bayer 04 Leverkusen', 'RB Leipzig'],
                ['08/19/2023 - 08/20/2023', '', '1', '5', 'Eintracht Frankfurt', 'SV Darmstadt 98'],
                ['08/19/2023 - 08/20/2023', '', '1', '6', 'VfL Wolfsburg', '1. FC Heidenheim 1846'],
                ['08/19/2023 - 08/20/2023', '', '1', '7', 'TSG Hoffenheim', 'Sport-Club Freiburg'],
                ['08/19/2023 - 08/20/2023', '', '1', '8', 'FC Augsburg', 'Borussia Mönchengladbach'],
                ['08/19/2023 - 08/20/2023', '', '1', '9', 'VfB Stuttgart', 'VfL Bochum 1848']
            ],
            "02": [
                ['08/25/2023 - 08/27/2023', '', '2', '10', 'FC Bayern München', 'FC Augsburg'],
                ['08/25/2023 - 08/27/2023', '', '2', '11', 'RB Leipzig', 'VfB Stuttgart'],
                ['08/25/2023 - 08/27/2023', '', '2', '12', 'Sport-Club Freiburg', 'SV Werder Bremen'],
                ['08/25/2023 - 08/27/2023', '', '2', '13', '1. FSV Mainz 05', 'Eintracht Frankfurt'],
                ['08/25/2023 - 08/27/2023', '', '2', '14', 'Borussia Mönchengladbach', 'Bayer 04 Leverkusen'],
                ['08/25/2023 - 08/27/2023', '', '2', '15', '1. FC Köln', 'VfL Wolfsburg'],
                ['08/25/2023 - 08/27/2023', '', '2', '16', 'VfL Bochum 1848', 'Borussia Dortmund'],
                ['08/25/2023 - 08/27/2023', '', '2', '17', '1. FC Heidenheim 1846', 'TSG Hoffenheim'],
                ['08/25/2023 - 08/27/2023', '', '2', '18', 'SV Darmstadt 98', '1. FC Union Berlin']
            ]
        }
        
        matchday_tables = clean_and_split_tables([tables])  # Wrapping tables in a list to match function input
        self.assertIsInstance(matchday_tables, dict)
        self.assertEqual(matchday_tables, expected_output)
    
    def test_filter_bundesliga_matches(self):

        """Test filtering Bundesliga matches.
        
        This test checks if the filter_bundesliga_matches function correctly filters
        out non-Bundesliga matches from the provided matchday tables.
        """
        
        # Sample input table
        matchday_tables = {
            "01": [
                ['08/11/2023 - 08/14/2023', '', 'DFB', 'R1 A', '', ''],
                ['08/12/2023', '', 'DFL', 'SCUP', '', ''],
                ['08/18/2023', '', '1', '1', 'SV Werder Bremen', 'FC Bayern München'],
                ['08/19/2023 - 08/20/2023', '', '1', '2', 'Borussia Dortmund', '1. FC Köln'],
                ['08/19/2023 - 08/20/2023', '', '1', '3', '1. FC Union Berlin', '1. FSV Mainz 05'],
                ['08/19/2023 - 08/20/2023', '', '1', '4', 'Bayer 04 Leverkusen', 'RB Leipzig'],
                ['08/19/2023 - 08/20/2023', '', '1', '5', 'Eintracht Frankfurt', 'SV Darmstadt 98'],
                ['08/19/2023 - 08/20/2023', '', '1', '6', 'VfL Wolfsburg', '1. FC Heidenheim 1846'],
                ['08/19/2023 - 08/20/2023', '', '1', '7', 'TSG Hoffenheim', 'Sport-Club Freiburg'],
                ['08/19/2023 - 08/20/2023', '', '1', '8', 'FC Augsburg', 'Borussia Mönchengladbach'],
                ['08/19/2023 - 08/20/2023', '', '1', '9', 'VfB Stuttgart', 'VfL Bochum 1848']
            ],
            "02": [
                ['08/22/2023 - 08/23/2023', '', 'DFB', 'R1 B', '', ''],
                ['08/24/2023', '', 'UECL', 'PO R', '', ''],
                ['08/25/2023 - 08/27/2023', '', '2', '10', 'FC Bayern München', 'FC Augsburg'], 
                ['08/25/2023 - 08/27/2023', '', '2', '11', 'RB Leipzig', 'VfB Stuttgart'],
                ['08/25/2023 - 08/27/2023', '', '2', '12', 'Sport-Club Freiburg', 'SV Werder Bremen'],
                ['08/25/2023 - 08/27/2023', '', '2', '13', '1. FSV Mainz 05', 'Eintracht Frankfurt'],
                ['08/25/2023 - 08/27/2023', '', '2', '14', 'Borussia Mönchengladbach', 'Bayer 04 Leverkusen'],
                ['08/25/2023 - 08/27/2023', '', '2', '15', '1. FC Köln', 'VfL Wolfsburg'],
                ['08/25/2023 - 08/27/2023', '', '2', '16', 'VfL Bochum 1848', 'Borussia Dortmund'],
                ['08/25/2023 - 08/27/2023', '', '2', '17', '1. FC Heidenheim 1846', 'TSG Hoffenheim'],
                ['08/25/2023 - 08/27/2023', '', '2', '18', 'SV Darmstadt 98', '1. FC Union Berlin'],
            ]
        }
        
        # Expected output format
        expected_output = {
            "01": [
                ['08/18/2023', '', '1', '1', 'SV Werder Bremen', 'FC Bayern München'],
                ['08/19/2023 - 08/20/2023', '', '1', '2', 'Borussia Dortmund', '1. FC Köln'],
                ['08/19/2023 - 08/20/2023', '', '1', '3', '1. FC Union Berlin', '1. FSV Mainz 05'],
                ['08/19/2023 - 08/20/2023', '', '1', '4', 'Bayer 04 Leverkusen', 'RB Leipzig'],
                ['08/19/2023 - 08/20/2023', '', '1', '5', 'Eintracht Frankfurt', 'SV Darmstadt 98'],
                ['08/19/2023 - 08/20/2023', '', '1', '6', 'VfL Wolfsburg', '1. FC Heidenheim 1846'],
                ['08/19/2023 - 08/20/2023', '', '1', '7', 'TSG Hoffenheim', 'Sport-Club Freiburg'],
                ['08/19/2023 - 08/20/2023', '', '1', '8', 'FC Augsburg', 'Borussia Mönchengladbach'],
                ['08/19/2023 - 08/20/2023', '', '1', '9', 'VfB Stuttgart', 'VfL Bochum 1848']
            ],
            "02": [
                ['08/25/2023 - 08/27/2023', '', '2', '10', 'FC Bayern München', 'FC Augsburg'],
                ['08/25/2023 - 08/27/2023', '', '2', '11', 'RB Leipzig', 'VfB Stuttgart'],
                ['08/25/2023 - 08/27/2023', '', '2', '12', 'Sport-Club Freiburg', 'SV Werder Bremen'],
                ['08/25/2023 - 08/27/2023', '', '2', '13', '1. FSV Mainz 05', 'Eintracht Frankfurt'],
                ['08/25/2023 - 08/27/2023', '', '2', '14', 'Borussia Mönchengladbach', 'Bayer 04 Leverkusen'],
                ['08/25/2023 - 08/27/2023', '', '2', '15', '1. FC Köln', 'VfL Wolfsburg'],
                ['08/25/2023 - 08/27/2023', '', '2', '16', 'VfL Bochum 1848', 'Borussia Dortmund'],
                ['08/25/2023 - 08/27/2023', '', '2', '17', '1. FC Heidenheim 1846', 'TSG Hoffenheim'],
                ['08/25/2023 - 08/27/2023', '', '2', '18', 'SV Darmstadt 98', '1. FC Union Berlin']
            ]
        }
        filtered_tables = filter_bundesliga_matches(matchday_tables)
        self.assertIsInstance(filtered_tables, dict)
        self.assertEqual(filtered_tables, expected_output)


        

if __name__ == '__main__':
    unittest.main()


