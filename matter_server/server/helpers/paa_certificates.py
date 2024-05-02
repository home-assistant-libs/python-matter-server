"""
Utils to fetch CHIP Development Product Attestation Authority (PAA) certificates from DCL.

This is based on the original script from project-chip here:
https://github.com/project-chip/connectedhomeip/edit/master/credentials/fetch-paa-certs-from-dcl.py

All rights reserved.
"""

import asyncio
from datetime import UTC, datetime, timedelta
import logging
import os
from pathlib import Path
import re
import warnings

from aiohttp import ClientError, ClientSession
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.utils import CryptographyDeprecationWarning

# Git repo details
OWNER = "project-chip"
REPO = "connectedhomeip"
PATH = "credentials/development/paa-root-certs"

LOGGER = logging.getLogger(__name__)
PRODUCTION_URL = "https://on.dcl.csa-iot.org"
TEST_URL = "https://on.test-net.dcl.csa-iot.org"
GIT_URL = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/master/{PATH}"


# Subject Key Identifier of certificates. The Subject Key Identifier is a mandatory
# X.509 extensions for Matter uniquely identifying the public key of PAA certificates.
CERT_SUBJECT_KEY_IDS: set[str] = set()


async def write_paa_root_cert(
    paa_root_cert_dir: Path, base_name: str, pem_certificate: str, subject: str
) -> bool:
    """Write certificate from string to file."""

    def _write(
        paa_root_cert_dir: Path,
        filename_base: str,
        pem_certificate: str,
        der_certificate: bytes,
    ) -> None:
        # handle PEM certificate file
        file_path_pem = paa_root_cert_dir.joinpath(f"{filename_base}.pem")
        LOGGER.debug("Writing PEM certificate %s", file_path_pem)
        with open(file_path_pem, "w+", encoding="utf-8") as outfile:
            outfile.write(pem_certificate)
        # handle DER certificate file (converted from PEM)
        file_path_der = paa_root_cert_dir.joinpath(f"{filename_base}.der")
        LOGGER.debug("Writing DER certificate %s", file_path_der)
        with open(file_path_der, "wb+") as outfile:
            outfile.write(der_certificate)

    filename_base = base_name + re.sub(
        "[^a-zA-Z0-9_-]", "", re.sub("[=, ]", "_", subject)
    )

    # Some certificates lead to a warning from the cryptography library:
    # CryptographyDeprecationWarning: The parsed certificate contains a
    # NULL parameter value in its signature algorithm parameters.
    with warnings.catch_warnings():
        if LOGGER.isEnabledFor(logging.DEBUG):
            # Use always so warnings are printed for each offending cert.
            warnings.simplefilter("always", CryptographyDeprecationWarning)
        else:
            # Ignore the warnings generally. The problem has been reported to the CSA
            # via Slack.
            warnings.simplefilter("ignore", CryptographyDeprecationWarning)

        cert = x509.load_pem_x509_certificate(pem_certificate.encode())

    ski: x509.SubjectKeyIdentifier = cert.extensions.get_extension_for_class(
        x509.SubjectKeyIdentifier
    ).value
    ski_formatted = ":".join(f"{byte:02X}" for byte in ski.digest)
    if ski_formatted in CERT_SUBJECT_KEY_IDS:
        LOGGER.debug(
            "Skipping, certificate with the same subject key identifier already stored."
        )
        return False
    CERT_SUBJECT_KEY_IDS.add(ski_formatted)

    der_certificate = cert.public_bytes(serialization.Encoding.DER)

    await asyncio.get_running_loop().run_in_executor(
        None,
        _write,
        paa_root_cert_dir,
        filename_base,
        pem_certificate,
        der_certificate,
    )

    return True


