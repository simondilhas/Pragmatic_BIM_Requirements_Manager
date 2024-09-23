import unittest
import pandas as pd
from pathlib import Path
from tempfile import TemporaryDirectory
from io import StringIO

# Import the functions to test
from src.import_csv import (
    get_data_path,
    load_dataframes,
    check_required_columns,
    process_attributes_df,
    export_excel,
    VERSION
)

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.data_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_data_path(self):
        expected_path = Path(__file__).parent.parent / 'data' / VERSION
        self.assertEqual(get_data_path(VERSION), expected_path)

    def test_load_dataframes(self):
        # Create sample CSV files
        for file_name in ['M_Attributes.csv', 'M_Elements.csv', 'M_Models.csv', 'M_Workflows.csv']:
            with open(self.data_dir / file_name, 'w') as f:
                f.write('Column1,Column2\nValue1,Value2\n')

        dataframes = load_dataframes(self.data_dir)

        self.assertEqual(len(dataframes), 4)
        for df_name, df in dataframes.items():
            self.assertIsInstance(df, pd.DataFrame)
            self.assertEqual(df.shape, (1, 2))

    def test_check_required_columns(self):
        df = pd.DataFrame({'Column1': [], 'Column2': []})
        required_columns = ['Column1', 'Column2*']

        # This should not raise an error
        check_required_columns(df, required_columns, 'test_df')

        # This should raise a ValueError
        with self.assertRaises(ValueError):
            check_required_columns(df, ['Column1', 'Column3'], 'test_df')

    def test_process_attributes_df(self):
        data = StringIO('''ElementID,ModelID,WorkflowID,SortAttribute
    1,A,X,2
    2,"B,C","Y,Z",1
    3,1,2,3
    ''')
        df = pd.read_csv(data)
        result = process_attributes_df(df)

        # The result should have 6 rows due to exploding "B,C" and "Y,Z"
        self.assertEqual(result.shape, (6, 4))
        self.assertEqual(result['SortAttribute'].tolist(), [1.0, 1.0, 1.0, 1.0, 2.0, 3.0])
        self.assertTrue(all(isinstance(x, str) for x in result['ElementID']))
        self.assertTrue(all(isinstance(x, str) for x in result['ModelID']))
        self.assertTrue(all(isinstance(x, str) for x in result['WorkflowID']))
        
        # Check if the exploding worked correctly
        self.assertIn('B', result['ModelID'].tolist())
        self.assertIn('C', result['ModelID'].tolist())
        self.assertIn('Y', result['WorkflowID'].tolist())
        self.assertIn('Z', result['WorkflowID'].tolist())
        
        # Check if the rows are in the correct order after sorting by SortAttribute
        self.assertEqual(result['ElementID'].tolist(), ['2', '2', '2', '2', '1', '3'])
        self.assertEqual(result['ModelID'].tolist(), ['B', 'B', 'C', 'C', 'A', '1'])
        self.assertEqual(result['WorkflowID'].tolist(), ['Y', 'Z', 'Y', 'Z', 'X', '2'])

    def test_export_excel(self):
        df = pd.DataFrame({'Column1': [1, 2], 'Column2': ['A', 'B']})
        export_excel(df, self.data_dir, VERSION)

        expected_file = self.data_dir / f"Elementplan_{VERSION}_raw_data.xlsx"
        self.assertTrue(expected_file.exists())

        # Read the Excel file and check its contents
        df_read = pd.read_excel(expected_file)
        pd.testing.assert_frame_equal(df, df_read)

        print("Data processing completed successfully.")

if __name__ == '__main__':
    unittest.main()