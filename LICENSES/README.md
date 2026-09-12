# Third-Party Licenses

This directory contains license texts for third-party software used by or
distributed with `reminder_on_desktop`.

These license files do **not** replace or modify the MIT License in the root
of this repository. The root `LICENSE` file applies to the original source
code of `reminder_on_desktop` for which the project author holds the
applicable copyright.

Third-party software remains subject to its own license terms, copyright
notices, attribution requirements, and redistribution conditions.

For package-specific notices and trademark information, see:

[`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md)

---

## License Files

| License file                           | License                                | Components associated with this project  |
| -------------------------------------- | -------------------------------------- | ---------------------------------------- |
| [`Apache-2.0.txt`](Apache-2.0.txt)     | Apache License 2.0                     | `requests`, `tzdata`                     |
| [`BSD-2-Clause.txt`](BSD-2-Clause.txt) | BSD 2-Clause License                   | `icalendar`                              |
| [`MIT.txt`](MIT.txt)                   | MIT License                            | `winotify`                               |
| [`LGPL-3.0.txt`](LGPL-3.0.txt)         | GNU Lesser General Public License v3.0 | `recurring-ical-events`, `x-wr-timezone` |
| [`GPL-3.0.txt`](GPL-3.0.txt)           | GNU General Public License v3.0        | Included together with LGPLv3            |

---

## Apache License 2.0

`Apache-2.0.txt` contains the Apache License 2.0 text.

Components associated with this project that use the Apache License 2.0
include:

* `requests`
* `tzdata`

These components are licensed separately from `reminder_on_desktop`.

Any component-specific copyright notices or NOTICE files supplied by an
upstream project must also be preserved when required by that project's
license.

---

## BSD 2-Clause License

`BSD-2-Clause.txt` contains the BSD 2-Clause License text applicable to the
`icalendar` package.

The license applies to `icalendar`, not to the original source code of
`reminder_on_desktop`.

---

## MIT License

`MIT.txt` contains the MIT License applicable to the `winotify` package.

This file is separate from the root `LICENSE` file.

Although both `winotify` and `reminder_on_desktop` use the MIT License, they
are separate copyrighted works and their respective copyright notices must
be preserved.

---

## GNU LGPL v3 and GNU GPL v3

`recurring-ical-events` and `x-wr-timezone` are licensed under the GNU Lesser
General Public License version 3 or later.

The GNU LGPL version 3 incorporates the terms and conditions of version 3 of
the GNU General Public License and supplements them with additional
permissions.

For this reason, this directory contains both:

* [`LGPL-3.0.txt`](LGPL-3.0.txt)
* [`GPL-3.0.txt`](GPL-3.0.txt)

Including these license texts does **not** cause the original source code of
`reminder_on_desktop` to become licensed under the GPL or LGPL.

The original project code remains licensed under the MIT License.

However, distributors of executable builds that include LGPL-covered
libraries are responsible for complying with the applicable LGPL
requirements for those libraries and any Combined Work.

---

## Direct and Transitive Dependencies

The source code of `reminder_on_desktop` directly uses or may use packages
including:

* `winotify`
* `requests`
* `icalendar`
* `recurring-ical-events`

Installing those packages may also install additional dependencies.

For example, current versions of the iCalendar-related packages may install
components including:

* `python-dateutil`
* `tzdata`
* `x-wr-timezone`
* `typing-extensions`, depending on the Python version
* other version-specific dependencies

The exact dependency set may change as upstream packages are updated.

The license files currently stored in this directory should therefore not
be interpreted as a complete list of every license that may apply to every
possible environment or executable build.

---

## Source Distribution vs. Executable Distribution

When users install dependencies themselves through `pip`, those third-party
packages are distributed and installed separately and retain their own
licenses.

A compiled or packaged executable may bundle Python, third-party packages,
runtime libraries, and other components into the distribution.

The exact components included in an executable can vary according to:

* Python version;
* package versions;
* operating system;
* packaging tool;
* packaging configuration; and
* optional dependencies.

Before publishing a new executable release, the distributor should inspect
the packages actually contained in that build and verify the license and
notice requirements for each bundled component.

Additional license files may need to be added to this directory for a
particular executable release.

---

## Google Calendar

Google Calendar is an external service and is not software distributed under
the license files in this directory.

Google, Google Calendar, and related names and marks are trademarks of Google
LLC.

`reminder_on_desktop` is an unofficial third-party project and is not
affiliated with, sponsored by, approved by, or endorsed by Google LLC.

References to Google Calendar are used solely to describe compatibility and
interoperability.

---

## Project License

Except for separately licensed third-party software and other third-party
intellectual property, the original source code of `reminder_on_desktop` is
licensed under the MIT License.

See:

* [`../LICENSE`](../LICENSE) — license for the original project code.
* [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) — third-party
  software, attribution, and trademark notices.