async def fetch_dcl_certificates(
    paa_root_cert_dir: Path,
    base_name: str,
    base_url: str,
) -> int:
    """Fetch DCL PAA Certificates."""
    fetch_count: int = 0

    try:
        async with ClientSession(raise_for_status=True) as http_session:
            # fetch the paa certificates list
            async with http_session.get(
                f"{base_url}/dcl/pki/root-certificates"
            ) as response:
                result = await response.json()
            paa_list = result["approvedRootCertificates"]["certs"]
            # grab each certificate
            for paa in paa_list:
                # do not fetch a certificate if we already fetched it
                if paa["subjectKeyId"] in CERT_SUBJECT_KEY_IDS:
                    continue
                url = f"{base_url}/dcl/pki/certificates/{paa['subject']}/{paa['subjectKeyId']}"
                LOGGER.debug("Downloading certificate from %s", url)
                async with http_session.get(url) as response:
                    result = await response.json()

                certificate_data: dict = result["approvedCertificates"]["certs"][0]
                certificate: str = certificate_data["pemCert"]
                subject = certificate_data["subjectAsText"]
                certificate = certificate.rstrip("\n")
                if await write_paa_root_cert(
                    paa_root_cert_dir,
                    base_name,
                    certificate,
                    subject,
                ):
                    fetch_count += 1
    except (ClientError, TimeoutError) as err:
        LOGGER.warning(
            "Fetching latest certificates failed: error %s", err, exc_info=err
        )

    return fetch_count


# Manufacturers release test certificates through the SDK (Git) as a part
# of their standard product release workflow. This will ensure those certs
# are correctly captured


async def fetch_git_certificates(paa_root_cert_dir: Path) -> int:
    """Fetch Git PAA Certificates."""
    fetch_count = 0
    LOGGER.info("Fetching the latest PAA root certificates from Git.")

    try:
        async with ClientSession(raise_for_status=True) as http_session:
            # Fetch directory contents and filter out extension
            api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{PATH}"
            async with http_session.get(api_url, timeout=20) as response:
                contents = await response.json()
                git_certs = {item["name"].split(".")[0] for item in contents}
            # Fetch certificates
            for cert in git_certs:
                async with http_session.get(f"{GIT_URL}/{cert}.pem") as response:
                    certificate = await response.text()
                if await write_paa_root_cert(
                    paa_root_cert_dir, "git_", certificate, cert
                ):
                    fetch_count += 1
    except (ClientError, TimeoutError) as err:
        LOGGER.warning(
            "Fetching latest certificates failed: error %s", err, exc_info=err
        )

    LOGGER.info("Fetched %s PAA root certificates from Git.", fetch_count)

    return fetch_count


async def fetch_certificates(
    paa_root_cert_dir: Path,
    fetch_test_certificates: bool = True,
    fetch_production_certificates: bool = True,
) -> int:
    """Fetch PAA Certificates."""
    loop = asyncio.get_running_loop()

    if not paa_root_cert_dir.is_dir():

        def _make_root_cert_dir(paa_root_cert_dir: Path) -> None:
            paa_root_cert_dir.mkdir(parents=True)
            # Clear mtime to make sure code retries if first fetch fails.
            os.utime(paa_root_cert_dir, (0, 0))

        await loop.run_in_executor(None, _make_root_cert_dir, paa_root_cert_dir)
    else:
        stat = await loop.run_in_executor(None, paa_root_cert_dir.stat)
        last_fetch = datetime.fromtimestamp(stat.st_mtime, tz=UTC)
        if last_fetch > datetime.now(tz=UTC) - timedelta(days=1):
            LOGGER.info(
                "Skip fetching certificates (already fetched within the last 24h)."
            )
            return 0

    total_fetch_count = 0

    LOGGER.info("Fetching the latest PAA root certificates from DCL.")

    # Determine which url's need to be queried.
    if fetch_production_certificates:
        fetch_count = await fetch_dcl_certificates(
            paa_root_cert_dir=paa_root_cert_dir,
            base_name="dcld_production_",
            base_url=PRODUCTION_URL,
        )
        LOGGER.info("Fetched %s PAA root certificates from DCL.", fetch_count)
        total_fetch_count += fetch_count

    if fetch_test_certificates:
        fetch_count = await fetch_dcl_certificates(
            paa_root_cert_dir=paa_root_cert_dir,
            base_name="dcld_test_",
            base_url=TEST_URL,
        )
        LOGGER.info("Fetched %s PAA root certificates from Test DCL.", fetch_count)
        total_fetch_count += fetch_count

    if fetch_test_certificates:
        total_fetch_count += await fetch_git_certificates(paa_root_cert_dir)

    await loop.run_in_executor(None, paa_root_cert_dir.touch)

    return fetch_count
