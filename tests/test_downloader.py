import io
import logging
import os
import unittest
import zipfile
from unittest.mock import MagicMock, patch
from xml.etree.ElementTree import Element, SubElement, tostring

from downloader import Downloader


class TestDownloader(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("test_logger")
        self.downloader = Downloader(logger=self.logger)

    def test_download_url(self):
        test_url = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/"\
            "select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&"\
            "indent=true&start=0&rows=100"
        test_download_link = "http://firds.esma.europa.eu/firds/DLTINS_20210117_01of01.zip"

        # Create a sample XML response
        root = Element("response")
        result = SubElement(root, "result")
        doc = SubElement(result, "doc")
        download_link = SubElement(doc, "str", {"name": "download_link"})
        download_link.text = test_download_link
        xml_response = tostring(root)

        # Mock the requests.get() method
        with patch("requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.content = xml_response

            # Test the download_url method
            download_link_result = self.downloader.download_url(test_url)
            self.assertEqual(download_link_result, test_download_link)

    def test_download_and_extract(self):
        test_url = "https://example.com/sample.zip"
        test_content = b"test content"

        # Mock the requests.get() method
        with patch("requests.get") as mock_get:
            # Create a sample zipfile in memory
            in_memory_zip = io.BytesIO()
            with zipfile.ZipFile(in_memory_zip, mode="w") as zf:
                zf.writestr("test_file.txt", test_content)
            in_memory_zip.seek(0)

            mock_get.return_value.ok = True
            mock_get.return_value.content = in_memory_zip.read()

            # Test the download_and_extract method
            extracted_file_path = self.downloader.download_and_extract(test_url)
            self.assertTrue(os.path.exists(extracted_file_path))

            # Clean up the extracted file
            os.remove(extracted_file_path)
