import base64, pytest, main
import json, sys
from unittest.mock import MagicMock


def test_get_verification_proof_invalid_index():
    with pytest.raises(ValueError):
        main.get_verification_proof(-5)


def test_inclusion_invalid_index(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("x")
    with pytest.raises(ValueError):
        main.inclusion("abc", str(f))


def test_cli_debug_flag(monkeypatch, capsys):
    monkeypatch.setattr(main, "get_latest_checkpoint", MagicMock(return_value={}))
    monkeypatch.setattr(sys, "argv", ["main.py", "-d", "-c"])
    main.main()
    assert "enabled debug mode" in capsys.readouterr().out


def test_cli_consistency_full_path(monkeypatch):
    cons = MagicMock()
    monkeypatch.setattr(main, "consistency", cons)
    monkeypatch.setattr(sys, "argv", ["main.py", "--consistency", "--tree-id", "1",
                                      "--tree-size", "10", "--root-hash", "ab"])
    main.main()
    cons.assert_called_once()


def test_cli_consistency_missing_tree_size(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "--consistency", "--tree-id", "1"])
    main.main()
    assert "tree size" in capsys.readouterr().out


def test_cli_consistency_missing_root_hash(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "--consistency", "--tree-id", "1", "--tree-size", "10"])
    main.main()
    assert "root hash" in capsys.readouterr().out


def fake_response(payload):
    resp = MagicMock()
    resp.json.return_value = payload
    resp.raise_for_status.return_value = None
    return resp


SAMPLE_CHECKPOINT = {"inactiveShards": [], "rootHash": "ab" * 32, "signedTreeHead": "sth", "treeID": "1193050959916656506", "treeSize": 2000}


def test_get_log_entry_rejects_negative_index():
    with pytest.raises(ValueError):
        main.get_log_entry(-1)


def test_get_log_entry_rejects_non_numeric_index():
    with pytest.raises(ValueError):
        main.get_log_entry("abc")


def test_consistency_rejects_empty_checkpoint():
    with pytest.raises(ValueError):
        main.consistency({})


def test_inclusion_rejects_missing_artifact(tmp_path):
    with pytest.raises(ValueError):
        main.inclusion(1, str(tmp_path / "does_not_exist.md"))


def test_get_log_entry_returns_json(monkeypatch):
    payload = {"uuid123": {"body": "e30="}}
    monkeypatch.setattr(main.requests, "get", MagicMock(return_value=fake_response(payload)))
    assert main.get_log_entry(5) == payload


def test_get_verification_proof_returns_inclusion_proof(monkeypatch):
    proof = {"logIndex": 5, "treeSize": 10, "hashes": [], "rootHash": "00"}
    payload = {"uuid123": {"verification": {"inclusionProof": proof}}}
    monkeypatch.setattr(main.requests, "get", MagicMock(return_value=fake_response(payload)))
    assert main.get_verification_proof(5) == proof


def test_get_latest_checkpoint_debug_writes_file(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(main.requests, "get", MagicMock(return_value=fake_response(SAMPLE_CHECKPOINT)))
    result = main.get_latest_checkpoint(debug=True)
    assert result == SAMPLE_CHECKPOINT
    saved = json.loads((tmp_path / "checkpoint.json").read_text())
    assert saved == SAMPLE_CHECKPOINT


def test_inclusion_success(monkeypatch, tmp_path, capsys):
    artifact = tmp_path / "artifact.md"
    artifact.write_text("hello")

    body = {"spec": {"signature": {"content": base64.b64encode(b"sig").decode(),
                                    "publicKey": {"content": base64.b64encode(b"cert").decode()}}}}
    
    encoded_body = base64.b64encode(json.dumps(body).encode()).decode()
    entry = {"uuid123": {"body": encoded_body, "verification": {"inclusionProof": {"logIndex": 1,
                                                                                    "treeSize": 2,
                                                                                    "hashes": ["00" * 32],
                                                                                    "rootHash": "11" * 32}}}}

    monkeypatch.setattr(main, "get_log_entry", MagicMock(return_value=entry))
    monkeypatch.setattr(main, "extract_public_key", MagicMock(return_value=b"pem"))
    verify_sig = MagicMock()
    verify_incl = MagicMock()
    monkeypatch.setattr(main, "verify_artifact_signature", verify_sig)
    monkeypatch.setattr(main, "verify_inclusion", verify_incl)

    main.inclusion(1, str(artifact))

    verify_sig.assert_called_once()
    verify_incl.assert_called_once()
    assert "Offline verification successful" in capsys.readouterr().out


def test_consistency_success(monkeypatch, capsys):
    proof_payload = {"hashes": ["aa" * 32]}
    get = MagicMock(side_effect=[fake_response(SAMPLE_CHECKPOINT), fake_response(proof_payload)])
    monkeypatch.setattr(main.requests, "get", get)
    verify_cons = MagicMock()
    monkeypatch.setattr(main, "verify_consistency", verify_cons)

    prev = {"treeID": "1193050959916656506", "treeSize": 1000, "rootHash": "cd" * 32}
    main.consistency(prev)

    verify_cons.assert_called_once()
    assert "Consistency verification successful" in capsys.readouterr().out
    

def test_cli_checkpoint_prints_json(monkeypatch, capsys):
    monkeypatch.setattr(main, "get_latest_checkpoint", MagicMock(return_value=SAMPLE_CHECKPOINT))
    monkeypatch.setattr(sys, "argv", ["main.py", "-c"])
    main.main()
    out = json.loads(capsys.readouterr().out)
    assert out["treeID"] == SAMPLE_CHECKPOINT["treeID"]


def test_cli_inclusion_without_artifact_prints_message(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "--inclusion", "1"])
    main.main()
    assert "artifact" in capsys.readouterr().out.lower()


def test_cli_consistency_without_tree_id_prints_message(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["main.py", "--consistency"])
    main.main()
    assert "tree id" in capsys.readouterr().out.lower()