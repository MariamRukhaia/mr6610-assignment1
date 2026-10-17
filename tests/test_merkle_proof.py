import base64
import hashlib
import pytest
from merkle_proof import (DefaultHasher, RootMismatchError,
                            compute_leaf_hash, verify_consistency, verify_inclusion, verify_match)

def _leaf(d):
    return hashlib.sha256(b"\x00" + d).digest()


def _node(l, r):
    return hashlib.sha256(b"\x01" + l + r).digest()


h0, h1, h2, h3 = (_leaf(x) for x in (b"a", b"b", b"c", b"d"))
n01, n23 = _node(h0, h1), _node(h2, h3)
root4 = _node(n01, n23)


def test_consistency_one_to_two():
    verify_consistency(DefaultHasher, 1, 2, [h1.hex()], h0.hex(), n01.hex())


def test_consistency_two_to_four():
    verify_consistency(DefaultHasher, 2, 4, [n23.hex()], n01.hex(), root4.hex())


def test_consistency_from_empty_tree():
    verify_consistency(DefaultHasher, 0, 4, [], h0.hex(), root4.hex())


def test_inclusion_four_leaf_tree():
    verify_inclusion(DefaultHasher, 2, 4, h2.hex(), [h3.hex(), n01.hex()], root4.hex())


def test_compute_leaf_hash():
    body = base64.b64encode(b"hello").decode()
    expected = hashlib.sha256(b"\x00hello").hexdigest()

    assert compute_leaf_hash(body) == expected


def test_empty_root():
    expected = hashlib.sha256(b"").digest()

    assert DefaultHasher.empty_root() == expected


def test_hash_leaf():
    expected = hashlib.sha256(b"\x00hello").digest()

    assert DefaultHasher.hash_leaf(b"hello") == expected


def test_hash_children():
    left = b"left"
    right = b"right"
    expected = hashlib.sha256(b"\x01" + left + right).digest()

    assert DefaultHasher.hash_children(left, right) == expected


def test_verify_match_success():
    verify_match(b"same", b"same")


def test_verify_match_failure():
    with pytest.raises(RootMismatchError):
        verify_match(b"first", b"second")


def test_inclusion_single_leaf():
    leaf = DefaultHasher.hash_leaf(b"hello")

    verify_inclusion(
        DefaultHasher, 0, 1, leaf.hex(), [], leaf.hex()
    )


def test_inclusion_invalid_index():
    leaf = DefaultHasher.hash_leaf(b"hello")

    with pytest.raises(ValueError):
        verify_inclusion(
            DefaultHasher, 1, 1, leaf.hex(), [], leaf.hex()
        )


def test_inclusion_wrong_root():
    leaf = DefaultHasher.hash_leaf(b"hello")
    wrong_root = bytes(32).hex()

    with pytest.raises(RootMismatchError):
        verify_inclusion(
            DefaultHasher, 0, 1, leaf.hex(), [], wrong_root
        )


def test_consistency_equal_trees():
    root = DefaultHasher.hash_leaf(b"hello").hex()

    verify_consistency(DefaultHasher, 1, 1, [], root, root)


def test_consistency_decreasing_size():
    root = DefaultHasher.hash_leaf(b"hello").hex()

    with pytest.raises(ValueError):
        verify_consistency(DefaultHasher, 2, 1, [], root, root)


def test_consistency_equal_size_wrong_roots():
    root1 = DefaultHasher.hash_leaf(b"hello").hex()
    root2 = DefaultHasher.hash_leaf(b"world").hex()

    with pytest.raises(RootMismatchError):
        verify_consistency(DefaultHasher, 1, 1, [], root1, root2)