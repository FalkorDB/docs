# Enterprise Portal architecture

Design decisions behind the FalkorDB Enterprise Portal — the hosted control
plane that issues licenses, manages customer organizations, and provisions
registry credentials — and the reasoning that led to them.

This records the *why*. For the Admin Server and Admin UI that ship *inside a
customer cluster*, see [architecture.md](./architecture.md). The two systems are
related but separate, and the distinction drives most of what follows.

## The two control planes

FalkorDB Enterprise now has two, and conflating them is the easiest way to get
this wrong.

| | Admin platform | Enterprise Portal |
| --- | --- | --- |
| Runs where | Inside the customer's Kubernetes cluster | FalkorDB-hosted, multi-tenant |
| Operated by | The customer | FalkorDB |
| Shipped as | Part of `helm/falkordb-enterprise` | Its own chart, never shipped to customers |
| Knows about | One cluster, in detail | Many organizations, no cluster internals |
| Licenses | **Verifies** them | **Issues** them |
| Datastore | Kubernetes objects + SQLite | MongoDB |

**They never talk to each other.** The portal has no network path into a
customer cluster, no kubeconfig, and no ability to read live deployment state.
The only artifact that crosses the boundary is a signed license string, carried
by a human or a pipeline. That is a deliberate constraint, not a gap — it means
a portal compromise cannot reach customer data planes, and a customer cluster
being offline or air-gapped changes nothing about portal behavior.

### Why the Admin platform's non-goals do not bind the portal

[architecture.md](./architecture.md) records "Kubernetes as the datastore" and
lists outbound notifications as a deliberate non-goal. Both hold for the Admin
Server and neither applies here.

"Kubernetes as the datastore" exists to remove an operational dependency *from
every customer install*. The portal is a single deployment that FalkorDB runs;
there is no per-customer operational cost to amortize, and the data — orgs,
quotas, requests, notification routing, delivery attempts — is relational,
queried across tenants, and grows without bound. Secrets and ConfigMaps are a
bad fit for all of that.

Notifications were skipped for the Admin Server because audit-to-stdout already
fed the customer's own aggregation pipeline. The portal's audience is external
and has no such pipeline, so the reasoning does not transfer.

## Package and stack

The portal is `packages/portal`, a Next.js App Router application in this
monorepo, consuming `@falkordb/ui-library` over `workspace:*`.

**Next.js 14 with React 18**, not Next 15 with React 19.
[pnpm-workspace.yaml](../../pnpm-workspace.yaml) pins `react` and `react-dom` to
`18.3.1` workspace-wide as part of the CVE override block. Carving out an
exception for one package means two React majors resolving in one `node_modules`
graph, which breaks `@falkordb/ui-library` — it is built once and linked into
both consumers. Staying on 18 keeps the design system single-versioned. The cost
is being a major behind; the trigger for revisiting is a workspace-wide React 19
bump, not a portal-only one.

**Types stay inside `packages/portal`.** `@falkordb/admin-types` is compiled
into the customer-shipped artifact; putting SaaS concepts like quota requests
and notification targets there would leak the hosted control plane's domain into
software customers run. The portal has exactly one consumer of its types —
itself — so a package buys nothing.

### Consuming the design system

The portal consumes `@falkordb/ui-library` exactly as `admin-ui` and
`support-viewer` do: `workspace:*`, barrel imports from the package name, and
resolution through the workspace symlink to the built `dist`. No alias, no
source compilation, no per-consumer build variation.

**Why the same way rather than a portal-specific setup:** three consumers
resolving one library three different ways is three different bundles to reason
about when a component misbehaves. The build order is already established — the
library is built before its consumers, as
[packages/admin-ui/Dockerfile](../../packages/admin-ui/Dockerfile) does — and
reusing it means the portal inherits a path that is already exercised in CI.

The consequence to design around: the library is bundled by tsup from a single
entry, so `"use client"` cannot survive per-module. The whole library is a
client boundary. **Every import of `@falkordb/ui-library` goes through one
re-export barrel that carries the directive** —
[src/components/ui/index.ts](../../packages/portal/src/components/ui/index.ts).
The first version of this convention put the directive on each importing file
instead, which meant a page could only render a `Card` by becoming a client
component in full, and with it every query it made. Moving the directive to a
single boundary reverses that: the barrel's exports are client *references*, so
a server page renders `<Card>` and stays a server component.

The barrel exports components and nothing else. A client reference is not
callable, so `cn` — a plain function — cannot travel that way; a server
component that imports it gets an object and fails at request time while type
checking and building cleanly. It lives in
[src/components/ui/cn.ts](../../packages/portal/src/components/ui/cn.ts), which
carries no directive, and is implemented over `clsx` and `tailwind-merge`
rather than re-exported from the library — importing the library into a server
module would pull its module-scope `createContext` calls into the server graph,
where they do not exist.

**Tailwind v3**, matching `admin-ui` and `support-viewer`, despite ui-library
declaring v4 as a dependency. Compilation happens in the consumer, so the
consumer's version wins; a third consumer on v4 would fork the token semantics.
The portal replicates `admin-ui`'s `content` glob — including
`../ui-library/src/**/*.{js,ts,jsx,tsx}` — and its CSS-variable token mapping.
Without that glob, ui-library components render unstyled.

Two of those tokens are the portal's own, and both were repairs. The library's
default button is `bg-primary text-primary-foreground dark:text-white`, which
assumes `--primary` is dark; the inherited dark theme set it to near-white, so
every submit control on the staff console was white text on a white button,
findable only by hovering for the cursor. It is now the brand indigo in both
themes, which is also the honest reading of the token's name. `--destructive`
was a near-black red on a dark background, and it is what a field error and an
over-quota meter bar are painted with — the same red as the light theme now,
because an error message you have to know the location of is not an error
message.

### A vocabulary of page primitives, not a page of Tailwind

The library supplies controls — `Card`, `Button`, `Input`, `Badge`. It does not
supply pages, and the first pass at the portal filled that gap inline: each page
composed its own header, its own bordered panel, its own table markup. Twenty
pages of that is twenty slightly different paddings, and a design change that
has to be made twenty times is a design change that gets made twelve times.

So `src/components/ui` holds a small vocabulary above the library:

| Module | Provides | Client? |
| --- | --- | --- |
| `page.tsx` | `PageHeader`, `Section`, `EmptyState`, `StatCard`, `DetailList`/`Detail`, `Mono` | server-safe |
| `status.tsx` | `StatusPill`, `StatusDot`, `toneFor`, `humanize` | server-safe |
| `data-table.tsx` | `DataTable`, `HeadRow`, `Th`, `Row`, `Td`, `EmptyRow` | server-safe |
| `form.tsx` | `Field`, `TextInput`, `SelectInput`, `TextArea`, `SubmitButton`, `FormFeedback`, `controlClasses` | `"use client"` |

Server-safe matters: those three carry no directive, so a server page composes
a whole screen — header, panels, tables, status pills — without a client
boundary anywhere in it. Only forms, which need `useActionState` and
`useFormStatus`, cross over.

`status.tsx` is the one worth arguing for. The portal has six independent
status vocabularies — organization state, quota request state, license state,
delivery state, release channel, and role — and they were being coloured at
each call site. One table mapping status to tone means a `PENDING_APPROVAL`
organization and a `PENDING` quota request are the same amber everywhere, and
that adding a state to an enum surfaces as one missing entry rather than as six
places nobody thought to update. The library's own `getStatusColor` was not
reused because its vocabulary is the Admin platform's, not this one's.

### The sidebar, and what it cost

Navigation is a fixed sidebar grouped by task — Overview, Entitlements,
Software, Organization, Help — rendered by
[app-shell.tsx](../../packages/portal/src/components/layout/app-shell.tsx),
with a drawer and a header at small widths. It replaced a single row of eleven
links in the header, which had no room left to grow and no way to say that
Licenses and Quota are the same subject.

Two consequences that are not cosmetic:

**`/signup` and `/suspended` get no navigation at all.** Both are pages a
visitor cannot leave — one has no organization yet, the other has lost access
to theirs — and eleven links that all bounce them back is a menu of dead ends.
The root layout cannot make that call, because a server layout has no pathname;
the shell has one already, for the active entry, so `STANDALONE_ROUTES` lives
there and those two pages render through `StandalonePage` instead.

**Customers and staff get disjoint navigations, decided server-side, with
nothing handed across the boundary.** Within an audience the list is
unconditional — a viewer sees every entry an org admin does, because a page the
viewer cannot use explains itself rather than 404ing, and a nav that disagrees
with the page it links to is worse than one that is simply complete. Role is
not audience, though. Staff sessions carry no tenant, so every customer
destination redirects them straight back out; drawing those links offered a
staff engineer eleven ways to leave the page they wanted, and the same argument
that makes a complete nav right for a viewer makes it wrong here. `PortalNav`
reads `isStaff` and picks the list.

That decision is the only thing that crosses the RSC boundary, and it is a
boolean on purpose. A nav entry carries its lucide icon, and an icon is a
function: passing a group from the server component into the client one that
renders it is passing a function through the boundary, which React refuses to
serialize — at request time, not at build time. The browser suite caught that,
having also caught the last boundary mistake.

**Staff reaching a tenant page land on the console, not the signup form.**
`getTenantContext` throws for a staff session because staff have no implicit
tenant, and `requireTenantForPage` turned every `NoTenantError` into `/signup`
— so a staff engineer who clicked the logo was asked to contact FalkorDB for
access to FalkorDB. `StaffHasNoTenantError` subclasses it, which leaves every
service that already catches `NoTenantError` behaving exactly as before while
the one place that turns errors into redirects can tell the two apart.

### An address that matches nothing

Next's built-in 404 is a line of unstyled text on a white page. Inside a
console that reads as an outage rather than a wrong turn: the branding, the
theme and every way out disappear at once.
[not-found.tsx](../../packages/portal/src/app/not-found.tsx) renders inside the
shell instead, so the sidebar the reader was using a second ago survives, and
echoes the path back — the one fact that separates a typo from a dead bookmark
from a link pasted with a trailing character. Reading it needs `usePathname`,
and therefore one small client component: the request that produced the page
matched no route, so a server render has no params to read.

It is not reached only by typos. `notFound()` is also how `/releases` and
`/staff/releases` refuse a caller without `release:read`, deliberately, because
a 403 would confirm the page exists to somebody with no business knowing. That
makes "you may not be allowed to see this" a real explanation, so the page
offers it — without saying which of the two happened, since saying would undo
the point. The way out is the reader's own console and nothing else. There is
no contact-support button, for the same reason `/no-access` has none: when a
page is hidden by role, the person who can change that is an administrator at
the reader's own organization.

### Server components for data, client components for UI

The Admin UI is a client-rendered SPA, justified there by it being an
authenticated internal tool shipped into air-gapped registries. The portal is
public-facing, and its pages are mostly reads of tenant-scoped database state
behind an authorization check. Doing that in Server Components means the
authorization check and the query happen in the same place, and no tenant data
is serialized to a client that was not entitled to it.

So pages and layouts are Server Components that authorize, query, and pass
plain data down. Presentation lives in the primitives above, most of which are
server-safe; the client boundary is the ui-library barrel and the form
controls. The split is load-bearing in both directions: it keeps credentials
and cross-tenant queries off the client, and it keeps the design system's hooks
out of the server graph.

Mutations are Server Actions. Route handlers exist only where an external system
needs an HTTP surface: OIDC callbacks, inbound webhooks, and the worker's
health endpoint.

## Identity and tenancy

Zitadel is the identity provider, running as a dedicated FalkorDB Enterprise
project. Authentication uses **Auth.js (`next-auth@5`) with its built-in Zitadel
provider**, authorization code with PKCE, session as a JWT in an `httpOnly`
cookie — the same posture as the Admin Server, and for the same reason: a bearer
token in `localStorage` is readable by any XSS.

**Rejected:** hand-rolling on `openid-client`. The Admin Server did that for
Google and Azure because it needed directory-group resolution the libraries did
not offer. Nothing here needs that, and Auth.js already handles callback
validation, `state`/`nonce`, and token refresh.

### Tenant resolution

A Zitadel Organization maps 1:1 to a portal `Organization`, and **a user belongs
to exactly one**. The mapping key is the
`urn:zitadel:iam:user:resourceowner:id` claim, resolved to
`Organization.zitadelOrgId` at session-callback time and frozen into the
session.

