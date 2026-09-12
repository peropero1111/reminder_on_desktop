# Third-Party Licenses

This directory contains license texts used by third-party software associated
with `calendar_widget_on_desktop`.

These files do **not** replace or modify the MIT License in the root of the
repository. The root `LICENSE` file applies to the original source code of
`calendar_widget_on_desktop` for which the project author holds the applicable
copyright.

For package-specific notices and trademark information, also see
[`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

---

## License Files

| License file | License | Components currently associated with this project |
|---|---|---|
| [`Apache-2.0.txt`](Apache-2.0.txt) | Apache License 2.0 | `requests`, `tzdata` |
| [`BSD-2-Clause.txt`](BSD-2-Clause.txt) | BSD 2-Clause License | `icalendar` |
| [`MIT.txt`](MIT.txt) | MIT License | `winotify` |
| [`LGPL-3.0.txt`](LGPL-3.0.txt) | GNU Lesser General Public License v3.0 | `recurring-ical-events`, `x-wr-timezone` |
| [`GPL-3.0.txt`](GPL-3.0.txt) | GNU General Public License v3.0 | Included because LGPLv3 incorporates GPLv3 |

---

## Apache License 2.0

`Apache-2.0.txt` contains the standard Apache License 2.0 text.

The packages currently identified in this project that use this license
include:

- `requests`
- `tzdata`

Any package-specific copyright or NOTICE information supplied by an upstream
package must also be preserved when required by that package's distribution.

---

## BSD 2-Clause License

`BSD-2-Clause.txt` contains the license text supplied by the upstream
`icalendar` project, including its copyright notice:

> Copyright (c) 2012-2013, Plone Foundation

The license applies to `icalendar`, not to the original source code of
`calendar_widget_on_desktop`.

---

## MIT License

`MIT.txt` contains the license text supplied by the upstream `winotify`
project, including its copyright notice:

> Copyright (c) 2021 Versa Syahputra

This file is separate from the root `LICENSE` file. Both use the MIT License,
but they cover different copyrighted works.

---

## GNU LGPL v3 and GNU GPL v3

`recurring-ical-events` and `x-wr-timezone` are licensed under the GNU Lesser
General Public License version 3 or later.

The LGPLv3 explicitly incorporates the terms and conditions of version 3 of
the GNU General Public License and adds additional permissions. Therefore this
directory includes both:

- `LGPL-3.0.txt`
- `GPL-3.0.txt`

Including these license texts does not change the license of the original
`calendar_widget_on_desktop` source code from MIT to GPL or LGPL.

When an executable distribution combines this project with LGPL-covered
libraries, the distributor is responsible for satisfying the applicable LGPL
requirements, including the requirements that apply to Combined Works.

---

## Source Distribution vs. Executable Distribution

When users install dependencies themselves with `pip`, third-party packages
are installed as separately distributed packages and retain their own
licenses.

A packaged executable may bundle those packages together with additional
dependencies. The exact set of bundled packages can vary depending on:

- package versions;
- Python version;
- operating system;
- the packaging tool and configuration; and
- optional dependencies selected during the build.

For this reason, this directory should be reviewed whenever a new executable
release is built.

Dependencies pulled in transitively by packages such as `requests`,
`icalendar`, and `recurring-ical-events` may require additional license texts
or notices that are not represented by the five license files currently in
this directory.

---

## Project License

The original source code of `calendar_widget_on_desktop` remains licensed
under the MIT License.

See:

- [`../LICENSE`](../LICENSE) — license for the original project code.
- [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) — package notices,
  attribution information, and trademark notices.
