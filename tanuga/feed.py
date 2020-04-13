# SPDX-FileCopyrightText: © 2019 The Tanuga Authors
# SPDX-License-Identifier: Apache-2.0
"""Tanuga Feed objects."""

from typing import Any, Optional, Sequence


class Feed:
    configured_url: str
    fetch_url: Optional[str]

    def __init__(self, url: str) -> None:
        self.configured_url = url

    def get_title(self) -> str:
        raise NotImplemented

    def refresh(self) -> None:
        raise NotImplemented

    def force_fetch(self) -> None:
        raise NotImplemented

    def parse(self) -> None:
        raise NotImplemented

    def get_posts(self, number: int) -> Sequence[Any]:
        raise NotImplemented
