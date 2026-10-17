import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID
from util import extract_public_key, verify_artifact_signature


def make_cert_and_key():
    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "test")])
    now = datetime.datetime.now(datetime.timezone.utc)
    cert = (x509.CertificateBuilder()
            .subject_name(name)
            .issuer_name(name)
            .public_key(key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(now)
            .not_valid_after(now + datetime.timedelta(days=1))
            .sign(key, hashes.SHA256()))
    return cert.public_bytes(serialization.Encoding.PEM), key


def test_extract_public_key_returns_matching_pem():
    cert_pem, key = make_cert_and_key()
    expected = key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
    assert extract_public_key(cert_pem) == expected


def test_verify_artifact_signature_valid(tmp_path, capsys):
    cert_pem, key = make_cert_and_key()
    artifact = tmp_path / "artifact.md"
    artifact.write_bytes(b"hello world")
    signature = key.sign(b"hello world", ec.ECDSA(hashes.SHA256()))

    verify_artifact_signature(signature, extract_public_key(cert_pem), str(artifact))
    assert "invalid" not in capsys.readouterr().out.lower()


def test_verify_artifact_signature_tampered_file(tmp_path, capsys):
    cert_pem, key = make_cert_and_key()
    artifact = tmp_path / "artifact.md"
    artifact.write_bytes(b"tampered content")
    signature = key.sign(b"original content", ec.ECDSA(hashes.SHA256()))

    verify_artifact_signature(signature, extract_public_key(cert_pem), str(artifact))
    assert "invalid" in capsys.readouterr().out.lower()