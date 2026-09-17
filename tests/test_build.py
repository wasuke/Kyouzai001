import tempfile
import unittest
from pathlib import Path
from scripts.build import collect

class MaterialsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.folder = self.root / 'codes' / '01'
        self.folder.mkdir(parents=True)
    def tearDown(self):
        self.tmp.cleanup()
    def test_empty_lessons(self):
        data = collect(self.root)
        self.assertEqual(len(data['lessons']), 6)
        self.assertTrue(all(not x['codes'] for x in data['lessons']))
    def test_order_names_and_exact_text(self):
        source = '    print("日本語 <script>")\r\n\r\n'
        for name in ('10_最後.py', '2_真ん中.py', '1_最初.py'):
            (self.folder / name).write_bytes(source.encode('utf-8'))
        codes = collect(self.root)['lessons'][0]['codes']
        self.assertEqual([c['name'] for c in codes], ['最初', '真ん中', '最後'])
        self.assertEqual(codes[0]['content'], source)
    def test_hidden_files_ignored(self):
        (self.folder / '.gitkeep').touch()
        self.assertEqual(collect(self.root)['lessons'][0]['codes'], [])
    def test_bad_encoding_rejected(self):
        (self.folder / 'bad.py').write_bytes(b'\xff')
        with self.assertRaises(UnicodeDecodeError): collect(self.root)
    def test_unsupported_file_rejected(self):
        (self.folder / 'image.png').touch()
        with self.assertRaises(ValueError): collect(self.root)
    def test_symlink_rejected(self):
        (self.folder / 'linked.py').symlink_to('/etc/hosts')
        with self.assertRaises(ValueError): collect(self.root)
    def test_subfolder_rejected(self):
        (self.folder / 'nested').mkdir()
        with self.assertRaises(ValueError): collect(self.root)

if __name__ == '__main__': unittest.main()
