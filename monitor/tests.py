from unittest.mock import patch

from django.test import SimpleTestCase

from .thresholds import evaluate_thresholds


class ThresholdEvaluationTests(SimpleTestCase):
    def test_soil_moisture_bands(self):
        self.assertEqual(evaluate_thresholds(35, None, None, 0)[0], 'NORMAL')
        self.assertEqual(evaluate_thresholds(35.1, None, None, 0)[0], 'WARNING')
        self.assertEqual(evaluate_thresholds(46, None, None, 0)[0], 'CRITICAL')

    def test_rain_rate_bands(self):
        self.assertEqual(evaluate_thresholds(20, 2.4, None, 0)[0], 'NORMAL')
        self.assertEqual(evaluate_thresholds(20, 2.5, None, 0)[0], 'WARNING')
        self.assertEqual(evaluate_thresholds(20, 25, None, 0)[0], 'WARNING')
        self.assertEqual(evaluate_thresholds(20, 25.1, None, 0)[0], 'CRITICAL')

    def test_humidity_bands(self):
        self.assertEqual(evaluate_thresholds(20, None, 74.9, 0)[0], 'NORMAL')
        self.assertEqual(evaluate_thresholds(20, None, 75, 0)[0], 'WARNING')
        self.assertEqual(evaluate_thresholds(20, None, 90, 0)[0], 'WARNING')
        self.assertEqual(evaluate_thresholds(20, None, 90.1, 0)[0], 'CRITICAL')

    def test_calibrated_water_stages(self):
        with patch.dict('os.environ', {'BANKFULL_WATER_LEVEL_CM': '60', 'OVERBANK_WATER_LEVEL_CM': '80'}):
            self.assertEqual(evaluate_thresholds(20, None, None, 59.9)[0], 'NORMAL')
            self.assertEqual(evaluate_thresholds(20, None, None, 60)[0], 'WARNING')
            self.assertEqual(evaluate_thresholds(20, None, None, 80)[0], 'CRITICAL')

    def test_highest_triggered_severity_wins(self):
        risk, reasons = evaluate_thresholds(40, 30, 80, 0)
        self.assertEqual(risk, 'CRITICAL')
        self.assertEqual(len(reasons), 3)