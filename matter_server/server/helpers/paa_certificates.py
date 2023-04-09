"""
Utils to fetch CHIP Development Product Attestation Authority (PAA) certificates from DCL.

This is based on the original script from project-chip here:
https://github.com/project-chip/connectedhomeip/edit/master/credentials/fetch-paa-certs-from-dcl.py

All rights reserved.
"""

import asyncio
import logging
from os import makedirs
import re

from aiohttp import ClientError, ClientSession
from cryptography import x509
from cryptography.hazmat.primitives import serialization

from matter_server.server.const import PAA_ROOT_CERTS_DIR

LOGGER = logging.getLogger(__name__)
PRODUCTION_URL = "https://on.dcl.csa-iot.org"
TEST_URL = "https://on.test-net.dcl.csa-iot.org"
GIT_URL = "https://github.com/project-chip/connectedhomeip/raw/master/credentials/development/paa-root-certs"  # pylint: disable=line-too-long
GIT_CERTS = [
    "Chip-Test-PAA-FFF1-Cert",
    "Chip-Test-PAA-NoVID-Cert",
]
LAST_CERT_IDS: set[str] = set()


async def write_paa_root_cert(certificate: str, subject: str) -> None:
    """Write certificate from string to file."""

    def _write() -> None:
        filename_base = "dcld_mirror_" + re.sub(
            "[^a-zA-Z0-9_-]", "", re.sub("[=, ]", "_", subject)
        )
        filepath_base = PAA_ROOT_CERTS_DIR.joinpath(filename_base)
        # handle PEM certificate file
        file_path_pem = f"{filepath_base}.pem"
        LOGGER.debug("Writing certificate %s", file_path_pem)
        with open(file_path_pem, "w+", encoding="utf-8") as outfile:
            outfile.write(certificate)
        # handle DER certificate file (converted from PEM)
        pem_certificate = x509.load_pem_x509_certificate(certificate.encode())
        file_path_der = f"{filepath_base}.der"
        LOGGER.debug("Writing certificate %s", file_path_der)
        with open(file_path_der, "wb+") as outfile:
            der_certificate = pem_certificate.public_bytes(serialization.Encoding.DER)
            outfile.write(der_certificate)

    return await asyncio.get_running_loop().run_in_executor(None, _write)


async def fetch_dcl_certificates(
    fetch_test_certificates: bool = True,
    fetch_production_certificates: bool = True,
) -> int:
    """Fetch DCL PAA Certificates."""
    LOGGER.info("Fetching the latest PAA root certificates from DCL.")
    if not PAA_ROOT_CERTS_DIR.is_dir():
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, makedirs, PAA_ROOT_CERTS_DIR)
    fetch_count: int = 0
    base_urls = set()
    # determine which url's need to be queried.
    # if we're going to fetch both prod and test, do test first
    # so any duplicates will be overwritten/preferred by the production version
    # NOTE: While Matter is in BETA we fetch the test certificates by default
    if fetch_test_certificates:
        base_urls.add(TEST_URL)
    if fetch_production_certificates:
        base_urls.add(PRODUCTION_URL)

    try:
        async with ClientSession(raise_for_status=True) as http_session:
            for url_base in base_urls:
                # fetch the paa certificates list
                async with http_session.get(
                    f"{url_base}/dcl/pki/root-certificates"
                ) as response:
                    result = await response.json()
                paa_list = result["approvedRootCertificates"]["certs"]
                # grab each certificate
                for paa in paa_list:
                    # do not fetch a certificate if we already fetched it
                    if paa["subjectKeyId"] in LAST_CERT_IDS:
                        continue
                    async with http_session.get(
                        f"{url_base}/dcl/pki/certificates/{paa['subject']}/{paa['subjectKeyId']}"
                    ) as response:
                        result = await response.json()

                    certificate_data: dict = result["approvedCertificates"]["certs"][0]
                    certificate: str = certificate_data["pemCert"]
                    subject = certificate_data["subjectAsText"]
                    certificate = certificate.rstrip("\n")

                    await write_paa_root_cert(
                        certificate,
                        subject,
                    )
                    LAST_CERT_IDS.add(paa["subjectKeyId"])
                    fetch_count += 1
    except ClientError as err:
        LOGGER.warning(
            "Fetching latest certificates failed: error %s", err, exc_info=err
        )
    else:
        LOGGER.info("Fetched %s PAA root certificates from DCL.", fetch_count)

    return fetch_count


async def fetch_git_certificates() -> int:
    """Fetch Git PAA Certificates."""
    fetch_count = 0
    LOGGER.info("Fetching the latest PAA root certificates from Git.")
    try:
        async with ClientSession(raise_for_status=True) as http_session:
            for cert in GIT_CERTS:
                if cert in LAST_CERT_IDS:
                    continue

                async with http_session.get(f"{GIT_URL}/{cert}.pem") as response:
                    certificate = await response.text()
                await write_paa_root_cert(certificate, cert)
                LAST_CERT_IDS.add(cert)
                fetch_count += 1
    except ClientError as err:
        LOGGER.warning(
            "Fetching latest certificates failed: error %s", err, exc_info=err
        )

    LOGGER.info("Fetched %s PAA root certificates from Git.", fetch_count)

    return fetch_count


async def fetch_certificates(
    fetch_test_certificates: bool = True,
    fetch_production_certificates: bool = True,
) -> int:
    """Fetch PAA Certificates."""

    fetch_count = await fetch_dcl_certificates(
        fetch_test_certificates=fetch_test_certificates,
        fetch_production_certificates=fetch_production_certificates,
    )

    if fetch_test_certificates:
        fetch_count += await fetch_git_certificates()

    return fetch_count