**The tenant is never read from the request.** Not from a path segment, not from
a query parameter, not from a header. Every query is scoped by the
organization id on the session. This is the single highest-value invariant in
the system: a tenancy bug in a hosted control plane is a cross-customer data
breach, and the cheapest way to not have one is to make the tenant
unspecifiable by the caller.

One org per user is what makes that invariant cheap. There is no org switcher,
so there is no server-side session mutation that changes tenant, so there is no
code path where the tenant is influenced by anything the caller sends. A user
who needs access to two organizations needs two accounts.

Enforcement is structural rather than by convention. Data access goes through a
repository layer that takes a `TenantContext` as its first constructor argument
and injects `organizationId` into every filter, and the raw Mongoose models are
not exported from that module. Admin-side queries that legitimately span tenants
go through an explicitly named escape hatch that requires an admin role and
writes an audit entry.

### Membership by email domain

An organization owns one or more email domains, and a user belongs to the
organization that owns their address's domain. Signing up with
`someone@acme.com` joins Acme's org; there is no invitation code to pass around
and no per-user membership record to keep in sync.

Two things have to be true for that to be safe, and neither is optional:

- **The email address must be verified by Zitadel before the domain is
  consulted.** Otherwise domain membership is self-asserted, and anyone who can
  type `ceo@acme.com` into a signup form joins Acme.
- **The domain must be verified as belonging to the organization**, and public
  mailbox providers are blocklisted. Otherwise the first person to register
  `gmail.com` owns every Gmail user who ever signs up.

Domain ownership is established by **account-manager attestation at approval
time**, not by a DNS challenge. The approving account manager confirms the
domain belongs to the customer as part of the review they are already doing.

**Why attestation rather than a DNS TXT record:** a DNS challenge proves control
of the domain, but the thing it would protect against — someone claiming a
domain that is not theirs — is already blocked by a human reading the signup
before anything is provisioned. Adding a DNS step buys cryptographic proof of a
fact the reviewer has to evaluate anyway, at the cost of a support ticket every
time a customer's DNS is managed by a different team. The attestation is
recorded on the organization with the approver's identity, so the decision is
attributable.

This holds only because signup is gated. If open signup is ever introduced, DNS
verification becomes mandatory in the same change — the two are a pair.

Domains are unique across organizations, enforced by a unique index rather than
an application check, because the failure mode of a duplicate is two orgs
claiming the same users.

### Signup and approval

Signup is self-service but access is not. A new signup creates an
`Organization` in `PENDING_APPROVAL` — no Zitadel org, no Gitea user, no quota,
no license capability — and notifies account managers. Approval is what runs
the provisioning saga. Rejection is terminal and recorded with a reason.

**Why not open signup:** the portal hands out registry credentials and signed
licenses. Those are commercial artifacts, and issuing them to an unreviewed
signup is issuing them to anyone. The Admin platform states this as "access to
the control plane is granted, not claimed"; the approval gate is that same rule
with a self-service front door, so the sales conversation starts from a form the
customer already filled in rather than from an email thread.

If a signup's domain already belongs to an approved organization, it is not a
new organization — it is a join request routed to that org's `org-admin`s. This
keeps a second employee at an existing customer from creating a duplicate
tenant, which is the most common way multi-tenant systems accumulate garbage.

### Approval attests the domain claim

Approval is the moment the organization's email domains become load-bearing:
from then on, anyone signing up from one of them lands in that tenant with no
invitation. So approval records `domainAttestedById` — the person who accepted
that consequence — and it is written only on the approval transition, never
back-dated onto a later suspension or reinstatement.

Status transitions put the permitted origin statuses in the update filter, the
same shape as quota review. Two account managers working the same queue is
ordinary, and a read-then-write would let an approval land on top of a
rejection. Approval is the transition that grants access, so it is the one that
must not win a race it did not start.

**Suspension is not an account manager's to make.** `organization:approve` and
`organization:suspend` are separate permissions and only `super-admin` holds
the second. Approving a signup and cutting off a paying customer are different
stakes, and one queue-facing role should not be able to do both by muscle
memory. Suspension blocks the portal only — licenses already issued keep
verifying offline until they expire, because stopping a customer's production
database is a business decision, not a side effect of a button in a console.

Staff work through `StaffContext`, which is deliberately *not* a
`TenantContext`. The staff queue spans every organization, so there is no
`organizationId` to scope by; giving it a synthetic one would hand the
repository layer a value it would then trust. The cross-tenant reads live in a
module named for who may call them rather than in a scoped repository that
sometimes ignores its scope — the danger should be legible from the import.

### Roles

Zitadel project roles arrive in the `urn:zitadel:iam:org:project:roles` claim.

| Role | Granted in | Can |
| --- | --- | --- |
| `super-admin` | FalkorDB's own Zitadel org | Everything, including global quota overrides and suspension |
| `account-manager` | FalkorDB's own Zitadel org | Approve or reject signups, set quota, review quota requests, publish releases |
| `support-engineer` | FalkorDB's own Zitadel org | Read every organization's metadata, audit logs, and registry credentials |
| `org-admin` | The customer's Zitadel org | Invite and remove members, connect an identity provider, configure notification routing, request quota, issue licenses, view registry credentials |
| `developer` | The customer's Zitadel org | Issue licenses within quota, generate install scripts, view registry credentials |
| `viewer` | The customer's Zitadel org | Read licenses, docs, and feeds |

Middleware gates route *groups* — it is a cheap early rejection, not the
boundary. Every Server Action and route handler re-checks with a
`requirePermission` guard that reads the session directly. This is the Admin
platform's rule restated: hidden UI is a usability affordance, never a security
boundary.

**Why roles come from Zitadel rather than a portal table:** access to the
control plane is granted through the identity provider, so revoking a
departing employee's Zitadel account revokes their portal access with no second
system to remember. It also means the portal never has an authorization state
that can drift from the IdP.

**Support engineers can read customer registry credentials**, because "my
`helm pull` returns 401" is the ticket they exist to close and diagnosing it
without the token means guessing. The control that makes this acceptable is not
restriction but visibility: decrypting a credential is a distinct audited
action recorded against the engineer, the organization, and the reason, and it
is surfaced in the customer's own audit view. Read-only is a real boundary here
— support engineers cannot rotate, suspend, or issue.

The same reasoning does not extend to license key payloads. A payload is a
signed bearer artifact whose only use is running a cluster, and nothing in a
support workflow requires the signature rather than the decoded limits. Support
engineers see the decoded payload, not the key.

### Provisioning Zitadel

The portal creates Zitadel organizations, invites users, and assigns project
roles through the Management API, authenticating as a service user with a JWT
profile key.

**Why the portal provisions rather than an operator doing it by hand:** approving
a customer organization is a multi-system transaction — Zitadel org, portal
`Organization`, Gitea machine user, initial quota. Any manual step in that chain
is a step that gets skipped, and the failure mode is a half-created tenant.

The transaction is not atomic across systems, so it is modeled as a saga with
explicit compensation: if Gitea provisioning fails after the Zitadel org is
created, the org is marked `PROVISIONING_FAILED` rather than left looking
healthy. Reconciliation is a manual admin action, because silently retrying
identity provisioning is worse than surfacing it.

## Data model

MongoDB via Mongoose. Collections follow the epic's shapes, with the additions
noted below.

```ts
Organization      { name, slug, domains[], domainAttestedById?, status,
                    zitadelOrgId?, giteaUsername?, giteaTokenId?,
                    giteaTokenCiphertext?, approvedById?, rejectionReason?,
                    createdAt, updatedAt }
Quota             { organizationId, maxCpuCores, maxMemoryGb,
                    maxKubernetesClusters, maxDeployments, maxUsers,
                    expirationTimestamp, ... }
QuotaRequest      { organizationId, requestedByUserId, requestedQuota,
                    justification, status, adminNotes, ... }
License           { organizationId, clusterId,
                    allocatedCpuCores, allocatedMemoryGb, allocatedDeployments,
                    keyPayload, expiresAt, origin, revokedAt?, createdById, ... }
Cluster           { organizationId, name, releaseChannel, k8sClusterId,
                    requestedCpuCores, requestedMemoryGb, requestedDeployments,
                    status, currentVersion?, ... }
Release           { version, channel, publishedAt, isSecurityPatch,
                    breakingChanges[], notes, source, sourceRef?, status, ... }
NotificationTarget  { organizationId?, name, type, configCiphertext, ... }
NotificationChannel { organizationId?, name, subscribedEvents,
                      releaseChannels, targetIds, ... }
InAppNotification { organizationId?, userId?, event, payload, readAt?, ... }
NotificationOutbox  { event, targetId, dedupeKey, attempts, nextAttemptAt,
                      status, lastError?, ... }
AuditEntry        { organizationId?, actorId, action, resourceType,
                    resourceId, result, message, ip, userAgent, createdAt }
```

`Organization.status` is `PENDING_APPROVAL | ACTIVE | SUSPENDED | REJECTED |
PROVISIONING_FAILED`. The epic's two states describe an approved org's lifecycle;
the rest exist because signup and provisioning can both fail and a tenant stuck
halfway needs to look stuck rather than look active.

Additions and why:

- **`Cluster`** — the unit customers register and the unit quota is measured
  against. The epic attaches a release channel and capacity to the license, but
  a license is an immutable signed artifact while a cluster is a long-lived
  record that gets re-licensed, re-channeled, and resized. Separating them lets
  the registration survive license reissuance, and gives release notifications
  something durable to target.

  The channel is on the cluster **only**. It was briefly copied onto the license
  as well, which was wrong twice over: every channel ships the same product, so
  a channel is not an entitlement, and the copy went stale the moment a cluster
  was re-channeled. A license says what a cluster may run; the channel says
  which releases the customer follows, and they change on different clocks.

  `releaseChannel` and `currentVersion` are editable after registration
  (`cluster:update`, audited as `cluster.update`). Nothing else on the record is:
  capacity is quota-bearing and `k8sClusterId` is what licenses are bound to.
  `currentVersion` is self-declared, like the capacity numbers — the portal has
  no network path into a customer cluster — and nothing is entitled or throttled
  by it, so a stale value only makes upgrade advice less useful, which is what an
  absent one does too.
