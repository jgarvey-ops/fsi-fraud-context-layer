from dataclasses import dataclass


@dataclass(frozen=True)
class ScaleProfile:
    name: str
    n_customers: int
    n_entities: int
    n_transactions: int
    replay_windows: int
    events_per_window: int


SCALES: dict[str, ScaleProfile] = {
    "small": ScaleProfile(
        name="small",
        n_customers=500,
        n_entities=50,
        n_transactions=100_000,
        replay_windows=24,
        events_per_window=5,
    ),
    "medium": ScaleProfile(
        name="medium",
        n_customers=5_000,
        n_entities=500,
        n_transactions=1_000_000,
        replay_windows=288,
        events_per_window=10,
    ),
}
