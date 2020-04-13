# SPDX-FileCopyrightText: © 2019 The Tanuga Authors
# SPDX-License-Identifier: Apache-2.0
"""Tanuga Feed objects."""

import datetime
import logging
from typing import Any, Optional, Sequence

import requests

DEFAULT_REFRESH_DELTA = datetime.timedelta(minutes=2)


class Feed:
    configured_url: str
    fetch_url: Optional[str]
    last_fetched: Optional[datetime.datetime] = None
    _refresh_delta: Optional[datetime.timedelta] = None

    def __init__(self, url: str, refresh_delta: Optional[datetime.timedelta]) -> None:
        self.configured_url = url
        self.fetch_url = url
        self._refresh_delta = refresh_delta

    def get_title(self) -> str:
        raise NotImplemented

    def ready_for_refresh(self) -> bool:
        # Never (successfully) fetched before.
        if self.last_fetched is None:
            return True

        refresh_delta = self._refresh_delta or DEFAULT_REFRESH_DELTA
        refresh_datetime = self.last_fetched + refresh_delta
        return refresh_datetime < datetime.datetime.now()

    def refresh(self) -> None:
        if self.ready_for_refresh():
            self.force_fetch()
        else:
            logging.info("%s is already fresh.", self.configured_url)

    def force_fetch(self) -> None:
        response = requests.get(self.fetch_url)
        response.raise_for_status()

        # We want to make sure to cache (at the very least in the current session) any
        # permanent redirect, to avoid incurring their cost again. The way we do that is
        # to look for the first non-permanent redirect in the response history. This
        # works because, if there's no redirect, the current URL is still valid. So the
        # conditions of either all redirects being permanent, or no redirect to be
        # present, are the same: the final URL is the one we want.
        #
        # This should work both in case of P→T→F and in case of T→P→F, as the first
        # non-temporary is the one we care about.
        temporary_redirects = [
            redirect
            for redirect in response.history
            if not redirect.is_permanent_redirect
        ]

        last_hop = temporary_redirects[0] if temporary_redirects else response

        if last_hop.url != self.fetch_url:
            logging.info(
                "Recording a permanent redirection from %s to %s",
                self.fetch_url,
                last_hop.url,
            )
            self.fetch_url = last_hop.url

        self.last_fetched = datetime.datetime.now()

    def parse(self) -> None:
        raise NotImplemented

    def get_posts(self, number: int) -> Sequence[Any]:
        raise NotImplemented
