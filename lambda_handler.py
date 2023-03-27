import json
import logging

from downloader import Downloader
from xmlconverter import XmlToCsvConverter
from uploader import S3Uploader


def lambda_handler(event: str, context: dict | None) -> dict:
    event = json.loads(event)
    url = event.get('url', None)

    if not url:
        raise ValueError("URL not present")

    # Download and extract the XML from the ZIP file
    downloader = Downloader()
    download_url = downloader.download_url(url)
    xml_file_path = downloader.download_and_extract(download_url)

    # Convert the XML to CSV
    xtc = XmlToCsvConverter()
    csv_rows = xtc.convert(xml_file_path)
    xtc.write_to_file("data.csv", csv_rows)

    # Upload the CSV to S3
    s3u = S3Uploader("data.csv")
    url = s3u.upload()

    return {"url": url}
