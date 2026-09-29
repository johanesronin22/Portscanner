import os
import sys
import unittest
from unittest.mock import patch
from app import app
from database.database import init_db, get_db_connection

class EndToEndTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        # Use an in-memory DB for tests, but here we can just use a test file
        app.config['DATABASE'] = 'test.db'
        self.client = app.test_client()
        with app.app_context():
            init_db()

    def test_end_to_end(self):
        # 1. Post to perform_scan
        response = self.client.post('/perform_scan', data={'target': 'scanme.nmap.org'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('scan_id', data)
        self.assertIn('redirect_url', data)
        
        scan_id = data['scan_id']
        
        # 2. View Results
        resp2 = self.client.get(f'/results/{scan_id}')
        self.assertEqual(resp2.status_code, 200)
        self.assertIn(b'scanme.nmap.org', resp2.data)
        # 3. View History
        resp3 = self.client.get('/history')
        self.assertEqual(resp3.status_code, 200)
        self.assertIn(b'scanme.nmap.org', resp3.data)
        
        # 4. Generate HTML Report
        resp4 = self.client.get(f'/report/{scan_id}/html')
        self.assertEqual(resp4.status_code, 200)
        self.assertIn('text/html', resp4.headers.get('Content-Type'))
        
        # 5. Generate PDF Report (may fail if GTK isn't installed, but we should test route)
        resp5 = self.client.get(f'/report/{scan_id}/pdf')
        # If WeasyPrint fails due to GTK, it redirects with a flash message
        if resp5.status_code == 302:
            print("PDF generation gracefully failed (likely missing GTK3 on Windows). HTML is available.")
        else:
            self.assertEqual(resp5.status_code, 200)
            self.assertEqual(resp5.headers.get('Content-Type'), 'application/pdf')

if __name__ == '__main__':
    unittest.main()
