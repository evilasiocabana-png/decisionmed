# PsychRx Protected Web Deployment

## Target architecture

The recommended public entry point is a dedicated subdomain such as
`app.psiquiatriaemfoco.com`. The WordPress site links to that subdomain while the
PsychRx service hosts both the interface and its API under the same protected
origin.

The initial personal pilot uses the free hosting plan and a single shared
password. It does not persist consultations or patient records.

## Required secrets

- `PSYCHRX_AUTH_REQUIRED=true`
- `PSYCHRX_ACCESS_PASSWORD=<access password with at least 8 characters>`
- `PSYCHRX_SESSION_SECRET=<random secret with at least 32 characters>`
- `PSYCHRX_SESSION_TTL_SECONDS=28800` (optional; default is eight hours)

Secrets must be configured in the hosting dashboard. They must never be written
to the repository, source code, deployment logs or WordPress.

## Start command

```text
python -m interfaces.web.server
```

The process reads `PORT` from the hosting environment and binds to `0.0.0.0`
when running in protected mode.

## Security boundary

- `/health` is public and contains no patient data.
- `/login` is public.
- The interface, static assets and every `/api/*` endpoint require a valid,
  signed session cookie.
- Sessions expire automatically and contain no clinical or patient data.
- Deployment must use HTTPS.
- Production access should initially be limited to authorized clinicians.

## WordPress integration

Create a protected menu entry or page in WordPress that links to the PsychRx
subdomain. The security boundary remains in PsychRx itself; protecting only the
WordPress page is insufficient because it would leave the API URL exposed.

## Production limitations

This password gate is suitable for a controlled pilot. Individual user
accounts, role-based access, audit trails, password reset and stronger identity
management remain required before broad clinical production use.
