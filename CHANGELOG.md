# Changelog

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

### Breaking changes

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
