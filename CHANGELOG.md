# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-14

### Added
- Initial release
- `FgpServer` - Concurrent connection handling with tokio
- `FgpService` trait - Implement to create custom daemons
- `FgpClient` - Async client for calling daemons
- NDJSON protocol implementation
- Built-in methods: health, methods, stop
- Socket management utilities
- Graceful shutdown handling
