# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## 1.0.0

### Changed

- Using [mitmproxy](https://mitmproxy.org/) instead of FastAPI

## 0.2.0

### Added

- `/tndetails` endpoint to return details about a TN
  - Currently only returns `CampaignFullyProvisioned` = `true`

### Changed

- `/new` endpoint renamed to `messages` to line up with the Bandwidth API

## 0.1.0

### Added

- Initial commit
- New commands:
  - `in:med-txt`
  - `in:med`
  - `in:mult`