- **`Release`** — see [Releases and channels](#releases-and-channels). Release
  notifications need something that says a version shipped; nothing in the
  epic's model does.
- **`NotificationOutbox`** — see [Notification delivery](#notification-delivery).
- **`AuditEntry`** — the portal makes decisions with commercial consequences
  (suspension, quota grants, license issuance). Every one needs to be
  attributable. Mirrored to stdout tagged `audit: true`, matching the Admin
  Server's dual-sink reasoning. Exported as CSV from `/audit/export`, gated on
  `audit:read`, streamed from a Mongo cursor so a long history does not have to
  fit in memory — and the export is itself audited, because "who took a copy of
  the audit log" is an auditable act. Every field is quoted and any value
  starting `=`, `+`, `-` or `@` is prefixed with an apostrophe: a spreadsheet
  treats those as formulas, and an audit log contains attacker-controlled
  strings.
- **`AccessRevocation`** — see [Removing members](#removing-members). Roles are
  frozen into a JWT at sign-in, so removing a Zitadel grant removes nothing from
  a session that is already open; this is what the request path checks.
- **`Organization.scimServiceUserId` / `scimTokenId`** — see
  [Bring your own identity provider](#bring-your-own-identity-provider). The id
  of a token, kept so it can be revoked. Not the token.
- **`License.revokedAt`** — records intent even though it cannot be enforced
  offline. See [License issuance](#license-issuance).
- **`License.origin`** — `issued | imported`. The portal signed the first kind
  and only recorded the second. Both count against quota; keeping them
  distinguishable means a discrepancy found later points at the import rather
  than at issuance.
- **Ciphertext suffixes** — `giteaTokenCiphertext` and
  `NotificationTarget.configCiphertext` hold AES-256-GCM ciphertext, not
  plaintext, with the key supplied out of band. Webhook URLs are bearer
  credentials: anyone holding a Slack incoming-webhook URL can post as the
  integration. Naming the field for its encoding makes a plaintext write
  obviously wrong at the call site.

Every tenant-scoped collection carries a compound index leading with
`organizationId`.

**MongoDB must be a replica set**, even for a single node. Multi-document
transactions require one, and the provisioning saga and quota checks both need
them. A standalone `mongod` will pass local development and fail the first
concurrent quota check in production.

## Inviting members

An org admin invites a colleague from `/members`, gated on `member:invite`. The
portal calls Zitadel four times: find the user by email within the customer's
organization, create them if they are not there, grant the chosen role on the
portal's project, and ask Zitadel to email an invite code.

**The portal stores a log, not a membership table.** `Invitation` records who
invited whom, to what role, and when it was last sent — one row per address per
organization. It is deliberately not the answer to "who can sign in": that is
the token, resolved from Zitadel's claims on every request. A membership table
here would be a second source of truth that drifts the first time somebody is
removed in Zitadel, and drifts silently, because nothing reads it.

**Invitations are not charged against `maxUsers`.** That quota dimension caps
the users of a customer's FalkorDB deployments and is metered by the Admin
Server. The people who administer the portal are a different set, usually
smaller and differently composed, and billing an operations engineer's portal
login against a database seat limit would be a charge nobody could explain.

Three details that are easy to get wrong:

- **The user is created with `returnCode`, not `sendCode`.** Asking Zitadel to
  email the email-verification code and then asking it to email an invite code
  delivers two emails for one invitation, and the first one leads nowhere
  useful. The verification code is taken back and discarded; the invite code is
  what the recipient acts on, and it verifies the address as a side effect.
- **An existing grant is not an error.** Re-inviting somebody to the role they
  already hold is the ordinary way to resend a lost invitation, so the 409 from
  `AddUserGrant` is swallowed. Any other status is not.
- **The search is scoped to the organization.** Zitadel makes email addresses
  unique per organization rather than per instance, and this function's answer
  feeds a role grant. An unscoped search could return a different customer's
  user.

A half-configured install counts as unconfigured: without both
`ZITADEL_API_TOKEN` and `ZITADEL_PROJECT_ID`, the members page says invitations
are unavailable and points at the identity provider, rather than failing
halfway through one. The token is deliberately a second credential and not
`AUTH_ZITADEL_SECRET` — that one proves the portal is an OIDC client and cannot
create users, and widening it so it could would mean every sign-in flowed
through a credential that can mint administrators.

## Removing members

Inviting without removing is half a feature, and the half without a deadline.
`/members` lists current access — read live from Zitadel, not from the
invitation log — and offers **Remove**, gated on `member:remove`.

**Removal is two writes in two systems, and neither alone removes anybody.**
Zitadel loses the role grant, so signing in again yields nothing. The portal
writes an `AccessRevocation` row, so the session they already have stops working
on its next request.

The second write exists because of how sessions are built here. `auth/index.ts`
uses `session: { strategy: 'jwt' }`, and the `jwt` callback only re-reads roles
`if (profile)` — that is, at sign-in. Roles are frozen into the cookie, and no
change in Zitadel reaches it for the cookie's life. Without a revocation record
the honest description of "remove access" would be "remove access, next week".
`getTenantContext` checks the record on every request and throws
`AccessRevokedError`, which `/no-access` explains.

Rows are kept with a `restoredAt` rather than deleted, and re-inviting somebody
sets it — so the record of the removal survives the reinstatement.

Two removals are refused, both because the alternative is a customer locked out
of their own account with no way back except a support ticket: nobody removes
themselves, and nobody removes the last `org-admin`. The last-admin check reads
the **live directory**, not the invitation log: an administrator granted in the
Zitadel console is invisible to the log, and counting only what the portal sent
would refuse a removal that is perfectly safe.

**The Zitadel account is not deactivated or deleted.** Only the grants on the
portal's project are removed. The same person may be a user of the customer's
other applications in the same Zitadel organization, and "remove from the
portal" must not mean "remove from your company's identity provider".

## Bring your own identity provider

A customer whose staff live in Okta or Entra ID has to have accounts here as
well: a second credential to phish, a second offboarding step to forget, and a
security review to fail. `/sso` removes both, gated on `sso:manage`.

Two separate things, deliberately not one switch — they are usually adopted
weeks apart, and a customer who turns on the first is not agreeing to the
second:

- **Connecting a provider changes authentication.** A generic OIDC provider is
  registered against the customer's Zitadel organization, with linking and
  auto-creation on so somebody already invited by email is matched to their
  existing account rather than given a second one.
- **Enabling SCIM changes lifecycle.** Zitadel exposes a SCIM v2 service per
  organization at `{issuer}/scim/v2/{orgId}`; the portal provisions a machine
  user and a personal access token for the customer's IdP to authenticate with.

**Registering a provider is not enough on its own.** Zitadel only offers a
provider on the login screen if it is attached to the organization's login
policy, and an organization that has never customised its policy inherits the
instance default and has nothing to attach to — Zitadel answers `404`. So
`connectProvider` falls back to reading the effective policy and creating an
organization-level copy of it with the provider included. The copy is field by
field from the policy that was already in force, so that connecting an IdP
changes exactly one thing: a chart that wrote its own defaults would silently
turn off the customer's MFA requirement as a side effect.

**None of this configuration is stored in Mongo.** It lives in Zitadel, which is
where the login screen reads it from. A copy here would be a second source of
truth that drifts the first time somebody uses the Zitadel console — and the
question this page answers ("which directory do we trust to say who somebody
is?") is one that must not be answered from a stale cache.

The two exceptions are `Organization.scimServiceUserId` and `scimTokenId`, kept
only so the token can be revoked. **The token itself is never stored**, not even
encrypted: unlike the Gitea credential, which the portal must show again when it
builds an install command, a SCIM token is pasted into the customer's IdP once
and never legitimately read by us again. It is shown once and the panel says so.

Three smaller choices:

- **The SCIM service account gets `ORG_USER_MANAGER`, not `ORG_OWNER`.**
  Provisioning creates, updates and deactivates users; that is all it needs. An
  owner token leaked out of a customer's IdP could rewrite their login policy
  and lock everybody out, including us.
- **The token does not expire.** An expiring provisioning token stops
  deprovisioning silently — the IdP keeps trying, the portal keeps looking
  correct, and a departed employee keeps their access until somebody notices.
  Rotation is offered as a button, not imposed as a timer.
- **Disconnecting a provider leaves its accounts alone.** Deleting them would
  turn a change of login method into data loss for the customer's own staff,
  who would rather sign in another way than be re-invited.

### Three things a real Zitadel says that a mock does not

These were all written the obvious way, passed their unit tests, and were wrong.
An integration suite that boots Zitadel in a container found them; it is kept
for that reason and not as a formality.

- **A role grant is a list, not a row.** Zitadel holds one grant per user per
  project, carrying a set of role keys, and answers `409` when a grant already
  exists. Treating that as "already done" is right for a resend and wrong for a
  promotion: it reported a viewer becoming an administrator and changed nothing.
  A grant that exists is now read back and rewritten with the extra role.
- **Rotating a SCIM token must reuse the machine user.** The username is unique
  within the organization, so recreating it fails — which made rotation
  impossible for exactly the people who had already rotated once.
- **Zitadel does not enforce provider names.** Connecting a second "Okta"
  succeeds and returns a new id, leaving the customer two identical rows, one of
  which signs people in. The portal refuses the duplicate itself; there is a
  race here between two administrators, and it is not worth a lock.

### Testing SCIM without a second identity provider

Zitadel implements SCIM as a *service provider*: it receives provisioning from
Okta or Entra and never sends any. There is therefore no arrangement of Zitadel
instances in which one provisions another, and no container that can stand in
for the customer's identity provider. The test suite acts as the SCIM client
itself, calling create, filtered search, deactivate and delete against the
token the portal issues.

That sequence, rather than a single call, is what the grant needs to be checked
against. `ORG_USER_MANAGER` is deliberately narrower than `ORG_OWNER`, and a
grant that could create but not deprovision would look healthy on the day it was
configured: joiners appear, and leavers keep their access until somebody
notices. The same suite points one organization's token at another
organization's SCIM URL, because the organization is in the URL and the token is
the only thing deciding whether it may be addressed.

What is still untested is a real federated sign-in: a browser redirected to a
third-party identity provider and back. Everything up to the point where
Zitadel issues claims is covered; the round trip through a foreign login screen
is not.

### Roles are Zitadel's word, and only for its own organization

Role keys belong to a project, and any organization administrator can create a
project role called `super-admin` and grant it to themselves — in the console it
takes about four clicks. The claims Zitadel then issues really do carry it,
truthfully: they are a super-admin of their own project. Staff authority is
therefore not "holds a staff role" but "holds a staff role **and** is issued by
the FalkorDB organization", and the second half is the whole of the check. The
integration suite performs that escalation against a real Zitadel and asserts
the portal discards the role.

## Quotas

Six dimensions per organization: expiration, CPU cores, memory, Kubernetes
clusters, deployments, and user seats.

**Quota is evaluated against registered clusters, not observed usage.** The
portal has no path into a customer cluster and cannot see what is actually
running. What it has is the set of clusters the customer registered in order to
get a license, each declaring the capacity it wants. Issuing a license for a
cluster is the moment that declaration becomes binding, so that is where the
check happens:

| Dimension | Measured as |
| --- | --- |
| Kubernetes clusters | count of the organization's active registered clusters |
| Deployments | sum of `requestedDeployments` across them |
| CPU cores | sum of `requestedCpuCores` across them |
| Memory | sum of `requestedMemoryGb` across them |
| Users | Zitadel org membership count |
| Expiration | issued license `expiresAt` is capped at the quota's |

### Kubernetes clusters and deployments are separate dimensions

The epic lists five dimensions, with "Deployment Count" covering "active
Kubernetes deployments/clusters". Those are two different things and they are
metered in two different places.

The portal's `Cluster` is a **Kubernetes cluster**, because that is what a
license binds to via `k8sClusterId`. A deployment is a **FalkorDB database**
running inside one — a KubeBlocks cluster — and the Admin Server meters
`limits.deployments` by counting those within its own installation. One
Kubernetes cluster hosts many deployments.

Collapsing them loses control in one direction or the other. Metering only
Kubernetes clusters lets an organization with a limit of 10 run unbounded
databases in each. Metering only deployments lets them spread a small database
allowance across arbitrarily many clusters, each of which is a separate license,
a separate support surface, and a separate registry pull path.

So a registered cluster declares three numbers — cores, memory, and deployments
— the organization's quota caps the total of each, and `maxKubernetesClusters`
caps how many registrations exist at all. Only `deployments`, `cpuCores`, and
`memoryGB` cross into the license payload, because those are the only ones the
Admin Server can see from inside a single cluster.

The customer is declaring their own numbers, which sounds weak until you note
what enforces them: the declared capacity is written into the license payload's
`limits`, and the Admin Server enforces *that* against real consumption inside
the cluster. A customer who under-declares to fit their quota gets a license
that throttles them at the number they chose.

So the two layers are: the portal governs what a customer is *entitled to
claim*, and the Admin Server governs what a cluster can *actually consume*.
Neither alone is sufficient, and neither requires the portal to reach into the
cluster.

The check is `sum(registered) + requested <= quota`, evaluated inside the same
transaction as the cluster registration and license insert. Outside the
transaction it is a race that lets two concurrent registrations both pass.

### A transaction alone does not close the race

Wrapping the check and the write in a transaction is necessary and *not
sufficient*, which is worth stating because the code looks correct without the
extra step.

MongoDB transactions give snapshot isolation, not serializability. Two
concurrent registrations each read a snapshot in which one slot is free, and
each inserts a *new* cluster document. The inserts share no document, so the
server has nothing to detect a conflict on, and both commit. The organization
ends up over its ceiling with neither request having done anything wrong. This
is textbook write skew, and it was reproduced against a real MongoDB before it
was fixed — the test that does so is in
[licensing.test.ts](../../packages/portal/test/integration/licensing.test.ts).

The fix is to give the two transactions a document to conflict on. Registration
increments `Quota.capacityVersion` before reading capacity, so the second
transaction hits a `WriteConflict`, the driver's `withTransaction` retries it,
and the retry reads the state the first one committed — at which point the
quota check correctly refuses it.

The field is a lock, not a version anyone reads. It is on the quota row because
that row is what the capacity is being spent against, so any future operation
that consumes capacity has an obvious place to serialize on.

**Rejected:** a unique index expressing the limit. It cannot work — the limit is
a sum across a variable number of documents, and the value changes per
organization and over time.

Quota requests are a state machine (`PENDING` → `APPROVED` | `REJECTED`) with
admin notes retained on both terminal states, so a rejection is explainable
months later.

### The review guard is a filter, not a read

Settling a request updates it with `status: 'PENDING'` **in the query filter**,
not in a check beforehand. Two account managers opening the queue at the same
moment is ordinary, not exotic, and a read-then-write there would let an
approval land on top of a rejection — and, because approval applies the limits,
raise a quota that had just been refused. With the status in the filter,
MongoDB's single-document atomicity decides it: one update matches, the other
matches nothing, and the loser is told the request was already decided rather
than being handed a success it did not cause.

Raising a quota deliberately takes no capacity lock, unlike registration. It
only loosens the constraint, so both orderings of two concurrent approvals end
at a quota the reviewers each considered acceptable.

Reducing a quota below what is already registered is permitted but never
silently truncates: existing clusters keep their licenses until expiry, new
registrations are refused, and renewals are refused until the customer
deregisters down to the new ceiling.

## License issuance

The portal owns the Ed25519 private key whose public half is embedded in
[licensing.service.ts](../../packages/admin-server/src/services/licensing.service.ts).
Signing logic is lifted from [scripts/generate-license.mjs](../../scripts/generate-license.mjs)
into a portal service; the wire format is unchanged:

```
falkor.license.v1.<base64url(payload)>.<base64url(ed25519 signature)>
```

Constraints that fall out of the format:

- **The private key never reaches a browser or a client bundle.** Signing
  happens in a Server Action only, through a `LicenseSigner` seam — see
  [Key custody](#key-custody).
- **Every issued license is bound to a cluster.** `k8sClusterId` is required at
  registration, and the Admin Server checks it against `K8S_CLUSTER_ID` or the
  `kube-system` namespace UID. Without it, one license covers unlimited
  clusters and the deployment-count quota means nothing.
- **Licenses cannot be revoked.** Verification is offline by design; a cluster
  that already holds a license will keep accepting it until `expiresAt`.
  `License.revokedAt` records the decision so the portal stops counting the
  allocation and refuses renewal — it does not reach into a running cluster.
  **This must be stated plainly to account managers**, because the natural
  assumption is that suspension stops a running deployment. It does not;
  suspension stops *pulls* and *renewals*. Cluster binding is what keeps the
  blast radius to the one cluster the license names.
- **Issued licenses are immutable.** Changing a limit means issuing a new
  license and expiring the old record, which keeps the audit trail honest.

### Requiring the cluster UID does not block onboarding

Requiring `k8sClusterId` means the customer must have a cluster before they can
have a license. That is fine, because the Admin Server already grants a
**14-day trial with unlimited limits when no license is present**. The onboarding
order is: install, run, then license — and the portal's registration form asks
for a value the customer can read out of the cluster they just installed into.

**Rejected:** optional binding with a prompt. It trades a real enforcement
property for a first-run convenience that the trial already provides.

### Expiry is customer-chosen, quota-capped

The organization's `Quota.expirationTimestamp` is the ceiling. At generation
time the customer picks any expiry up to it.

**Why let the customer choose rather than always issuing to the ceiling:** a
shorter license is a smaller window in which a suspended or departed customer
keeps running, and the customer is the one who knows their maintenance cadence.
Making it their choice means the safe option is available without a support
request. Renewal is self-service and re-runs the full quota check, so an
organization that has been suspended or has outgrown its quota simply cannot
renew — which is the enforcement mechanism that offline verification denies us
at revocation time.

### Four things the quota check does not cover on its own

The check is `sum(live clusters) <= quota`, and it is correct. What it does not
do is notice when the question is malformed, and every one of these mints a
signed, offline-verified license that cannot be recalled.

**A decommissioned cluster.** Quota is summed over live clusters, so a retired
one contributes nothing to the ceiling while its declared capacity is still
sitting on its own document. Retire a cluster, register another with the freed
room, and both would hold a license: the check passes because it is not counting
the capacity the license is about to grant. Nothing sets `DECOMMISSIONED` yet,
which is precisely why the guard exists now rather than after the button that
does exists.

**A term that has already ended.** Expiry is clamped to
`quota.expirationTimestamp`, and clamping to a date in the past is arithmetic
that succeeds while meaning nothing: issuance reports success and the customer
installs a key their cluster reports as expired. The remedy is a renewed
agreement, which no amount of pressing the button produces, so the refusal names
the end date.

**An expiry the customer asked for in the past.** The form has a date picker;
the server action is an HTTP endpoint, and only one of those is under our
control. Capping can lower a date but never raise it.

**Rotating a license that has already expired.** Rotation deliberately carries
the expiry over, so applied to an expired key it mints a replacement expiring at
the same passed date and retires the original in the same transaction — two dead
licenses and a success message. The portal now says to issue rather than rotate,
and the licenses table stops calling an expired license "Active" and stops
offering the button.

None of these is reachable by an ordinary customer following the UI. All four
are reachable by anyone who can post a form, and three of the four would have
been reachable through the UI the day an ordinary feature landed.

### A refusal shown before the form, not after it

A server that refuses correctly and a UI that offers the refused action anyway
are the same product to the person using it: they type, they submit, they get a
sentence they could have been given a minute earlier. Worse, the sentence
arrives with no way forward, and the states the portal refuses are mostly ones
the customer cannot resolve alone — a quota we have not recorded, an agreement
that has ended, capacity that is already spoken for. Those need us, so they get
a contact button rather than an apology.

So each page now answers "why is the form not here" in its place: no permission,
no quota, or a lapsed term on the licensing page; no permission, no quota, or no
headroom on the clusters page. Registration additionally shows what is left of
each limit beside the field that spends it, because the quota is checked against
the sum of every live cluster and the only number that predicts the outcome is
the remainder — the number the customer did not have.

The two capacity forms also constrain what they accept: an expiry cannot be set
before today or after the agreement ends, and a declared size cannot exceed the
headroom. That is courtesy, not control. Every one of these limits is checked
again in the action, because a form is a suggestion and the transaction is the
decision.

### The portal becomes the only issuer

[scripts/generate-license.mjs](../../scripts/generate-license.mjs) stops being a
normal way to issue a license and becomes break-glass only. Since the portal
holds the same key in its environment rather than in a KMS, "only issuer" is a
process guarantee rather than a cryptographic one — see
[Key custody](#key-custody).

**Why single-issuer is load-bearing:** the portal's quota accounting is a model
of what customers are entitled to run, and that model is only true if every
signed license passed through the check that maintains it. A second issuing path
is a path that mints capacity the portal cannot see, and the drift is silent —
nothing fails, the numbers are just wrong, and they stay wrong until a renewal
surfaces the discrepancy in front of a customer.

### Backfilling existing customers

Licenses already issued by script exist and are in production, so the portal
starts with an accounting gap it did not create. It is closed by an import path,
not by waiting for the licenses to age out: an account manager creates the
organization, attests its domains, sets the quota, registers the clusters, and
records each previously issued license against the cluster it covers.

Imported licenses are stored with the same shape as issued ones and marked
`imported`, because the portal did not sign them and cannot prove what it did
not witness. They count against quota — that is the entire point — but the
provenance stays distinguishable so a discrepancy found later is attributable to
an import rather than a bug in issuance.

**Rejected:** letting old licenses expire naturally with no import. It is less
work exactly once, and in exchange every quota number is wrong until the last
legacy license lapses — during which the first renewal an existing customer
attempts is checked against a quota that does not know what they are already
running.

### Key custody

The signing key is the most valuable secret in the company: whoever holds it can
mint unlimited capacity for any account. **The key is supplied to the portal as
an environment variable** (`LICENSE_PRIVATE_KEY_B64`, a base64-encoded PEM), the
same way it reaches `scripts/generate-license.mjs` today.

This is a deliberate choice of operational simplicity over custody, and the cost
is real enough to write down rather than discover later:

- Anything that can read the portal's environment can mint licenses — a shell in
  the pod, the deployment manifest, a process dump, a backup of the manifest.
- Those licenses are **indistinguishable from ours**. The verifier is offline
  inside customer clusters, so nothing reports back and nothing can be revoked.
- **Rotation is not a recovery path.** Changing the key invalidates every
  license already in the field, because each one is verified against the public
  key compiled into the Admin Server the customer is running. A leak is
  therefore mitigated by narrowing who can read the secret, not by rotating
  after the fact.

Given that, the practical controls are: keep the Kubernetes secret readable only
by the portal's service account, keep the number of humans with cluster exec
rights small, and rely on the audit log for issuance *through the portal* —
noting it says nothing about a key used elsewhere.

Signing still goes through a `LicenseSigner` interface with a single
implementation. One interface for one implementation is usually noise; it earns
its place here because it is the line above which no code can see key material,
and because moving custody later should not touch anything that assembles a
payload.

**A move to a KMS would not require changing the license format**, which is not
obvious and was worth confirming while the question was open.
`crypto.sign(null, ...)` is pure Ed25519 over the raw payload segment, and pure
Ed25519 is available in both plausible backends:

- **HashiCorp Vault Transit** — native `ed25519` key type, `/transit/sign`
  (returns `vault:v1:<base64>`; the version prefix would need stripping)
- **AWS KMS** — `ECC_NIST_EDWARDS25519` with `ED25519_SHA_512` and
  `MessageType: RAW` (the `ED25519_PH_` variant is Ed25519ph and is *not*
  interchangeable)

So the door stays open at the cost of one new class. Had pure Ed25519 *not* been
available, the choice would have been between changing the license algorithm —
which means changing the verifier embedded in every deployed Admin Server — and
keeping the key where it is.

The existing `LICENSE_PRIVATE_KEY_B64` GitHub Actions secret is removed from
Actions once the portal issues licenses. Leaving it there would preserve the
second issuing path that [single-issuer](#the-portal-becomes-the-only-issuer)
exists to close.

### Regenerating a key

A customer who has leaked a license key — pasted into a ticket, committed to a
public repository, left in a CI log — needs a new one. `/licenses` offers
**Regenerate** on any current key, gated on `license:issue`.

Regeneration mints a replacement and marks the original `revokedAt`, in that
order and inside one transaction. The order matters: minting can fail, most
often because quota was reduced since the original was issued, and an abort that
had already revoked would leave the cluster with no current license over a
failure that changed nothing.

Three properties are chosen rather than incidental:

- **The replacement is minted from the cluster's current registration**, not
  copied from the old payload. Copying would let regeneration grandfather
  capacity that a quota reduction had already removed — a revocation feature
  that quietly restores entitlement.
- **The expiry is carried over.** Rotation is not a renewal. Reissuing at
  `now + term` would hand out free time to anyone who pressed the button, and
  reissuing at a default term would shorten a customer's licence for rotating.
- **The old key keeps working.** This is the part the UI has to say out loud.
  Verification is offline, so nothing reaches a running cluster: the old key
  stays valid inside FalkorDB until the new one is installed or the term ends.
  Revocation means the portal stops treating it as current — it drops out of
  `currentForCluster` and out of the expiry sweep — and nothing more.

**The revoked row is kept, not deleted.** A hard delete would destroy the record
that a key existed and was withdrawn, which is the exact question asked after a
leak: what was issued, to whom, when, and when did we stop honouring it. The
licenses table shows revoked keys as *Replaced* rather than *Revoked*, because
"revoked" implies it stopped working somewhere, and it did not.

## Registry credentials

Customers pull Helm charts and images from Gitea's OCI registry. Each
organization gets its own credential so it can be revoked in isolation.

Gitea's `POST /api/v1/users/{username}/tokens` creates a token *belonging to
that user*, so per-organization tokens require **per-organization Gitea machine
users**, created by the portal through the admin API and granted read access to
the artifact org. A single shared machine user cannot produce independently
revocable credentials, which is the whole point.

Token values are returned by Gitea exactly once. They are stored encrypted so
`org-admin` and `developer` can retrieve them later; the alternative — showing
once and forcing regeneration — was rejected because the credential is embedded
in customer CI and regenerating it breaks their pipeline.

Suspension deletes every token for the org's machine user and deactivates the
user. Deleting tokens is what actually revokes `helm pull`; deactivating the
user is defense in depth. Reactivation provisions a **new** token — the old
value is unrecoverable — and notifies the org's admins, because their pipelines
need updating.

Scope is `read:package` only. The portal is the sole writer to the registry.

### What the real Gitea changed

The plan above was written from Gitea's API documentation. Building it against a
real Gitea 1.22 contradicted it twice, in ways that would both have shipped.

**A token cannot mint a token.** The obvious implementation — call
`POST /api/v1/users/{u}/tokens` with the admin token and a `Sudo` header — is
refused with `401 auth required`, no matter how privileged the token is. Gitea
deliberately does not let token authentication reach its own token endpoints,
which prevents a leaked token from minting more. The endpoints accept basic auth
only: the admin's, or the target user's.

Neither option is obviously good, since it means the portal needs a *password*
rather than the token already in its configuration. The way out is that the
portal creates the machine user, so it can choose that user's password: create
the user with a random password through the admin API, then authenticate **as
that user** to mint the token. The password is used once and never stored — a
later rotation sets a fresh one through the admin API first. So the portal still
holds exactly one operator-supplied secret, `GITEA_ADMIN_TOKEN`, and never an
admin password. That is strictly better than what was planned, and it was forced
by a constraint discovered rather than designed around.

**Deactivating a user does not revoke its tokens.** A token belonging to an
inactive account still authenticates against the OCI registry — verified by
pulling with one. The line above calling deactivation "defense in depth" is
correct, but understated the risk: it is not a second layer, it is not a layer
at all on its own.

Worse, the two operations interact. Once the account is inactive, the API
returns `403` to any attempt to delete that user's tokens. Revoking in the
intuitive order — deactivate, then clean up — therefore leaves a **working**
credential in the customer's CI that the portal can no longer remove. The order
in `revokeRegistryCredential` is load-bearing and commented as such: delete the
tokens, then deactivate.

Both of these are the kind of thing a unit test with a mocked client asserts
happily in either order. The tests that exist assert the *order* and the *auth
header per endpoint* precisely because those are what the real service rejects.

### Removing a member does not revoke this credential

Removing somebody takes away their session and their Zitadel grant. It does
nothing about the registry, and cannot be quietly made to: the credential is one
password shared by the whole organization, and by the time a person leaves it is
in the customer's CI, their pull secrets and probably a laptop or two. Rotating
it the moment an administrator presses "remove" would turn an offboarding into
an unscheduled outage in a system the portal cannot see, at a moment nobody
chose. That is a worse failure than the one it prevents, and it is one the
portal would have caused.

So the portal reports it and leaves the decision with the people who know what
depends on the credential. The registry panel names anyone who was shown the
password and has since been removed, next to the button that replaces it.

Two details make it useful rather than noise. The `registry.reveal` audit entry
records **which token** was revealed, so the warning is about the credential
live now rather than about history — replacing it answers the warning, and a
warning that survives its own fix is one people learn to scroll past. And the
address shown comes from the access-revocation record rather than the directory,
which no longer holds this person: an alert naming an opaque user id is one the
reader cannot act on.

This also depends on the audit log being permanent, which it is, and on reveals
being audited at all, which is why they are — a rotation is visible from its
consequences, but a copy is visible from nothing else.

### Related fix: optional configuration must tolerate being blank

Registry integration is optional, and the schema said so: `GITEA_BASE_URL` was
`z.string().url().optional()`. But a Helm chart renders an unset optional value
as `""`, not as an absent variable — and an empty string is not a valid URL, so
every install *not* using the registry would have failed schema validation at
boot and taken the entire portal down over a feature it had declined to enable.

The schema now treats blank as absent. This was caught by a test asserting the
unconfigured path, not by review.

## Notifications

An event bus with pluggable adapters: `BrevoEmailAdapter`,
`SlackWebhookAdapter`, `MSTeamsWebhookAdapter`, `GoogleChatWebhookAdapter`,
`GenericWebhookAdapter`. Routing is `Channel` (a set of events + release
channels) → `Target` (a destination), configurable by admins globally and by
`org-admin` per tenant.

The in-app feed is not configurable and not an adapter — it is written
unconditionally on every event, so there is always one delivery path that cannot
be misconfigured into silence.

### The in-app feed has no read state, on purpose

Feed rows are written per *organization*, not per user, because the emitters
know which tenant an event concerns and nothing more — an approval or an expiry
is a fact about the organization, not about whoever happens to be logged in.

That makes an unread badge the wrong feature rather than a missing one. Read
state on an org-scoped row means the first colleague to open the tray marks the
release announcement read for everyone else, which is a worse outcome than
having no badge: a notification nobody sees is indistinguishable from one that
was never sent. The feed therefore shows the recent list and no unread count.

Per-user read state is possible — `InAppNotification.userId` exists and is
currently unset — but it needs a decision about who a notification is *for*
before it can be modelled, and fanning every event out to a row per member is a
write amplification worth agreeing to deliberately rather than by accident.

The rendering of an event into a sentence lives in the feed service rather than
the component, next to a test that asserts no message contains the string
`undefined` when its payload is empty. The payload shapes belong to the
emitters, so this is exactly the coupling that breaks quietly and reaches a
customer as a literal "undefined" in their tray.

**Cost, accepted knowingly:** the feed sits in the root layout and reads the
session, which makes every route dynamic — `/signup`, `/suspended` and the
404 page were statically prerendered before it landed. That is three trivial,
low-traffic pages losing prerendering in exchange for a header component the
epic requires on every authenticated page. If it ever matters, the fix is a
route group that scopes the feed to authenticated routes rather than the root,
not making the feed lazier.

### Notification delivery

Events are written to `NotificationOutbox` in the same transaction as the state
change that produced them, and delivered by a worker.

**Why an outbox rather than dispatching inline:** every adapter is a call to a
third party that will eventually be slow or down. Dispatching inline either
blocks the user's request behind Slack's availability or, if fired and
forgotten, loses the notification when the process restarts. The outbox makes
"the org was suspended" and "somebody will be told" a single atomic fact, and
lets retries be a property of the queue rather than of each call site.

Delivery is at-least-once with exponential backoff and a `dedupeKey`, because
duplicate delivery is an annoyance and lost delivery of a "license expires
today" alert is a customer outage.

The same key deduplicates the in-app feed, not just the outbox. A CronJob has a
`backoffLimit`, so a `scan-expiry` pod that dies after emitting is retried and
emits again; without a unique key on the feed collection the customer would see
the same "license expires in 7 days" card twice and reasonably conclude the
portal is broken. The key is scoped to the organization because release fan-out
deliberately reuses one seed across every customer — see [Releases and
channels](#releases-and-channels) — so a global key would let the first
customer's card suppress everybody else's.

Scheduled work — license expiry warnings at 30, 7, and 0 days — runs as a
**Kubernetes CronJob invoking a worker command**, not as a Next.js route handler
poked by an external scheduler. Route handlers scale with replicas, so a cron
that hits one is a cron that fires N times or zero times depending on routing.

Webhook targets are an SSRF surface: a user supplies a URL and the server
fetches it. Targets are validated against an allowlist of the known providers'
hostnames, generic webhooks are restricted to HTTPS with private and
link-local address ranges blocked, and redirects are not followed.

### Blocking private address ranges is not enough on its own

The obvious guard — parse the hostname, and if it is an IP address in a private
or link-local range, refuse — has a hole. `https://0177.0.0.1/`,
`https://0x7f.0.0.1/`, `https://127.1/` and `https://2130706433/` are all read
as `127.0.0.1` by some resolvers and C library implementations, and Node's
`isIP()` returns `0` for every one of them. A check that only rejects
*recognised* private addresses will wave all four through, because to it they
are ordinary hostnames.

So the rule is inverted. A hostname whose final label begins with a digit or
`x` is treated as an address literal, not a name. Real DNS suffixes are
alphabetic — there is no `.1` or `.0x7f` TLD — so a trailing numeric label means
somebody is writing an address, and if it cannot be parsed into one we refuse
rather than resolve it. Refusing an unparseable address is the safe failure;
resolving it is not.

The same reasoning covers the provider allowlists. `hooks.slack.com.evil.test`
contains the string `hooks.slack.com`, so the comparison is an exact match or a
match on `'.' + allowed`, never `includes`.

### The URL is validated again at delivery time

The stored ciphertext is decrypted and re-checked by `assertSafeWebhookUrl`
before the worker calls it, even though nothing can reach the database without
passing the same check on the way in. This is deliberate: the check at write
time protects the database, and the check at send time protects the network.
They defend against different failures — a future code path that writes a target
without validating, a restored backup, a direct database edit — and the second
one is the only one standing between an attacker-controlled string and an
outbound request from inside the cluster.

For the same reason the worker resolves the hostname and checks the resulting
addresses before fetching, and sets `redirect: 'error'`. A hostname that passes
every textual check can still resolve to `169.254.169.254`, and a host that
answers honestly on the first request can answer with a 302 to the metadata
endpoint on the second.

### A webhook URL is a bearer credential

The path of a Slack or Teams webhook URL is the entire secret; anyone holding it
can post as the integration. So targets are write-only from the portal's point
of view: the URL is accepted, encrypted, and never returned — not to the page,
not in the audit entry, which records the host only. There is no "reveal"
affordance because there is no version of revealing it that is safer than
deleting the target and adding a new one, which is also how rotation works.

Channel target ids are checked against the tenant's own targets rather than
trusted from the form. They arrive from a browser, so without that check an
organization could name another organization's target id and have its events
delivered into somebody else's Slack.

### FalkorDB's own routing

The notification matrix has two audiences. A customer wants their own licence
expiry in their own Slack; FalkorDB wants every customer's quota request in an
internal channel. Both are the same mechanism — a rule matching events to
targets — differing only in reach, so a channel whose `organizationId` is absent
matches every organization. `resolveTargets` already unions
`{ organizationId: { $exists: false } }` with the tenant's own rules, so a single
query serves both.

The write path is a separate `GlobalNotificationSettingsRepository` rather than a
nullable tenant on the existing one. A repository that took `TenantContext | null`
would make the difference between "this customer's Slack" and "every customer's
Slack" one argument that could be defaulted, forgotten, or passed straight
through from a request. Two classes cannot be confused by accident.

For the same reason `/staff/notifications` is a separate page rather than a
checkbox on `/notifications`, and `notification:configure-global` is a separate
permission held only by `super-admin`. An org admin holds
`notification:configure` over one tenant; this one decides where every
customer's events are copied, and a checkbox is too easy to leave ticked.

Three smaller consequences:

- The reference check runs in both directions. A global rule may only name
  global targets — accepting a customer's target id would point FalkorDB's
  firehose at that customer's Slack — and a customer's rule still may only name
  their own.
- Audit entries for these changes carry no `organizationId`. The change belongs
  to no customer, and stamping one would put a FalkorDB-internal decision into a
  customer's audit view.
- The unique index on `{ organizationId, name }` indexes a missing organization
  as null, so two global targets cannot share a name while a customer may still
  reuse one. That is the behaviour wanted, and needed no second index.

### The worker ships as a second entrypoint in the same image

Delivery runs from two Kubernetes CronJobs — `drain-outbox` every minute and
`scan-expiry` daily — rather than from a timer inside the web process. An
interval in the server fires once per replica, so two replicas send every
notification twice. An external cron calling a route handler fires against
whichever replica the ingress happened to pick, or against none at all during a
rollout.

Neither CronJob needs to be the only one running. `claimDueOutboxRows` leases
rows with an atomic find-and-modify, and an integration test runs two claimants
against six rows and asserts they split them with no overlap. `concurrencyPolicy:
Forbid` is set anyway, not for correctness but to stop a wedged delivery target
accumulating a pod a minute.

### The lease has to outlive the batch

A lease that expires while the row it covers is still being delivered does not
protect anything: the next run claims the row again and the customer gets the
webhook twice. That makes the lease duration a function of how long a batch can
take, which is a function of how the batch is delivered.

Delivering sequentially made that number unbounded in practice. Fifty rows
against a host that black-holes packets is fifty ten-second timeouts, so one
unresponsive target delayed every other customer's notification behind it and
blew through any lease worth setting. The worker therefore delivers ten rows at
a time from a shared queue, which puts the worst case for a full batch at about
a minute, and the lease is five — long enough to cover the batch with room for a
slow database, short enough that a pod killed mid-flight releases its rows
within one retry cycle rather than one shift.

Concurrency also made a second query worth avoiding: a hundred rows aimed at one
Slack target used to decrypt and fetch that target a hundred times. The batch
now caches the in-flight promise per target id, so rows that share a target join
one query rather than racing to repeat it.

The worker is bundled by tsup into a single CJS file rather than shipped as a
second traced application. Next's `output: 'standalone'` traces only what the
HTTP server reaches, so `src/worker/main.ts` is invisible to it and would
otherwise be missing from the image — the feature would be configurable in the
UI and silently undeliverable in production. Bundling it into the same image as
the server, rather than a separate one, means the two cannot drift: a change to
the outbox schema reaches the reader and the writer in the same deploy or
neither.

The command is validated before the database connection is opened, so a typo in
a CronJob's arguments fails with a usage line rather than a configuration error
from a database it had no business touching.

### Some failures are not worth retrying

Backoff assumes the next attempt could go differently. Two classes of failure
guarantee it will not, and retrying them costs eight delivery slots to arrive at
a state that was already known on the first attempt:

- **The target's stored configuration cannot be read.** A ciphertext that will
  not decrypt, or that decrypts to something that is not the JSON the adapter
  expects, is a target that was written wrong or a key that was rotated without
  re-encrypting. Six hours will not fix either.
- **The target answered "no", not "not right now".** A 4xx other than 408 and
  429 is the receiving end saying the request is wrong — a deleted Slack webhook
  answers 404 forever. 408 and 429 are excluded deliberately: they are the two
  4xx codes that mean "try again", and treating them as permanent would abandon
  notifications purely for arriving during a burst.

Both land the row in `ABANDONED` immediately rather than after the eighth
attempt. `ABANDONED` is the terminal state worth alerting on — it means nobody
was told — so the point of reaching it early is that the alert fires while the
cause is still fresh, instead of six hours later when whoever deleted the
webhook has moved on. Everything else — connection refused, a timeout, a 5xx —
still retries, because those are the failures a later attempt genuinely fixes.

The distinction is visible in the drain result, which now counts `delivered`,
`failed`, and `abandoned` separately. Log-wise the difference matters: a
`failed` row is a warning and an `abandoned` one is an error, because only one
of them will be tried again.

## Releases and channels

`STABLE`, `BETA`, and `LTS` are attributes of a registered `Cluster`, editable
after registration so that following a beta and then going back to production is
an edit rather than a second registration that spends quota on an install the
customer already has.

Filtering, though, is a property of the **routing rule**, not of the cluster. A
`NotificationChannel` names the release channels it wants and an event is
delivered when they match, so a customer running only production is not paged
about a beta build. Deriving the filter from the customer's clusters instead was
considered and rejected: an organization with a beta cluster and a production
cluster wants both kinds of announcement, but not necessarily in the same Slack
channel, and only the routing rule can express that. The cluster's channel is
the record of what they are running; the rule is the record of what they want to
hear about.

A `Release` record is what makes those notifications possible: the notification
matrix has "New Release / Security Patch" and "Upgrade Advisory" events, and
something has to assert that version X shipped on channel Y with these breaking
changes. That assertion is a first-class record, not a side effect of a webhook.

**Publishing is manual, ingestion is automatic**, and the model is designed for
both. `Release.source` is `MANUAL | GITHUB`, and `status` is `DRAFT |
PUBLISHED`. Manual publishing is an admin composing the release and choosing its
channel. GitHub ingestion watches **this repository's releases** —
`FalkorDB/FalkorDB-Enterprise`, which is what produces the chart and images
customers consume — and creates the same record as a `DRAFT` with `source:
'GITHUB'` and a `sourceRef` pointing at the release tag.

**Where an ingested release gets its channel:** CHANGELOG.md. The heading form
`## [VERSION] - YYYY-MM-DD (CHANNEL)` is fixed by that file's own conventions
section, `scripts/generate-release-docs.mjs` generates the published changelog
and the compatibility matrix from it, and the release workflow refuses to
publish a version whose heading declares no channel. Ingestion reads the same
file at the release tag — the tag rather than the default branch, because a
release is cut on a branch and tagged there. A `Security` subsection makes the
record a security patch and a `Breaking changes` subsection fills its breaking
changes, so the fields that drive notification quality come from the one place
they are already written down.

A tag whose changelog section is missing, or whose heading declares no channel,
is logged and left alone. Nothing is defaulted: a beta build ingested onto
`STABLE` would eventually be announced to every customer who asked for
production only.

Reading at the tag is also what makes the LTS line work at all. An LTS patch is
cut from a long-lived `release/X.Y.x` branch that is deliberately never merged
back, so its changelog entry never reaches the default branch — a sync that read
the tip would miss every LTS release there is.

The one thing the tag cannot carry is a channel that changes afterwards. A
shipped version is promoted to `lts` by editing its heading and regenerating the
compatibility matrix, and a tag's copy of the file is frozen. So each run also
reads CHANGELOG.md at the tip and moves tracked records onto the channel it
declares. A version the tip does not mention is left alone rather than demoted,
since that is what an LTS line and a folded beta both look like from the trunk.
Nothing is announced: promotion re-labels a release customers were already told
about, and re-announcing a version they have been running for months would read
as a new one.

**Why ingestion produces a draft rather than publishing directly:** what it
removes is transcription — copying a version, a channel and a list of breaking
changes out of a changelog and into a form, which is where a release ends up on
the wrong channel. What it leaves is the judgment. Publishing fans out to every
active customer's Slack, email and in-app feed in one transaction, and nothing
un-sends it, so a human reads the draft the customers will read and presses the
button.

**Why polling rather than a webhook or a workflow step:** a workflow calling
into the portal would mean the portal's first machine-facing write endpoint, on
a control plane that holds the licence signing key and every customer's registry
credential, guarded by a shared secret in repository settings. Polling needs no
inbound exposure and a read-only token. It also survives its own failures: a
push is one delivery attempt made while the portal happens to be mid-rollout,
while a poll that finds nothing finds it on the next tick. The cost is minutes
of latency on a draft that a human still has to approve.

Notification dispatch fires on the `DRAFT → PUBLISHED` transition, never on
record creation, so the ingestion path and the manual path have exactly one
place where customers get told.

### Publishing fans out per organization, inside the transaction

A release is not tenant data, but a release *announcement* is: whether a given
customer hears about it depends on that customer's own targets and channel
subscriptions. So publishing walks every `ACTIVE` organization and emits a
`RELEASE_PUBLISHED` event scoped to each one, rather than emitting a single
global event and hoping the delivery layer sorts it out.

That walk is deliberately unbounded, unlike every other list read in the
system. A fan-out that silently stopped at the first 500 customers would
announce a release to some of them and not others, which is a worse failure
than being slow.

The status flip and the whole fan-out share one transaction, and the flip is a
conditional update on `status: 'DRAFT'` rather than a read followed by a write.
Two admins clicking Publish at the same moment therefore produce one
announcement, not two: the second update matches nothing, and the service
raises rather than emitting a duplicate set of events.

**The dedupe key is seeded with the release alone, deliberately not with the
organization.** The outbox is unique on `(dedupeKey, targetId)`, so each
customer's own targets still get their own row — different targets, no
collision. But a *FalkorDB-global* target, one with no `organizationId`, is
reached once per customer during the walk and collapses onto a single row.
Staff hear about a release once, not once per customer. This is the property
that would quietly regress into a mailbox flood, so it has its own test.

Getting that collapse to work correctly forced a fix in the outbox writer.
Queueing originally inserted rows and swallowed the duplicate-key error, on the
reasoning that the row already existing *is* the success condition. That works
outside a transaction and fails inside one: a duplicate key aborts the
transaction server-side, and catching the error client-side does not undo that.
Every later write in the callback then fails, and `withTransaction` retries the
whole thing until it gives up about two minutes later. The fan-out is the first
code path that writes the same key twice in one transaction, so it was the
first to hit it. Queueing now upserts, which turns the collision into a no-op
update instead of an error.

## Installer wizard

The wizard produces artifacts for [scripts/install.sh](../../scripts/install.sh)
and the chart: a `values.yaml` preview and the corresponding install command.

**The license and registry password are emitted as a Secret manifest and a
values file, never inlined into a copyable shell command.** A command line with
credentials in it lands in shell history, in CI logs, and in screenshots. The
installer already supports `-f/--values` and `adminServer.license.existingSecret`,
so the safe path is also the supported one.

The wizard's field set is checked against the installer's documented flags
rather than generated from them. Generation was the original plan and turned
out to be the wrong mechanism for the right goal: the reference table gives a
flag's name, default and a sentence of prose, while a usable form field also
needs a label, a widget, an ordering, a group, whether the value is a
credential, and which artifact it belongs in. None of that is derivable from
the table. What actually matters is that a new flag cannot pass unnoticed, and
that is a coverage property, not a code-generation one. So every documented
flag must appear in exactly one of two lists — surfaced as a field, or refused
with a written reason — and a unit test parses
[docs/reference/installer-flags.mdx](../reference/installer-flags.mdx) and
fails if any flag is in neither, in both, or no longer documented. Adding a
flag to the installer breaks the portal's test suite until somebody decides
what it means. The selection rule for the surfaced set is that a field earns
its place if a first successful install can need it; flags reached for while
staring at a failure are not first-install decisions.

**The wizard is entirely client-side and has no Server Action.** Every other
form in the portal posts to one, so the deviation is deliberate: a post would
put a license key and a registry password into the server's request path, its
logs and its error reports in exchange for nothing at all. The artifacts are
pure functions of the form state, so the credentials never leave the tab. The
consequence worth stating plainly is that nothing here is audited, because
nothing here happens — issuing the license was the audited event, and this page
only formats it.

**The license is pasted, not fetched.** The portal shows a signed license once,
at issue time, and does not show it again; it is a bearer credential, and a
page that re-displays it on demand turns every logged-in session into a copy of
it. Prefilling the wizard from the license list would have silently reversed
that decision, so the user pastes what they saved.

Two smaller judgement calls, recorded because they are easy to "fix" wrongly
later:

- `--image-pull-secret` is emitted only when the wizard's manifest actually
  creates that Secret. Naming a Secret that does not exist is worse than
  omitting the flag — it produces `ImagePullBackOff` at pull time instead of an
  error at install time. The installer's own
  `create_image_pull_secret` reuses a named Secret when no username and
  password are supplied, which is exactly what makes the safe path work.
- The split between the values file and the flags is not cosmetic: the values
  file configures the *chart*, the flags configure the *installation run*. So
  `global.imageRegistry` and `adminServer.license.existingSecret` go in the
  file, which is safe to commit, and `--namespace`, `--timeout` and `--dry-run`
  stay on the command line, where they belong to one invocation.

## Comparing values before an upgrade

The epic asks for a `helm diff`. A real one needs the cluster, and the portal
has no path into a customer cluster — that is the single largest thing the
design refuses to build, because a control plane holding a kubeconfig for every
customer is a far larger thing to defend than one holding none.

So `/install/diff` compares two pasted documents. The page shows the exact
`helm get values <release> -n <namespace> -o yaml` to run, takes that output in
one pane and the values file about to be applied in the other, and reports what
would change.

**It runs entirely in the tab**, for the same reason the installer wizard does:
a values file routinely carries a registry password or a license key, and
posting a production cluster's live configuration to us in order to be told
which keys differ would put customer credentials in our logs in exchange for
nothing. `parseValues`, `flatten` and `diffValues` are pure, unit-tested, and
imported by a client component; there is no Server Action.

**The comparison is by key path, not by line.** `helm get values` sorts its
output and strips comments, so a textual diff against a hand-maintained file
reports a difference on nearly every line while saying nothing about what would
actually change in the cluster. Flattening both sides to leaf paths
(`global.imageRegistry`, `nodes[0].name`) makes reordering and formatting
invisible and real changes obvious.

Smaller decisions worth keeping:

- An empty paste is a valid empty document, because that is what a release
  installed with no overrides produces, and "you have no overrides" is a
  legitimate half of a comparison. The `USER-SUPPLIED VALUES:` header Helm
  prints without `-o yaml` is stripped rather than rejected.
- An empty nested section is a leaf. Otherwise `redis: {}` and an absent
  `redis` compare equal, and clearing a section is exactly the kind of change
  worth seeing.
- Values on paths that look like credentials are masked, but still reported as
  changed. Over-masking is the safe direction — the page's question is *which*
  keys change, and a masked value answers it.
- The page says plainly that this is a comparison of two files and not a
  rehearsal of the upgrade, and points at `helm upgrade --dry-run` for that.

## Documentation, not embedded

The epic calls for embedding `docs.falkordb.com/enterprise` in an iframe. That
is not possible. The site is Mintlify-hosted and serves:

```
x-frame-options: DENY
content-security-policy: ... frame-ancestors 'self'
  https://dashboard.mintlify.com https://app.mintlify.com; ...
```

Both headers are set by Mintlify's platform, not by our `docs.json`, so this is
not a configuration we can change. Any iframe attempt renders a blank frame in
every browser.

What the site does expose is machine-readable content: `/llms.txt` and
`/llms-full.txt`, advertised in a `link` header alongside an API catalog and MCP
server card. So the portal renders documentation by **fetching and rendering
content server-side**, styled with `ui-library`, rather than by framing a
foreign origin.

**Why that is the better outcome anyway:** an iframe would have given us a
second scrollbar, a broken theme boundary, and no ability to deep-link a
customer to the section relevant to their cluster's version. Rendering content
we fetch means search, version awareness, and portal chrome are all ours.

The upgrade guidance pages — changelogs, breaking changes, Helm values diffs —
are rendered from the portal's own `Release` records regardless, because those
are tenant-aware views the docs site cannot produce.

### What that turned into

`/docs` lists every page, grouped and filterable; `/docs/<slug>` renders one.
Both are server-rendered, so the Markdown machinery never reaches the browser —
the index page costs 881 B of client JavaScript, which is the filter box.

**The index is an allowlist, not a menu.** `fetchDocsPage` refuses any slug the
index does not list, and refuses it before fetching anything. That is a security
control rather than tidiness: the slug arrives from the URL bar, so without it
`/docs/…` is a fetch of an attacker-chosen path on the docs origin, rendered
inside an authenticated page. For the same reason `slugFromUrl` rejects any URL
whose origin is not the docs site, which also rules out a lookalike domain
appearing in the index one day.

**Only Markdown pages are listed.** `llms.txt` advertises 142 entries, and one
of them is the OpenAPI spec as `.json`. Appending `.md` to it produces a 404, so
the entry is dropped from the index rather than offered as a link that cannot
work.

**Grouping is derived, not read.** `llms.txt` has its own headings, but they put
141 of the 142 entries in a single bucket called `Docs` — fine for a crawler
reading the whole file, useless as navigation. Sections come from the first path
segment instead.

**Raw HTML stays off, and the components are flattened before rendering.** The
`.md` endpoint is not plain Markdown: it still contains `<Warning>`, `<Steps>`,
`<Card>`, `<ResponseField>` and a dozen more, with no blank line between the tag
and its content. A Markdown parser reads that as one block of raw HTML, and a
renderer that declines to emit raw HTML — the correct posture for content
fetched from another origin into an authenticated page — drops the tag *and the
sentence inside it*. The page still renders and still looks finished, having
quietly lost its safety warnings; `index.md` is almost entirely inside `<Steps>`
and would have rendered as a title and nothing else. So `flattenMdxComponents`
removes the tags first and keeps what they held: callouts become blockquotes,
`title` becomes a heading, and `href` and `name` are preserved because a card
without its `href` stops being a link and a glossary entry without its `name`
no longer states the term it defines. Everything it has never heard of is
treated as a wrapper, so a component added next month costs a reader a heading
rather than a page.

**Cross-references are rewritten during rendering, not in the text.** Every
internal link in the corpus is root-relative and extensionless —
`](/databases/networking)` — which resolves against the portal and 404s. There
are 85 of them. Rewriting is done per link node rather than by regex over the
Markdown so that a link-shaped string inside a code fence stays the string it
was, and a path the index does not list is sent to the docs site rather than
into a portal route that cannot serve it.

**It degrades instead of failing.** The fetch has a five-second timeout and
returns null on any error, and `/docs` then renders an explanation and a link to
the docs site. The navigation links here unconditionally and a browser test
walks every entry, so a nav destination that 500s because somebody else's site
is down would be a worse outcome than one that explains itself. Content is
revalidated hourly.

None of the above was designed from the epic. All 141 pages were fetched and
inspected first — which is what turned up the components, the absence of
descriptions on 98 entries, the `.json` entry, and a slug containing `&`. An
early sample of a single page had suggested there were no components at all.

## Packaging

`packages/portal/Dockerfile`, multi-stage on `node:24-alpine`, using Next's
`output: 'standalone'`. It follows [packages/admin-ui/Dockerfile](../../packages/admin-ui/Dockerfile)'s
structure — manifests copied first for layer caching, `ui-library` built before
the app, `pnpm deploy --prod` with injected workspace packages.

The base image is **pinned to a digest**, not just the `24-alpine` tag, through
a global `ARG` both stages share. A tag moves, so two builds of the same commit
can produce different images — which means a passing scan says nothing about the
image that shipped, and a base regression arrives looking exactly like "nothing
changed". CI scans the built image with Trivy for fixed HIGH and CRITICAL
findings and fails on them, so the digest is what makes that gate mean
something; bumping it becomes a commit with a diff, which is the point.

The chart is **`helm/falkordb-enterprise-portal`, separate from
`helm/falkordb-enterprise`**. The customer chart is an artifact customers
install; the portal is infrastructure FalkorDB runs. Merging them would ship the
portal's Zitadel, Gitea, and MongoDB configuration surface — and its license
*signing* key path — into every customer's values file.

**MongoDB runs in-cluster**, deployed as a single-node replica set alongside the
portal rather than as a managed service. Zitadel and Gitea are already
self-hosted, so this keeps the whole control plane in one operational model with
one backup story.

Single-node is a deliberate starting point, not an oversight: the replica set
exists for transactions, not availability, and adding members later is an
operational change rather than a schema one. What it does mean is that
**MongoDB's backup is the portal's disaster recovery plan** — there is no second
copy of an organization's quota or a customer's Gitea token, and the encrypted
token is unrecoverable from Gitea itself. Scheduled backups are a launch
requirement, not a follow-up.

#### Bootstrapping the replica set

A replica set with authentication needs two things a plain `mongod` does not: a
shared keyfile for internal member authentication, and an `rs.initiate` that
runs once. Both are awkward enough to be worth writing down.

The keyfile cannot be mounted from the Secret directly. `mongod` refuses to
start if the keyfile is readable by anyone but its owner, and a Secret volume is
mounted owned by root — so the only file mode that lets `mongod` read it is one
that grants group access, which `mongod` then rejects. The way through is an
init container that copies it to an `emptyDir` at mode 0400, where the copy is
owned by the uid that made it.

Initiation runs in a `postStart` hook rather than an init container, because it
has to happen *after* `mongod` is listening. It is guarded by an authenticated
`rs.status()` — if that succeeds the set is already up and the hook exits, which
matters because re-initiating a live set is destructive. On first boot the probe
fails, the hook initiates the set, waits for the member to become writable, and
creates the root user through the localhost exception, which is open only until
that user exists.

The member is advertised under the stable per-pod DNS name from the headless
Service. That name is written into the replica set config on the data volume the
first time the pod starts and changing it afterwards needs a manual
`rs.reconfig`, so it is worth getting right once rather than defaulting to
`localhost`.

The connection string is assembled by the chart, not stored in the Secret, so
there is one copy of the password rather than two that can drift. The password
is substituted by Kubernetes' own `$(VAR)` expansion, resolved in the kubelet,
which keeps it out of the rendered manifest and out of `helm get manifest`. That
does constrain it to characters with no meaning in a URI; the chart enforces the
same rule on the username, which is the half it can see.

This whole sequence was rehearsed against a real `mongod` in Docker before it
was written as a template — keyfile permissions, initiation, the localhost
exception, restart idempotency, and a two-collection transaction over the
resulting connection string. A template is not a good place to discover that
step three needed step two to have finished.

**The bundled database is a switch.** `mongodb.enabled=false` drops the
StatefulSet and reads `MONGODB_URI` from the Secret instead, for running against
a database somebody else operates. It still has to be a replica set.

#### Backups

A nightly CronJob dumps the database and uploads it to S3-compatible object
storage. Two containers in one pod, dump then upload, in that order — an upload
container that started independently would copy a partial archive and report
success.

`mongodump --oplog`, not a plain dump. `--oplog` records the writes that land
*while* the dump runs, so the archive is a point in time rather than a smear
across one. Without it a restore can produce a license whose quota row is
missing, which is the exact invariant the application spends a transaction to
maintain — it would be a strange thing to protect at write time and then throw
away at restore time. It does constrain the job to a full-instance dump, since
`--oplog` and `--db` are mutually exclusive.

S3-compatible rather than S3, because the same client reaches AWS, R2, GCS and
MinIO — which keeps the destination a deployment decision rather than a chart
one, and leaves the open question genuinely open. What the chart does insist on
is that a destination exists: enabling backups without one is the single mistake
that yields a green nightly job and no backups, so it fails at install time.

Retention is deliberately absent. Object lifecycle rules do it in the storage
layer, where they keep working if this CronJob breaks, and where a compromised
backup job cannot use them to erase history. Reimplementing that as a prune step
would be strictly worse at both.

The backup job takes its database connection from a helper that carries the
connection and nothing else, rather than the shared environment block. The
shared block includes the license-signing key, and a backup pod that can mint
licenses is a much larger thing to lose than a backup pod.

Dump, destroy, restore and verify were exercised against an authenticated
replica set before this was written, and the upload step was run as rendered —
extracted from the manifest, not retyped — against a real S3-compatible endpoint
as an unprivileged uid with a read-only root filesystem. The restore procedure
is in the chart README, because a backup nobody has practised restoring is a
belief rather than a backup.

The portal image is not obfuscated. The Admin Server is obfuscated because it
runs on customer hardware and embeds the license *verifier*; the portal runs on
FalkorDB hardware and the threat model is different.

The image runs as UID 1000 with a read-only root filesystem. Next writes to two
paths at runtime, `/tmp` and `.next/cache`, and both are backed by `emptyDir`;
nothing else in the image needs to be writable. CI starts the built image under
exactly those constraints and waits for `/api/health`, so a new runtime write
path fails there rather than on the first deploy.

CI also runs the worker entrypoint with no configuration and requires it to
exit complaining about configuration. That looks like a strange thing to
assert, but it is the only cheap proof that the worker bundle is in the image
at all: Next's standalone output traces what the HTTP server reaches, and the
CronJob entrypoint is invisible to it. Without the check, a missing bundle
ships silently and fails on a schedule.

## Running it locally with nothing behind it

`pnpm dev:demo` starts the portal with a MongoDB container, a populated demo
database, and seven people you can be. No Zitadel tenant, no Atlas cluster, no
registry, no configuration to copy from anyone. `Ctrl-C` takes it all down
again; `pnpm dev:demo:reset` drops the database first.

The alternative was what we had: a `.env.local` handed around, pointed at a
shared Zitadel org and somebody's Atlas cluster. That makes a new contributor's
first day an access-request queue, makes every local experiment visible to
everyone else, and means the pages nobody visits — a suspended organization, an
org with no quota yet — are only ever seen in production.

### Personas rather than accounts

`src/lib/dev/personas.ts` names seven sessions, and `/dev/sign-in` mints one on
request. Three are customers with different roles at the same organization, two
are staff at different privilege levels, and two exist purely to reach states
that are otherwise hard to arrive at: a suspended customer, who should be
redirected away from everything, and an authenticated stranger with no
organization, who should land on the signup form. The read-only viewer is there
because "what does this look like to someone who cannot do it" is the question
most likely to go unasked.

The staff org id the personas are minted with is the same constant the harness
passes as `ZITADEL_STAFF_ORG_ID`, imported from one module, so the seed and the
session cannot drift apart.

### Why a route, and why it is locked twice

The Playwright suite mints its cookies from the test process precisely so that
the application contains no bypass — see the testing section. Nothing owns a
developer's browser, though, so the choice for local work is a route in the app
or a real identity provider.

It is a route, guarded twice. `process.env.NODE_ENV === 'production'` is
inlined by Next at build time, so in a production image the check is a
constant and everything after it is dead code. `PORTAL_DEV_SIGN_IN=1` is a
second lock that is not load-bearing: it exists so a plain `next dev` pointed
at a colleague's database does not hand out super-admin to anyone who guesses
the URL. Only the harness sets it.

The route has no test. That is deliberate — a test asserting it works is a test
that fails the day somebody strengthens the guard, which is exactly the change
nobody should have to argue for.

It lives at `/dev/sign-in` and not `/__dev/sign-in`, which reads better,
because Next treats a path segment beginning with an underscore as a private
folder and excludes it from routing entirely. A route file that plainly exists
and serves the framework's own 404 is a disorienting way to spend ten minutes.

### The demo data

`scripts/dev-seed.ts` writes through the application's own models and index
migration, not through raw collection inserts, so a seed that violates a schema
or a uniqueness constraint fails here rather than looking fine until
production. It covers the states the UI has to handle and not much else: an
organization at three quarters of its quota, a cluster awaiting binding
alongside two active ones, a license that expires in nine days and one that was
revoked, a pending quota request, a delivery rule with events on it, a draft
release, and enough audit entries to fill a page.

Secrets — the session key, the encryption key, the license signing key — are
generated once into `.dev/secrets.json` (gitignored, mode 600) and reused. A
fresh `AUTH_SECRET` per run would sign you out on every restart, which is a
small thing that becomes the loudest thing about the harness.

`DEV_MONGODB_URI` skips the container and uses whatever you point it at, for
when the data needs to outlive the process. A container is thrown away on exit,
which is usually what you want and occasionally maddening.

## Observability

Logs are structured JSON on stdout, written with **pino**, picked up by Fluent
Bit, shipped to **VictoriaLogs**, and read in **Grafana**. Nothing in the
application knows about any of that — it writes lines to stdout and the platform
does the rest — but the pipeline is why the format is what it is.

**JSON in development too**, not pretty-printed. A developer looking at the
console and an operator looking at Grafana should be reading the same fields; a
transport that only exists locally means the one time it matters, in an
incident, the format is unfamiliar and a field someone relied on turns out to be
a rendering artifact rather than real.

Every line carries `service: 'portal'` and, via `loggerFor(component)`, a
`component` — `worker`, `outbox`, `members`. The component is the difference
between "the portal logged an error" and "the outbox logged an error", which is
the granularity a Grafana query needs to be useful. Call sites use
`loggerFor(...)` rather than the root logger for exactly that reason.

`LOG_LEVEL` is read straight from `process.env`, deliberately not through the
validated `serverEnv()`. One of the things most worth logging is that
configuration validation failed, and a logger that cannot initialise until the
configuration parses cannot report that. An unrecognised level writes one raw
warning and falls back to `info` rather than refusing to start: a typo in a
values file should not be an outage.

The logger redacts `url`, `token`, `secret`, `password`, `apiKey`, and
`authorization` at the top level and one level down, plus the `authorization`
and `cookie` headers. This is belt-and-braces on top of never logging those
fields on purpose — a Slack webhook URL *is* a bearer credential, and the way
one reaches a log is a well-meant `log.error({ target }, ...)` written months
after everyone stopped thinking about it.

### Kept forever, read a page at a time

Neither audit entries nor in-app notifications expire. A TTL on an audit log
makes it useless for the thing an audit log is for — answering a question about
something that happened before anyone thought to ask — and a retention window is
much easier to add later than the history it already deleted.

Unbounded retention is precisely why the *read* has to be bounded, so the audit
view pages with a **keyset cursor** rather than a page number. Offsets get more
expensive the further in you go, because the server still walks the rows it is
skipping, and they shift under concurrent writes — a new entry arriving between
page one and page two pushes a row from one to the other, so a reader paging
through their own busy log sees one entry twice and never sees another. A cursor
of `(createdAt, _id)` is stable regardless of what arrives, and rides the
existing `{ organizationId: 1, createdAt: -1 }` index. The `_id` is in there
because several entries written by one request share a millisecond, and a cursor
on time alone either repeats them or skips them.

The cursor is URL input, so an unparseable one is treated as "start at the
beginning" rather than as a 500. It cannot be used to see anything: the tenant
filter is applied regardless, so the worst a forged cursor achieves is choosing
where the reader's own log starts.

Paging is forward-only, with links rather than buttons. Links make a position
shareable and let the browser's own back button walk backwards, which is a
back-stack the page would otherwise have to keep itself.

The in-app feed is deliberately *not* paginated: it is a nav dropdown capped at
twenty, rendered on every page load behind the nav, and it is a notification bell
rather than an archive. Everything it summarises is durable elsewhere — the
license, the release, the quota request — and reachable from the page that owns
it.

## Testing

Repo convention holds: `*.test.ts` for Vitest, `*.spec.ts` for Playwright.

Integration tests run **Testcontainers** for MongoDB (as a single-node replica
set), Zitadel, and Gitea. Mocking these was rejected: the three highest-risk
behaviors in the system are token revocation actually revoking pulls, tenant
scoping actually isolating queries, and the provisioning saga actually
compensating. All three are properties of the real systems' semantics, and a
mock asserts only that we called it the way we expected to.

Tenant isolation gets dedicated tests that attempt cross-tenant reads through
every entry point, and they are treated as security tests rather than
functional ones.

### Two tests read files that are not code

The installer wizard's field set is checked against
`docs/reference/installer-flags.mdx`, and the chart's environment block is
checked against the schema in `src/lib/env.ts`. Both exist because the failure
they catch is invisible to every other kind of test: a variable renamed in the
schema but not in the chart type-checks, lints, passes the unit, integration
and browser suites, and builds a clean image, before throwing `Invalid server
configuration` on the first pod that starts.

The chart test reads `_helpers.tpl` as text rather than rendering it with
`helm`, so it runs wherever `pnpm test` runs. That costs nothing in fidelity
because every workload in the chart draws its environment from that one helper
— which is itself deliberate, so the web Deployment and the CronJobs cannot
drift apart.

Both tests open with a case asserting they parsed anything at all. A coverage
test whose parser silently stops matching does not fail; it compares two empty
sets and passes, which is worse than not having it.

### CI

`.github/workflows/portal.yml`, split into five jobs by what each one needs
rather than by what it is: types/lint/unit need only Node, integration and
browser need a Docker daemon for Testcontainers, the image job needs Buildx,
and the chart job needs Helm. One combined job would make a lint error wait on
a container build.

The path filter includes `docs/reference/installer-flags.mdx`, which is not a
portal file. It is there because a unit test reads it: documenting a new
installer flag without deciding whether the wizard should expose it is exactly
what that test exists to catch, and it touches nothing else in the filter.

The chart job renders with the optional pieces switched on — a template that
only renders under its defaults is half tested — validates the result with
`kubeconform -strict`, and then asserts that rendering with *no* values fails.
That last one guards the chart's own required-value checks, which are otherwise
the kind of thing that gets deleted to make an unrelated command work.

### Browser tests mint their own session cookies

The Playwright suite needs an authenticated browser, and the obvious way to get
one — a credentials provider switched on by an environment variable — was
rejected. That puts an authentication bypass in the shipped application and
defends it with a string comparison, so the day someone copies a `.env` between
environments, the bypass is in production.

Instead the specs mint the session cookie themselves with `encode()` from
`next-auth/jwt`, using the same `AUTH_SECRET` the server under test runs with.
The portal trusts any session cookie it can decrypt, and the `jwt` callback only
rewrites claims when a fresh OIDC profile is present, so a minted token is
indistinguishable from one Zitadel produced. Everything downstream — the session
callback, the per-request organization lookup, the permission checks, the three
redirect branches — runs exactly as in production. Nothing test-only ships.

What this deliberately does not cover is the OIDC exchange itself: claim
mapping, staff-org detection, role extraction. That is `resolveIdentityFromClaims`,
and it is unit tested against real claim payloads, which is a better place for
it than a browser.

The dev server is started from `globalSetup` rather than Playwright's
`webServer`, because it needs the MongoDB connection string and that does not
exist until the container has started. Relying on the ordering of config
evaluation, global setup, and `webServer` — and then on a mutated `process.env`
being inherited by a process Playwright spawns for us — is more undocumented
behaviour than a CI job should rest on.

### What the browser suite is for

It is not a second copy of the integration tests. The Vitest suites call
services directly against a real MongoDB and already prove the authorization
rules and the queries. What they never execute is Next.js: the server/client
component boundary, `redirect()` and `notFound()` actually producing a redirect
and a 404, Server Actions round-tripping through a form post, and the root
layout rendering at all. Those failures are invisible to a Node-only test and
total in production — a missing `'use client'` is a green suite and a blank page.

It earned its place on the first run. A spec that walks every nav link found
that `/notifications` and `/audit` answered a viewer with `notFound()`, and the
nav links every member to both. The 404 was reasoned — it avoided describing
what was behind the page — but the nav had already disclosed the page, so it
hid nothing and turned a link we drew into a dead end. Both now render an
explanation naming the role that would grant access. `/staff` keeps its 404,
because nothing links a customer there and its existence really is undisclosed.

It earned it again on the redesign. Every page type-checked, linted and built
cleanly while four of them returned 500s, because both failures were RSC
boundary mistakes — a plain function re-exported through a `"use client"`
barrel, and an icon passed from a server component into a client one. Neither
is visible to `tsc`, and `next build` renders no page that needs a session. The
spec that walks the nav found them on the first navigation.

A third one hid from it. The lookup that turns `LICENSE_EXPIRING` into "License
expiring" sat in the same client module as the checkbox list that first needed
it, and the two pages that summarise a rule's events read it from there. That
throws on the server — but only once a rule with at least one event exists, and
the fixtures had none, so the page rendered its empty state and passed. The
demo seed found it in about a minute. The fixture now includes a rule with an
event on it, which is the general lesson: an empty table proves almost nothing
about the page that draws it.

## Deliberate non-goals

| Not built | Reasoning |
| --- | --- |
| Billing and payments | Quota changes are approved by a human and invoiced outside the portal. Adding a payment processor would make the portal a system of record for money, with the compliance surface that implies, to automate a step that currently involves a conversation anyway |
| Any network path into a customer cluster | The signed license is the entire interface. A portal compromise must not reach a customer data plane |
| License revocation that stops a running cluster | Offline Ed25519 verification cannot support it. Cluster binding plus customer-chosen expiry bound the exposure instead |
| Org switching for a single user | One org per user is what keeps the tenant unspecifiable by the caller. Two organizations means two accounts |
| Automatic publishing of ingested GitHub releases | Ingestion fills the draft from CHANGELOG.md, but publishing fans out to every customer and nothing un-sends it. A human reads the draft the customers will read |
| DNS-based domain verification | The approval gate already puts a human on the claim. Revisit if open signup is introduced |
| Iframing the documentation site | Mintlify serves `x-frame-options: DENY` and a restrictive `frame-ancestors`, neither of which we control. Content is fetched and rendered instead |
| Managed MongoDB | The rest of the control plane is already self-hosted in the same cluster; a managed service would add a second operational model for one component |
| Editing or removing a member from the portal | Zitadel owns access. A remove button here would have to stay correct against changes made in Zitadel directly, and would be wrong the first time it did not |
| A `helm diff` against a live cluster | Would require cluster credentials, which is the one thing the portal must never hold. Values are compared from what the customer pastes |
| A `NetworkPolicy` shipped with the chart | Not for now. A chart-owned policy is only as good as the CNI enforcing it, and a policy that silently does nothing is worse than an explicit gap; the namespace's own network posture is the operator's to set |
| Retention windows on audit entries or the in-app feed | Kept forever. A TTL makes an audit log useless for the question it exists to answer, and deleting history is not a decision that can be walked back. Reads are paginated instead |
| Support tickets rendered in the portal | The nav links out to `support.falkordb.com`. Bringing tickets in means mirroring them locally to keep the tenant boundary in one place, syncing them on a schedule, and pushing customer emails into a CRM — a great deal of machinery, and a new way to be wrong about who sees what, to avoid one new tab |

## Open questions

| Question | Blocks |
| --- | --- |
| Zitadel issuer URL, project id, and whether the app is confidential or public | Auth wiring beyond local containers. The project id is also what member invitations grant roles on, alongside a service-user token in the Secret — an install missing either runs fine, with invitations turned off |
| Gitea base URL, and an admin token for it | Turning registry credentials on. The provisioning is built and verified against a real Gitea; it needs `config.registryUrl` and a `GITEA_ADMIN_TOKEN` in the Secret. A token, specifically — the design deliberately needs no admin password, and an install that sets neither runs fine without the feature |
| A GitHub token that can read this repository | Turning release ingestion on. `contents: read` and nothing more; the sync worker lists releases and reads CHANGELOG.md at each new tag, and never writes. Without it the worker records that it is not configured and exits, which is the right state for any install that is not the one publishing these releases |
| Which bucket, in which account, backups are written to | Turning backups on. The mechanism is built and tested; it is one `--set` away, but the destination has to be somewhere a compromise of this cluster cannot reach, and that is an infrastructure decision rather than a chart one |

