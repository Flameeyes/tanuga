#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: © 2019 The Tanuga Authors
# SPDX-License-Identifier: Apache-2.0

import flask

from tanuga import tanuga

web_app = flask.Flask(__name__, static_url_path=None)
logic_app = tanuga.Tanuga()


if __name__ == "__main__":
    web_app.run(host="localhost", port=8080, debug=True)
