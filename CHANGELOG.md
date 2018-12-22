# Changelog

## [2.0.0](https://github.com/leovan/SciHubEVA/compare/v1.3.0...v2.0.0) (2018-12-22)

### Features

- Support dark theme (Change it in "Preferences", "System" option does not work currently).
- Add Traditional Chinese support.

---

- 支持暗色主题 (请在“配置”中进行修改，“System”选项暂不可用)。
- 增加繁体中文支持。

### Breaking changes

- Change Qt Python binding from [PyQt5](https://www.riverbankcomputing.com/software/pyqt) to [PySide2](https://doc.qt.io/qtforpython).
- Change Windows installer builder from [NSIS](https://nsis.sourceforge.io) to [Inno Setup](http://www.jrsoftware.org/isinfo.php).
- Change Material Design Icons from [Google](https://github.com/google/material-design-icons) to [Community](https://github.com/templarian/MaterialDesign/).

---

- 替换 Qt 的 Python 绑定 [PyQt5](https://www.riverbankcomputing.com/software/pyqt) 为 [PySide2](https://doc.qt.io/qtforpython)。
- 替换 Windows 安装构建器 [NSIS](https://nsis.sourceforge.io) 为 [Inno Setup](http://www.jrsoftware.org/isinfo.php)。
- 替换 Material Design 图标 [Google](https://github.com/google/material-design-icons) 为 [Community](https://github.com/templarian/MaterialDesign/)。


## [1.3.0](https://github.com/leovan/SciHubEVA/compare/v1.2.0...v1.3.0) (2018-08-03)

### Features

- Enhance dealing with HTTP response, e.g. response may be open access article page rather than captcha page.
- Add feature of opening links in logs.

---

- 增强对 HTTP 响应的处理，例如响应可能是开放文章页面而非验证码页面。
- 添加在日志中打开链接功能。

## [1.2.0](https://github.com/leovan/SciHubEVA/compare/v1.1.0...v1.2.0) (2018-07-07)

### Features

- Add preference button on the main window for env without menu (e.g. Linux).
- Remove retry with different Sci-Hub URLs.

---

- 在主界面上添加配置按钮，便于无菜单环境用户使用 (例如：Linux)。
- 删除利用不同 Sci-Hub 网址进行重试方案。

### Bug Fixes

- Allow user enter captcha. ([#5](https://github.com/leovan/SciHubEVA/issues/5))

---

- 允许用户输入验证码。([#5](https://github.com/leovan/SciHubEVA/issues/5))

## [1.1.0](https://github.com/leovan/SciHubEVA/compare/v1.0.1...v1.1.0) (2018-06-16)

### Features

- Update Sci-Hub API which supports search string now.

---

- 更新 Sci-Hub API，支持搜索标题。

### Bug Fixes

- Fix issue PDF metadata fetching error. ([#2](https://github.com/leovan/SciHubEVA/issues/2))

---

- 修复获取 PDF 元信息时错误。([#2](https://github.com/leovan/SciHubEVA/issues/2))

## [1.0.1](https://github.com/leovan/SciHubEVA/compare/v1.0.0...v1.0.1) (2018-05-28)

### Features

- Change placeholder of query which makes it more clear.
- Add Windows x86 version.

---

- 更新搜索框占位符，可搜索类型更加清晰明了。
- 添加 Windows x86 版本。

## 1.0.0 (2018-05-19)

### Features

- First release version.

---

- 第一个发行版本。
