# Changelog

## [5.0.0](https://github.com/leovan/SciHubEVA/compare/v4.1.1...v5.0.0) (2021-06-20)

### Breaking Changes

- Change Qt Python binding from PySide2 to PySide6.

## [4.1.1](https://github.com/leovan/SciHubEVA/compare/v4.1.0...v4.1.1) (2020-10-22)

### Bug Fixes

- Fix dialog auto width problem.
- Fix high DPI scaling problem on Windows.

## [4.1.0](https://github.com/leovan/SciHubEVA/compare/v4.0.1...v4.1.0) (2020-10-19)

### Features

- Restore preferences after a new version installed.

### Bug Fixes

- Fix network retry times and proxy.

## [4.0.1](https://github.com/leovan/SciHubEVA/compare/v4.0.0...v4.0.1) (2020-05-05)

### Features

- Center windows based on parent.

## [4.0.0](https://github.com/leovan/SciHubEVA/compare/v3.2.3...v4.0.0) (2020-05-02)

### Features

- More modern preference dialog.
- Invert captcha image when dark theme is enabled.

## [3.2.3](https://github.com/leovan/SciHubEVA/compare/v3.2.2...v3.2.3) (2019-10-29)

### Features

- Add log file, right clicking log area can popup menu to open log file or log directory. ([#21](https://github.com/leovan/SciHubEVA/issues/21))

### Bug Fixes

- Fix illegal filename on Windows. ([#20](https://github.com/leovan/SciHubEVA/issues/20))

## [3.2.2](https://github.com/leovan/SciHubEVA/compare/v3.2.1...v3.2.2) (2019-10-12)

### Features

- Add PMID and DOI filename keywords. ([#17](https://github.com/leovan/SciHubEVA/issues/17))

### Bug Fixes

- Fix OpenGL problem. ([#18](https://github.com/leovan/SciHubEVA/issues/18))

## [3.2.1](https://github.com/leovan/SciHubEVA/compare/v3.2.0...v3.2.1) (2019-09-26)

_This is a hotfix version._

### Bug Fixes

- Fix captcha handling bug.

## [3.2.0](https://github.com/leovan/SciHubEVA/compare/v3.1.2...v3.2.0) (2019-09-26)

### Features

- Support doing not overwrite existing file when downloading.

### Bug Fixes

- Fix captcha display bug due to the temporary file problem on Windows. ([#14](https://github.com/leovan/SciHubEVA/issues/14)) ([#16](https://github.com/leovan/SciHubEVA/issues/16))

## [3.1.2](https://github.com/leovan/SciHubEVA/compare/v3.1.1...v3.1.2) (2019-09-10)

### Bug Fixes

- Fix captcha display bug. ([#13](https://github.com/leovan/SciHubEVA/issues/13))

## [3.1.1](https://github.com/leovan/SciHubEVA/compare/v3.1.0...v3.1.1) (2019-08-11)

### Features

- Add buttons and keys binding.

### Bug Fixes

- Fix socks proxy bugs. ([#12](https://github.com/leovan/SciHubEVA/issues/12))

## [3.1.0](https://github.com/leovan/SciHubEVA/compare/v3.0.0...v3.1.0) (2019-08-08)

### Features

- Support range pattern in query.

### Bug Fixes

- Fix captcha handling bugs.

### Tests

- Add a fake server to test different situations. ([#11](https://github.com/leovan/SciHubEVA/issues/11))

## [3.0.0](https://github.com/leovan/SciHubEVA/compare/v2.1.2...v3.0.0) (2019-08-04)

### Features

- Support downloading with query list file. ([#10](https://github.com/leovan/SciHubEVA/issues/10))
- Add SciHubEVA as a brew cask formula. (Thanks [@womeimingzi11](https://github.com/womeimingzi11))

## [2.1.2](https://github.com/leovan/SciHubEVA/compare/v2.1.1...v2.1.2) (2019-06-04)

### Features

- Change to new icon.

### Bug Fixes

- Fix building with PyInstaller against PySide2 5.12.3+.
- Fix some bugs.

## [2.1.1](https://github.com/leovan/SciHubEVA/compare/v2.1.0...v2.1.1) (2019-03-27)

### Bug Fixes

- Fix some small bugs.

## [2.1.0](https://github.com/leovan/SciHubEVA/compare/v2.0.1...v2.1.0) (2019-01-16)

### Features

- Fully support dark theme in macOS ("System" option now works).

## [2.0.1](https://github.com/leovan/SciHubEVA/compare/v2.0.0...v2.0.1) (2019-01-09)

### Bug Fixes

- Fix url without scheme error. ([#8](https://github.com/leovan/SciHubEVA/issues/8))
- Add OpenGL libraries on Windows. ([#1](https://github.com/leovan/SciHubEVA/issues/1))

## [2.0.0](https://github.com/leovan/SciHubEVA/compare/v1.3.0...v2.0.0) (2018-12-22)

### Features

- Support dark theme (Change it in "Preferences", "System" option does not work currently).
- Add Traditional Chinese support.

### Breaking Changes

- Change Qt Python binding from [PyQt5](https://www.riverbankcomputing.com/software/pyqt) to [PySide2](https://doc.qt.io/qtforpython).
- Change Windows installer builder from [NSIS](https://nsis.sourceforge.io) to [Inno Setup](http://www.jrsoftware.org/isinfo.php).
- Change Material Design Icons from [Google](https://github.com/google/material-design-icons) to [Community](https://github.com/templarian/MaterialDesign/).


## [1.3.0](https://github.com/leovan/SciHubEVA/compare/v1.2.0...v1.3.0) (2018-08-03)

### Features

- Enhance dealing with HTTP response, e.g. response may be open access article page rather than captcha page.
- Add feature of opening links in logs.

## [1.2.0](https://github.com/leovan/SciHubEVA/compare/v1.1.0...v1.2.0) (2018-07-07)

### Features

- Add preference button on the main window for env without menu (e.g. Linux).
- Remove retry with different Sci-Hub URLs.

### Bug Fixes

- Allow user enter captcha. ([#5](https://github.com/leovan/SciHubEVA/issues/5))

## [1.1.0](https://github.com/leovan/SciHubEVA/compare/v1.0.1...v1.1.0) (2018-06-16)

### Features

- Update Sci-Hub API which supports search string now.

### Bug Fixes

- Fix issue PDF metadata fetching error. ([#2](https://github.com/leovan/SciHubEVA/issues/2))

## [1.0.1](https://github.com/leovan/SciHubEVA/compare/v1.0.0...v1.0.1) (2018-05-28)

### Features

- Change placeholder of query which makes it more clear.
- Add Windows x86 version.

## 1.0.0 (2018-05-19)

### Features

- First release version.
