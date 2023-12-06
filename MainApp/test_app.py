import unittest
from flask import session
from flask.testing import FlaskClient
from unittest.mock import patch, Mock
from Routes import app, MLApplier, permutation_importance_score, handle_non_numerical_data
import numpy as np
import pandas as pd

class FlaskTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        self._ctx = app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        self._ctx.pop()

    def test_homePage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_report(self):
        response = self.app.get('/report')
        self.assertEqual(response.status_code, 200)

    def test_permutation_importance_score(self):
        # Mocking the estimator, X, and y
        estimator = Mock()
        X = np.array([[1, 2], [3, 4]])
        y = np.array([0, 1])

        # Mocking the permutation_importance function
        with patch('Routes.permutation_importance') as mock_permutation_importance:
            mock_permutation_importance.return_value = np.array([[0.1, 0.2], [0.3, 0.4]])

            # Call the function
            result = permutation_importance_score(estimator, X, y)

            # Assert the mock function was called with the correct arguments
            mock_permutation_importance.assert_called_once_with(estimator, X, y, scoring='accuracy')

        # Assert the result is as expected
        expected_result = np.array([0.15000000000000002, 0.35])
        np.testing.assert_array_equal(result, expected_result)
    
    def test_handle_non_numerical_data(self):
        # Mocking the DataFrame
        data = {'Column1': ['A', 'B', 'A', 'B'],
                'Column2': [1, 2, 1, 3]}
        df = pd.DataFrame(data)

        # Call the function
        result_df = handle_non_numerical_data(df)

        def handle_non_numerical_data_t(df):
            columns = df.columns.values
            for column in columns:
                text_digit_vals = {}
                def convert_to_int(val):
                    return text_digit_vals[val]

                if df[column].dtype != np.int64 and df[column].dtype != np.float64:
                    column_contents = df[column].values.tolist()
                    unique_elements = set(column_contents)
                    x = 0
                    for unique in unique_elements:
                        if unique not in text_digit_vals:
                            text_digit_vals[unique] = x
                            x+=1

                    df[column] = list(map(convert_to_int, df[column]))

            return df
        # Assert the changes in the DataFrame
        expected_df = handle_non_numerical_data_t(df)
        pd.testing.assert_frame_equal(result_df, expected_df)

if __name__ == '__main__':
    unittest.main()
