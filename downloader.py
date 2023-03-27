import io
import logging
import xml.etree.ElementTree as ET
import zipfile

import requests as requests


class Downloader:
    """
    A utility class for downloading and extracting content from a given URL.
    """

    def __init__(self, logger: logging.Logger | None = None):
        self.logger = logger if logger else logging.getLogger(__name__)

    def download_url(self, url: str) -> str:
        """
        Download an XML file from the given URL, parse it, and return the download link from the first document.

        :param url: The URL to download the XML file from.
        :return: The download link extracted from the first document in the XML file.
        :raises ValueError: If no documents are found in the XML file.
        """

        response = requests.get(url)
        if not response.ok:
            error_message = f"Request failed returned status code {response.status_code}."
            self.logger.error(error_message)
            raise RuntimeError(error_message)
        self.logger.info("Successfully retrieved xml file")

        root = ET.fromstring(response.content.decode("utf8"))  # Decode response to utf8 then parse
        result = root.find("result")
        docs = result.findall("doc") if result is not None else []

        if len(docs) == 0:
            error_message = "No content. Expecting content but no docs in result."
            self.logger.error(error_message)
            raise ValueError(error_message)

        # Filter the first doc to find the download_link
        first_doc_elements = docs[0].findall("str")
        download_link_element = list(filter(lambda x: x.attrib.get("name") == "download_link", first_doc_elements))

        return_val = download_link_element[0].text

        self.logger.info("Successfully retrieved download link")
        return return_val

    def download_and_extract(self, url: str) -> str:
        """
        Download a zipfile from the given URL, extract the first file, and return its path.

        :param url: The URL to download the zipfile from.
        :return: The path to the first extracted file from the zipfile.
        :raises ValueError: If no files are found in the zipfile.
        """
        response = requests.get(url)
        if not response.ok:
            error_message = f"Request failed returned status code {response.status_code}."
            self.logger.error(error_message)
            raise RuntimeError(error_message)

        with zipfile.ZipFile(io.BytesIO(response.content)) as data:
            if len(data.filelist) == 0:
                raise ValueError

            extracted = data.extract(member=data.filelist[0].filename)
            self.logger.info("Successfully extracted data url")
            return extracted
