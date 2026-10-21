from pathlib import Path

from fraud_synthetic.generate import DEMO_CASES, generate_pack


def test_generate_small_deterministic(tmp_path: Path) -> None:
    m1 = generate_pack(tmp_path / "a", scale="small", seed=7)
    m2 = generate_pack(tmp_path / "b", scale="small", seed=7)
    assert m1 == m2
    assert m1["counts"]["customers"] == 500
    assert (tmp_path / "a" / "historic" / "gold_cases.jsonl").is_file()
    assert (tmp_path / "a" / "replay" / "win-00000.jsonl").is_file()


def test_demo_case_ids_present(tmp_path: Path) -> None:
    generate_pack(tmp_path, scale="small", seed=42)
    text = (tmp_path / "historic" / "gold_cases.jsonl").read_text()
    for case in DEMO_CASES:
        assert case["case_id"] in text
