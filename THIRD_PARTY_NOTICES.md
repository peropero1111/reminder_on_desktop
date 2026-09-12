# THIRD-PARTY SOFTWARE AND TRADEMARK NOTICES

This document provides notices for third-party software and services used by
`reminder_on_desktop`.

The MIT License in the root of this repository applies to the original source
code of `reminder_on_desktop` for which the project author holds the
applicable copyright.

Third-party software, services, trademarks, and other third-party
intellectual property remain subject to their respective licenses, terms,
and rights.

---

## 1. Requests

**Package:** `requests`
**License:** Apache License 2.0
**License text:** [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt)

`reminder_on_desktop` may use Requests to retrieve iCalendar data over HTTP
or HTTPS.

Requests is licensed separately from this project.

The MIT License of `reminder_on_desktop` does not replace or modify the
Apache License 2.0 applicable to Requests.

---

## 2. iCalendar

**Package:** `icalendar`
**License:** BSD 2-Clause License
**License text:** [`LICENSES/BSD-2-Clause.txt`](LICENSES/BSD-2-Clause.txt)

`reminder_on_desktop` may use the `icalendar` package to parse calendar data
in the iCalendar format.

The `icalendar` package is licensed separately from this project.

The MIT License of `reminder_on_desktop` does not replace or modify the
license applicable to `icalendar`.

---

## 3. recurring-ical-events

**Package:** `recurring-ical-events`
**License:** GNU Lesser General Public License v3.0 or later
(`LGPL-3.0-or-later`)
**License text:** [`LICENSES/LGPL-3.0.txt`](LICENSES/LGPL-3.0.txt)
**GNU GPL v3 text:** [`LICENSES/GPL-3.0.txt`](LICENSES/GPL-3.0.txt)

`reminder_on_desktop` may use `recurring-ical-events` to expand and process
recurring events contained in iCalendar data.

This library is licensed separately under the GNU Lesser General Public
License version 3 or later.

The GNU LGPL version 3 incorporates the terms and conditions of version 3 of
the GNU General Public License and supplements them with additional
permissions. Both license texts are therefore included in this repository.

The MIT License of `reminder_on_desktop` does not relicense
`recurring-ical-events`.

---

## 4. winotify

**Package:** `winotify`
**License:** MIT License
**License text:** [`LICENSES/MIT.txt`](LICENSES/MIT.txt)

`reminder_on_desktop` uses `winotify` to display Windows notifications.

`winotify` is separately licensed under the MIT License.

The MIT license text and copyright notice applicable to `winotify` should be
preserved independently from the root MIT License applicable to the original
source code of `reminder_on_desktop`.

---

## 5. x-wr-timezone

**Package:** `x-wr-timezone`
**License:** GNU Lesser General Public License v3.0 or later
(`LGPL-3.0-or-later`)
**License text:** [`LICENSES/LGPL-3.0.txt`](LICENSES/LGPL-3.0.txt)
**GNU GPL v3 text:** [`LICENSES/GPL-3.0.txt`](LICENSES/GPL-3.0.txt)

`x-wr-timezone` may be installed as a dependency of the iCalendar processing
libraries used by this project.

It is licensed separately under the GNU Lesser General Public License
version 3 or later.

Its inclusion as a dependency does not change the MIT License applied to the
original source code of `reminder_on_desktop`.

---

## 6. tzdata

**Package:** `tzdata`
**License:** Apache License 2.0
**License text:** [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt)

`tzdata` may be installed as a dependency of the calendar-processing
libraries used by this project.

It is licensed separately from `reminder_on_desktop`.

---

## 7. Additional Dependencies

The packages listed above may install additional transitive dependencies,
including `python-dateutil` and other version-specific packages.

The exact dependency set depends on the versions of Python and the packages
installed.

Such dependencies retain their own licenses and copyright notices.

Before distributing a compiled or packaged executable, the distributor
should inspect the actual dependencies included in that build and add any
additional license texts or notices required by those components.

---

## 8. Bundled Executable Distributions

Compiled or packaged executable versions of `reminder_on_desktop` may contain
Python, third-party Python packages, runtime components, or other
dependencies.

Each bundled component remains subject to its own:

* license;
* copyright notice;
* attribution requirements; and
* redistribution conditions.

Including a third-party component in an executable does not cause that
component to become licensed under the MIT License of
`reminder_on_desktop`.

Likewise, including an LGPL-covered library does not by itself change the
license of the original `reminder_on_desktop` source code, but distribution
of a Combined Work must comply with the applicable LGPL requirements.

The exact set of bundled components may vary between releases.

---

## 9. Google Calendar and Google Trademarks

`reminder_on_desktop` can use iCalendar data made available through Google
Calendar.

Google, Google Calendar, and related names and marks are trademarks of
Google LLC.

These names are used solely for identification, compatibility, and
interoperability purposes.

`reminder_on_desktop` is an unofficial third-party project.

This project is not affiliated with, sponsored by, approved by, or endorsed
by Google LLC.

Google Calendar and other Google services are subject to Google's own terms,
policies, and conditions.

No Google software or service is licensed under the MIT License of
`reminder_on_desktop`.

---

## Project License

Except for separately licensed third-party software and third-party
intellectual property, the original source code of `reminder_on_desktop` is
distributed under the MIT License.

See the root [`LICENSE`](LICENSE) file for the full project license terms.

For the license texts associated with third-party components, see the
[`LICENSES/`](LICENSES/) directory.
