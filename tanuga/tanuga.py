# SPDX-FileCopyrightText: © 2019 The Tanuga Authors
# SPDX-License-Identifier: Apache-2.0
"""Tanuga main logic."""

from typing import MutableSequence

from . import feed


class Tanuga:

    feeds = MutableSequence[feed.Feed]

    def add_feed(self, url: str) -> None:
        feeds.append(feed.Feed(url))
