import hashlib


def calculate_sha256(file_bytes):
    """
    Generate SHA-256 hash for an uploaded document.
    """

    sha256 = hashlib.sha256()
    sha256.update(file_bytes)

    return sha256.hexdigest()


def verify_hash(file_bytes, original_hash):
    """
    Verify whether the current document matches
    its original SHA-256 hash.
    """

    current_hash = calculate_sha256(file_bytes)

    return current_hash == original_hash
