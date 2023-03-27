import unittest
from unittest.mock import MagicMock, patch
from xml.etree.ElementTree import Element
import os
import tempfile
import csv

from xmlconverter import XmlToCsvConverter


class TestXmlToCsvConverter(unittest.TestCase):

    def setUp(self):
        self.headers = ["Id", "FullNm", "ClssfctnTp", "CmmdtyDerivInd", "NtnlCcy", "Issr"]
        self.converter = XmlToCsvConverter(headers=self.headers)

    def test_get_xml_data(self):
        # Prepare a sample XML file
        xml_content = '''
        <root>
            <child>Content</child>
        </root>
        '''
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write(xml_content)

        # Test the get_xml_data() method
        root = self.converter.get_xml_data(f.name)
        self.assertIsInstance(root, Element)
        os.unlink(f.name)

    def test_convert(self):
        test_xml = """<?xml version="1.0" encoding="UTF-8"?>
            <root xmlns:auth="urn:iso:std:iso:20022:tech:xsd:auth.036.001.02">
                <auth:FinInstrm>
                    <auth:Issr>Issuer1</auth:Issr>
                    <auth:FinInstrmGnlAttrbts>
                        <auth:Id>1</auth:Id>
                        <auth:FullNm>Instrument1</auth:FullNm>
                        <auth:ClssfctnTp>Type1</auth:ClssfctnTp>
                        <auth:CmmdtyDerivInd>True</auth:CmmdtyDerivInd>
                        <auth:NtnlCcy>USD</auth:NtnlCcy>
                    </auth:FinInstrmGnlAttrbts>
                </auth:FinInstrm>
            </root>
        """
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
            tmp_file.write(test_xml)
            tmp_file.flush()

        converter = XmlToCsvConverter()
        rows = converter.convert(tmp_file.name)
        os.remove(tmp_file.name)

        expected_rows = [
            ["Id", "FullNm", "ClssfctnTp", "CmmdtyDerivInd", "NtnlCcy", "Issr"],
            ["1", "Instrument1", "Type1", "True", "USD", "Issuer1"]
        ]
        self.assertEqual(rows, expected_rows)

    def test_write_to_file(self):
        rows = [
            ["Id", "FullNm", "ClssfctnTp", "CmmdtyDerivInd", "NtnlCcy", "Issr"],
            ["1", "Instrument1", "Type1", "True", "USD", "Issuer1"]
        ]
        converter = XmlToCsvConverter()

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp_file:
            converter.write_to_file(tmp_file.name, rows)
            tmp_file.flush()

            with open(tmp_file.name, newline='') as f:
                reader = csv.reader(f)
                read_rows = [row for row in reader]

            os.remove(tmp_file.name)

        self.assertEqual(rows, read_rows)
