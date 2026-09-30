# PhoneFarm experimental WDA build

Build-only repository. No phone data, media, device identifiers or signing credentials belong here.

GitHub Actions builds unsigned WDA 8.9.1 with Git-Agni's Photos import and sessionless-button patches from pinned revisions. The artifact requires local signing and compatibility testing before installation. It does not post anything and is not a production-approved build.

Upstream source: https://github.com/appium/WebDriverAgent (Apache-2.0).
Patches: https://github.com/Git-Agni/prod-FARM-IOS-Core (Apache-2.0).
Upstream license and notice files are packaged with the artifact.

The import endpoint is experimental: it does not provide durable idempotency. Never blindly retry an import after a timeout. Keep forwarding local; do not expose WDA to the Internet.
