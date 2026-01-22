import re

def remove_digital_signatures(body):
    # Remove PGP signatures
    body = re.sub(r"-----BEGIN PGP SIGNATURE-----.*?-----END PGP SIGNATURE-----", "", body, flags=re.DOTALL|re.IGNORECASE)
    # Remove S/MIME signatures
    body = re.sub(r"-----BEGIN S/MIME SIGNATURE-----.*?-----END S/MIME SIGNATURE-----", "", body, flags=re.DOTALL|re.IGNORECASE)

    # Remove common email footers / signatures
    body = re.sub(r"\n--+\s*\n.*", "", body, flags=re.DOTALL)

    return body.strip()
