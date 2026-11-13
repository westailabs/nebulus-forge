# Security policy

## Reporting a vulnerability

Please do not open a public issue. Use GitHub's private vulnerability reporting on this repository (Security tab, "Report a vulnerability"), or contact the maintainers through [West AI Labs](https://westailabs.com).

Include what you found, how to reproduce it, and the affected commit or version. You should hear back within a few days.

## Handling credentials

- Never commit credentials, tokens, or `.env` files. Use the `*.example` files as templates.
- If a credential is committed by mistake, treat it as exposed: revoke and rotate it first, then remove it from the repository.
