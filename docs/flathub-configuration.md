# Flathub metadata, login, and Explore tab configuration

Bazaar normally communicates with Flathub for supplemental metadata
(curated picks, categories, stats, favorites) and an OAuth login flow
(for favorites and user-specific data). Both features, along with Flathub
integration and Explore tab branding, can be configured or disabled via
the main configuration YAML file (e.g. `/etc/bazaar/bazaar.yaml`, baked
in via the meson option `-Dhardcoded_main_config_path=...`).

## Configuration options

All options are specified in the top-level mapping of the main configuration
YAML file:

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `metadata-api-url` | string | `https://flathub.org/api/v2` | Base URL for the Flathub metadata API. Empty string resets to default. |
| `disable-metadata-fetching` | bool | `false` | When `true`, Bazaar never makes network requests to the metadata API. Explore tab categories are populated from enabled Flatpak remotes directly. |
| `flathub-login-url` | string | `https://flathub.org` | Base URL for the OAuth login flow, userinfo, and authenticated requests. |
| `hide-flathub-login` | bool | `false` | Hides the "Login with Flathub" menu action and login prompts, and blocks all authenticated Flathub requests (favorites, user profile, etc.). |
| `flathub-tab-title` | string | `Explore` | Custom label for the Explore / Flathub tab in the main navigation. |
| `disable-flathub` | bool | `false` | Suppresses the "Set Up Flathub?" first-launch prompt, treats the Flathub remote as absent, and automatically hides the Flathub login action. |

### Example configuration (`/etc/bazaar/bazaar.yaml`)

```yaml
# Disable external Flathub metadata requests and use local remote AppStream data
disable-metadata-fetching: true

# Hide Flathub login and account actions
hide-flathub-login: true

# Suppress Flathub setup prompts
disable-flathub: true

# Customize the Explore tab label
flathub-tab-title: "Apps"
```

## Flathub API endpoints used by Bazaar

### Metadata API (base configurable via `metadata-api-url`, default `https://flathub.org/api/v2`)

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

### Login API (base configurable via `flathub-login-url`, default `https://flathub.org`)

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

## Behavior details

- **Metadata Source & Disabling** (`global-net.c`): `bz_query_flathub_v2_json*`
  functions build request URLs from `metadata-api-url` and immediately reject
  requests with `G_IO_ERROR_NOT_SUPPORTED` when `disable-metadata-fetching` is enabled.
- **Local Remote Fallback** (`bz-flathub-state.c`, `bz-flathub-page.c`): When metadata
  fetching is disabled or unreachable, `BzFlathubState` categorizes locally known
  applications from enabled Flatpak remotes into standard XDG categories using their
  AppStream category flags. The Explore page displays this content rather than falling
  back to empty or offline placeholders.
- **Configurable / Hidden Login** (`bz-login-page.c`, `bz-application.c`): The login
  page targets `flathub-login-url` and validates OAuth redirects against the configured
  host. The `app.flathub-login` action is disabled when `hide-flathub-login` or
  `disable-flathub` is set, hiding the menu item. `global-net.c` also rejects all
  authenticated requests to prevent transmitting tokens.
- **Flathub Remote Disabling** (`bz-application.c`): When `disable-flathub` is `true`,
  the startup check suppresses the "Set Up Flathub?" dialog.
- **Tab Title Customization** (`bz-window.c`, `bz-window.blp`): The Explore tab page
  title is set from `flathub-tab-title` at window creation time.
- **Cache Lifecycle on Refresh** (`refresh-worker.c`, `bz-application.c`): During a
  remote refresh, stale serialized entries on disk (`entry-cache`) and in-memory group
  collections are cleared before repopulating from currently configured Flatpak remotes,
  preventing removed remotes from lingering in search results or caches.
