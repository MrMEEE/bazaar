# Flathub metadata, login, and Explore tab configuration

Bazaar normally talks to Flathub for two independent things: a supplemental
metadata API (curated picks, categories, stats, favorites) and a login/OAuth
flow (for favorites). Both, along with the tab that displays the metadata,
can now be reconfigured or turned off via GSettings
(`io.github.kolunmi.Bazaar`).

## Flathub API endpoints used by Bazaar

### Metadata API (base configurable via `metadata-api-url`, default
`https://flathub.org/api/v2`)

| Endpoint | Purpose |
| --- | --- |
| `/collection/category` | List of top-level categories |
| `/collection/category/{id}` | Apps in a category |
| `/collection/category/{id}/subcategories` | Apps in a subcategory (used for "show more") |
| `/collection/popular` | Popular apps |
| `/collection/trending` | Trending apps |
| `/collection/recently-added` | Recently added apps |
| `/collection/recently-updated` | Recently updated apps |
| `/collection/mobile` | Mobile-friendly apps |
| `/collection/developer/{name}` | Apps by developer (also used for KDE picks) |
| `/app-picks/app-of-the-day/{date}` | App of the day |
| `/app-picks/apps-of-the-week/{date}` | Apps of the week |
| `/app-picks/curated-app-selections/{date}` | Curated selections shown on the Explore tab |
| `/quality-moderation/passing-apps` | "Quality" badge eligibility |
| `/stats/{id}` | Per-app install stats |
| `/similar/{id}` | Similar apps |
| `/favorites`, `/favorites/{id}` | List/add/remove/count favorites (requires login token) |
| `/search?q=...` | Keyword search, used by subcategory "show more" browsing |

### Login API (base configurable via `flathub-login-url`, default
`https://flathub.org`)

| Endpoint | Purpose |
| --- | --- |
| `/api/v2/auth/login` | List available OAuth providers |
| `/api/v2/auth/login/{provider}` | Start/complete OAuth login for a provider |
| `/api/v2/auth/userinfo` | Fetch the logged-in user's profile |

### Other services (not affected by these settings)

| Endpoint | Purpose |
| --- | --- |
| `https://usebazaar.org/...` | Misc. Bazaar-project data (`bz_query_bazaar_json`) |
| `https://arewelibadwaitayet.com/api/apps` | Non-KDE "Adwaita apps" picks |
| `https://dl.flathub.org/repo/...` | Flatpak repo/screenshot CDN (not a JSON API call) |

General app browsing, installing, updating, and searching are driven by the
Flatpak remotes configured on the system and do **not** depend on the
metadata API at all.

## New GSettings keys

All keys live in the `io.github.kolunmi.Bazaar` schema and are also editable
from **Preferences**.

| Key | Type | Default | Effect |
| --- | --- | --- | --- |
| `metadata-api-url` | string | `https://flathub.org/api/v2` | Base URL for the metadata API. Empty string resets to the default. |
| `disable-metadata-fetching` | bool | `false` | When `true`, Bazaar never contacts the metadata API. Apps/search still come from enabled Flatpak remotes. |
| `flathub-login-url` | string | `https://flathub.org` | Base URL for the OAuth login flow and userinfo/favorites requests. |
| `hide-flathub-login` | bool | `false` | Hides/disables the "Login With Flathub" menu item and favorite-button login prompt. |
| `flathub-tab-title` | string | `Explore` | Label shown on the tab that displays curated/categorized Flathub content. |

## Behavior changes

- **Metadata source / disable switch** (`global-net.c`): `bz_query_flathub_v2_json*`
  now build the request URL from `metadata-api-url` instead of a hardcoded
  host, and short-circuit with a rejected future when
  `disable-metadata-fetching` is on. Toggling either setting at runtime
  re-triggers a resync of the Explore tab (`metadata_setting_changed` in
  `bz-application.c`).
- **Local fallback** (`bz-flathub-state.c`): when metadata fetching is
  disabled, or the very first metadata request fails (e.g. no network route
  to the configured host), `BzFlathubState` builds the Explore tab's category
  listing directly from apps already known from enabled Flatpak remotes
  (grouped by their AppStream category), instead of leaving the tab empty or
  erroring out. This is tracked via a new `has-connection-error` property.
  `BzFlathubState` is fed the full set of local entry groups through
  `bz_flathub_state_set_entries()`.
- **Configurable/hidden login** (`bz-login-page.c`, `bz-application.c`): the
  login page's requests (`create_flathub_request`, OAuth completion, the
  WebView navigation-policy host check) now target `flathub-login-url`. The
  `app.flathub-login` action's enabled state is recomputed from both
  authentication status and `hide-flathub-login`, which also hides the
  corresponding menu item (`hidden-when: "action-disabled"`).
- **Renameable tab** (`bz-window.c`/`bz-window.blp`): the Explore tab's
  `AdwViewStackPage` (`flathub_view_page`) has its `title` bound one-way to
  `flathub-tab-title` in `bz_window_new()`.

## Commit history

1. `Allow configuring or disabling the Flathub metadata source`
2. `Fall back to local remote data when Flathub metadata is unavailable`
3. `Allow customizing or hiding the Flathub login`
4. `Allow renaming the Explore/Flathub tab`
