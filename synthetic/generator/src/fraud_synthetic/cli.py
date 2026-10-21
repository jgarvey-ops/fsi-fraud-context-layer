import os

import click

from fraud_synthetic.generate import generate_pack


@click.group()
def main() -> None:
    """Fraud context synthetic data generator."""


@main.command("generate")
@click.option("--out", "out_dir", type=click.Path(path_type=str), required=True)
@click.option("--scale", default=None, help="small | medium (default: env GENERATOR_SCALE or small)")
@click.option("--seed", default=None, type=int, help="RNG seed (default: env GENERATOR_SEED or 42)")
def generate_cmd(out_dir: str, scale: str | None, seed: int | None) -> None:
    """Write historic + replay ledger under OUT."""
    from pathlib import Path

    scale = scale or os.environ.get("GENERATOR_SCALE", "small")
    seed = seed if seed is not None else int(os.environ.get("GENERATOR_SEED", "42"))
    manifest = generate_pack(Path(out_dir), scale=scale, seed=seed)
    click.echo(f"Generated scale={manifest['scale']} -> {out_dir}")
    click.echo(f"Demo cases: {', '.join(manifest['demo_cases'])}")


if __name__ == "__main__":
    main()
