# SPDX-FileCopyrightText: © 2019 The Tanuga Authors
# SPDX-License-Identifier: Apache-2.0
"""Tanuga Cache singleton."""

import functools

import cachecontrol
import cachecontrol.caches.file_cache
import requests


@functools.lru_cache(maxsize=1)
def cache_session() -> requests.session:
    return cachecontrol.CacheControl(
        requests.session(), cache=cachecontrol.caches.file_cache.FileCache(".web_cache")
    )


def get(url: str) -> requests.Response:
    return cache_session().get(url)
