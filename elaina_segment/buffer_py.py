from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from . import SEPARATORS, Runes, Segment, build_runes, segment, Quoted, UnmatchedQuoted
from .err import OutOfData

T = TypeVar("T")


@dataclass
class SegmentToken(Generic[T]):
    buffer: Buffer[T]
    val: Segment[T]
    tail: Callable[[], Runes[T]] | None = None

    def apply(self):
        if self.tail is not None:
            self.buffer.runes = self.tail()
        else:
            self.buffer.runes = []


@dataclass
class AheadToken(Generic[T]):
    buffer: Buffer[T]
    val: Segment[T]

    def apply(self):
        self.buffer.ahead.popleft()


class Buffer(Generic[T]):
    runes: Runes[T]
    ahead: deque[Segment[T]]

    def __init__(self, data: list[str | T], runes: bool = True):
        self.runes = data
        self.ahead = deque()

        if runes:
            self._to_runes()

    def _to_runes(self):
        self.runes = build_runes(self.runes)

    def __repr__(self) -> str:
        return f"Buffer({self.runes}, ahead={self.ahead})"

    def copy(self) -> Buffer[T]:
        return Buffer(self.runes.copy(), runes=False)

    def next(self, until: str = SEPARATORS) -> SegmentToken[T] | AheadToken[T]:
        if self.ahead:
            # NOTE: 在这一层其实上报 source = ahead。
            val = self.ahead[0]
            return AheadToken(self, val)

        res = segment(self.runes, until)
        if res is None:
            raise OutOfData

        val, tail = res
        return SegmentToken(self, val, tail)

    def pushleft(self, *segments: Segment[T]):
        s = []
        for seg in segments:
            if isinstance(seg, (UnmatchedQuoted, Quoted)):
                s.append(str(seg))
            elif seg:  # NOTE: 仅当 seg 不为空时才添加。
                s.append(seg)
        
        self.runes = build_runes(s) + self.runes

    def add_to_ahead(self, val: Segment[T]):
        self.ahead.appendleft(val)

    def first(self) -> Runes[T]:
        return self.runes[0]
