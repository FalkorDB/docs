# Admin platform architecture

Design decisions behind the Admin Server and Admin UI, and the reasoning that
led to them. This records the *why*. For the *what*, use:

- API surface — [`packages/admin-ui/api.json`](../../packages/admin-ui/api.json) (OpenAPI 3.0)
- Server layering — [`packages/admin-server/src/repositories/README.md`](../../packages/admin-server/src/repositories/README.md)
- Shipped behavior — the published docs under `docs/`

## Kubernetes as the datastore

The Admin Server has no external database. Configuration and identity live in
Kubernetes objects; SQLite holds only the audit trail.

**Why:** it removes an operational dependency from every install. There is no
database to provision, back up, connect-pool, or upgrade alongside the chart.
It also makes the entire configuration surface GitOps-friendly — roles and
settings can be declared in Helm values and reconciled like any other manifest.

**Rejected:** PostgreSQL or MySQL for users, roles, and settings. The write
volume is negligible and the data is small; a database would have added
operational cost without buying anything.

| Data | Stored in |
| --- | --- |
| Users | one Secret per user, named `<prefix><email>` with non-alphanumerics replaced by `-` |
| Roles and rules | ConfigMap, `admin.rbacConfig.configMapName` (default `falkordb-rbac`) |
| Settings and feature flags | ConfigMap, managed by `K8sSettingsRepository` |
| Audit log | SQLite, via Drizzle ORM |
| Deployments, backups, restores, schedules | KubeBlocks CRDs (`apps.kubeblocks.io`, `dataprotection.kubeblocks.io`) |

### One Secret per user

Users are individual Secrets rather than rows in a shared object.

**Why:** Kubernetes RBAC can then be applied per user, users are listable with a
label selector, and metadata (email, display name, active flag) lives in
annotations so it can be read without decoding the payload. OIDC-only users
simply have no password hash — the same object serves both auth modes.

## Authorization

Roles are data, not code. The chart ships three predefined roles — `admin`,
`operator`, and `viewer` — and operators can add their own by editing the RBAC
ConfigMap.

A rule is a `(resource, actions, namespace)` tuple. Resources are dotted paths
(`clusters`, `clusters.backups`, `clusters.restores`, `users`, `rbac`,
`settings`, `system`, `admin`). Both `resource` and entries in `actions` accept
`*`. A permission check succeeds if any rule on the user's role matches all
three of resource, action, and namespace.

**Why namespace is part of every rule:** it lets one installation serve several
teams. A role can grant `clusters:create` in `team-a` only. Note this is a
control-plane boundary, not a network or runtime one.

**Group mapping:** OAuth directory groups map to roles, so team membership in
the identity provider drives access without per-user administration.

**Caching:** permission results and the RBAC config are cached with short TTLs.
Changes to the ConfigMap therefore take effect within roughly a minute rather
than instantly.

## Sessions and secrets

- **JWT in an `httpOnly` cookie**, with `Secure` and `SameSite` configurable via
  `COOKIE_SECURE` and `COOKIE_SAME_SITE`. Chosen over a bearer token in
  `localStorage`, which JavaScript — and therefore any XSS — can read.
- **CSRF** is handled by `SameSite` on the session cookie plus a random `state`
  parameter on the OAuth authorization request, validated on callback.
- **bcrypt with a cost factor of 12**, not the library default of 10. Roughly
  250 ms per hash: slow enough to blunt GPU-accelerated cracking, fast enough
  that interactive login is unaffected.
- **Secrets never enter the audit log.** Audit entries record the action, the
  resource, and the outcome — never request bodies, passwords, or tokens.

## Auditing

Every mutating operation is written twice: to SQLite and to stdout as a
structured log line tagged `audit: true`.

**Why both:** SQLite backs the in-product audit view with filtering and
pagination. Stdout is what cluster log aggregation already collects, so the
trail survives independently of the pod's volume and can feed an existing
compliance pipeline. Neither sink is a single point of failure for the other.

## Identity providers

Google and Microsoft Entra ID are implemented behind a provider interface with
a factory, rather than being wired directly into the auth routes.

**Why:** these two cover the majority of enterprise directories, and the
indirection means adding Okta or Keycloak is a new implementation rather than a
change to the authentication flow.

## Feature flags

Runtime toggles — OAuth on/off, self-service onboarding, retention behavior —
are read from the settings ConfigMap rather than compiled in or stored in a
database.

**Why:** an operator can change behavior by editing values and upgrading the
release, with no image rebuild. Self-service onboarding is off by default: an
administrator must invite users, and enabling self-service is a deliberate act
gated behind an allowlist.

## Admin UI

- **Client-rendered SPA** (React, Vite, React Router) served as static assets by
  a small Node process, talking to the Admin Server over the same origin. There
  is no server-side rendering: the UI is an authenticated internal tool, so SEO
  and first-paint-over-cold-cache do not apply, and a static bundle is simpler
  to ship in an air-gapped registry.
- **Server state via React Query, client state via Zustand.** Nearly all state
  in the product is a projection of cluster state, so the cache and its
  invalidation rules are the important part; a global store is reserved for the
  genuinely local concerns.
- **Permissions are enforced server-side.** The UI hides controls the user
  cannot use, but every route re-checks. Hidden UI is a usability affordance,
  never a security boundary.

## Deliberate non-goals

These were considered and left out. They are recorded so the reasoning is not
relitigated from scratch.

They scope the Admin Server and Admin UI — the components that run inside a
customer cluster. The hosted Enterprise Portal is a separate system with a
different operator and threat model; see
[enterprise-portal-design.md](./enterprise-portal-design.md) for why several of
these are reversed there.

| Not built | Reasoning |
| --- | --- |
| Offline-capable UI (service worker, IndexedDB cache, queued writes) | An operator console is useless when the control plane is unreachable; caching would show stale state at exactly the moment accuracy matters most |
| Managing multiple Kubernetes clusters from one Admin Server | The service layer is abstracted enough to allow it, but nothing is wired end to end. One install per cluster |
| Multi-replica Admin Server | SQLite is local to the pod. Horizontal scaling requires moving the audit store first |
| User self-registration by default | Access to the control plane is granted, not claimed |
| Outbound webhooks and notifications | No demand established; audit stdout already feeds external systems |
