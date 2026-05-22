# Development Style

Shared implementation rules for Obelisk projects.

## Engineering Defaults

- Reuse local patterns before adding a new abstraction.
- Keep auth and relay-derived data flowing through the established bridge or SDK session layer.
- Add tests at the risk boundary: auth, storage, event signing, relay state, and admin mutations deserve focused coverage.
- Keep docs close to behavior. Product-specific specs stay in product repos; cross-project policy belongs here.

## Canonical Pages

- [Frontend](frontend.md)
- [Docs and specs](docs-and-specs.md)
