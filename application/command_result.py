from dataclasses import dataclass, field

from domain.event import Event


@dataclass(frozen=True)
class CommandResult:
    success: bool = True
    events: list[Event] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.success

    def __str__(self) -> str:
        return f"CommandResult(success={self.success}, events={self.events})"
