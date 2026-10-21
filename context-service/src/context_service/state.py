from dataclasses import dataclass, field


@dataclass
class RuntimeState:
    stream_injection_enabled: bool = False
    injected_events: list[dict] = field(default_factory=list)


runtime = RuntimeState()
