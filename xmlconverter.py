import logging
import xml.etree.ElementTree as ET
from typing import List, Optional
import csv


class XmlToCsvConverter:
    """
    A utility class for converting XML data to CSV format.
    """

    def __init__(self, headers: list[str] | None = None, logger: logging.Logger | None = None):
        self.headers = headers if headers else ["Id", "FullNm", "ClssfctnTp", "CmmdtyDerivInd", "NtnlCcy", "Issr"]
        self.logger = logger if logger else logging.getLogger(__name__)
        self.namespaces = {
            'head': 'urn:iso:std:iso:20022:tech:xsd:head.003.001.01',
            'apphdr': 'urn:iso:std:iso:20022:tech:xsd:head.001.001.01',
            'auth': 'urn:iso:std:iso:20022:tech:xsd:auth.036.001.02'
        }

    @staticmethod
    def get_xml_data(xml_file_path: str) -> ET:
        """
        Parse an XML file and return its root element.

        :param xml_file_path: The path to the XML file.
        :return: The root element of the XML file.
        """
        tree = ET.parse(xml_file_path)
        return tree.getroot()

    def convert(self, xml_file_path: str) -> List[List[str]]:
        """
        Convert the XML data to CSV format and return the rows.

        :param xml_file_path: The path to the XML file.
        :param csv_file_path: The path to the output CSV file.
        :return: A list of lists representing the rows of the CSV data.
        """

        # Get the root element from the XML file
        xml_data = self.get_xml_data(xml_file_path)
        self.logger.info("Extracted root")

        # Find all FinInstrm elements
        fin_instrm_elements = xml_data.findall(".//auth:FinInstrm", namespaces=self.namespaces)
        rows = [self.headers]

        # Process the FinInstrm element and add them to the output list
        for element in fin_instrm_elements:
            issuer = element.find(".//auth:Issr", namespaces=self.namespaces).text
            fin_instrm_attrs = element.find(".//auth:FinInstrmGnlAttrbts", namespaces=self.namespaces)
            rows.append([
                fin_instrm_attrs.find("auth:Id", namespaces=self.namespaces).text,
                fin_instrm_attrs.find("auth:FullNm", namespaces=self.namespaces).text,
                fin_instrm_attrs.find("auth:ClssfctnTp", namespaces=self.namespaces).text,
                fin_instrm_attrs.find("auth:CmmdtyDerivInd", namespaces=self.namespaces).text,
                fin_instrm_attrs.find("auth:NtnlCcy", namespaces=self.namespaces).text,
                issuer
            ])
        self.logger.info(f"Processed {len(rows)} rows")

        return rows

    @staticmethod
    def write_to_file(csv_file_path: str, rows: List[List[str]]):
        """
        Write the CSV rows to a file.

        :param csv_file_path: The path to the output CSV file.
        :param rows: A list of lists representing the rows of the CSV data.
        """

        # Open a CSV file for writing
        with open(csv_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

