import unittest
import os
import io
from app import app


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = 'upload_test'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

        # for test dir
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

    def tearDown(self):
        # rm test dir
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir(app.config['UPLOAD_FOLDER'])
        self.app_context.pop()

    def test_index(self):
        # its work?
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload a text file', response.data)

    def test_upload_no_file(self):
        # no file
        response = self.app.post('/upload')
        self.assertEqual(response.status_code, 302)

        response = self.app.get('/')
        self.assertIn(b'No file part', response.data)

    def test_upload_empty_file(self):
        # empty input
        data = {
            'file': (io.BytesIO(b''), '')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 302)

        response = self.app.get('/')
        self.assertNotIn(b'No selected file', response.data)

    def test_upload_valid_file(self):
        # normal input
        data = {
            'file': (io.BytesIO(b'This is a test file with some words. Words are repeated words words words.'), 'test.txt')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'words', response.data)  # words?
        self.assertIn(b'5', response.data)  # 5 words

if __name__ == '__main__':
    unittest.main()
