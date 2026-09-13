<div align="center">
   <h2>Viral API</h2>
</div>

<p align="center">
  <img src="https://raw.githubusercontent.com/Viralway/viralAPI/main/imgs/viralway.png" alt="Viral API Logo" width="170"/>
</p>

<div align="center">
   <p><b>Viral API retrieves viral TikTok content for you automatically</b></p>
</div>

It fetches public TikTok data: Explore category videos, users, hashtags, sounds, comments, and more. 

Needs **Python 3.9+**. TikTok changes endpoints often, so if something breaks, open an issue 


## Docker

The `Dockerfile` installs this repo with `pip install .`. Rebuild after you change code (`COPY . .` is from build time).

```sh
docker build . -t viralapi:latest
docker run --rm --ipc=host viralapi:latest python3 -m examples.explore_category_example
```

Pass secrets at run time. Do not bake `ms_token` into the image.

```sh
export ms_token="paste_the_cookie_value_here"
docker run --rm --ipc=host -e ms_token="$ms_token" viralapi:latest python3 -m examples.trending_example
```

`.env` is gitignored. Inject it without copying it into the image:

```sh
docker run --rm --ipc=host --env-file .env viralapi:latest python3 -m examples.explore_category_example
```

Explore with a JSON file on the host (files inside the container vanish on `--rm` unless you mount a volume):

```sh
docker run --rm --ipc=host -v "$PWD:/out" \
  -e CATEGORY=technology -e COUNT=30 -e OUTPUT=/out/technology.json \
  viralapi:latest \
  python3 -m examples.explore_category_example
```

## Manual setup

```sh
pip install ViralApi
python -m playwright install
```

From this repo (includes local extras such as `proxyproviders`):

```sh
pip install .
python -m playwright install
```

## Get an `ms_token`

Examples read the env var `ms_token`. In the browser the cookie is named **`msToken`**.

You do not need to be logged in. Wait until tiktok.com finishes loading (scroll the feed once).
Examples live in [`examples/`](examples).

**Chrome / Edge / Brave:** open [tiktok.com](https://www.tiktok.com) → DevTools (`F12` or `Cmd+Option+I`) → **Application** → **Cookies** → `https://www.tiktok.com` → copy **`msToken`**.

**Safari:** Develop → Show Web Inspector → Storage → Cookies → `www.tiktok.com`.

**Firefox:** `F12` → Storage → Cookies → `https://www.tiktok.com`.

```sh
export ms_token="paste_the_msToken_value_here"
```

```py
import os
ms_token = os.environ.get("ms_token")
# await api.create_sessions(ms_tokens=[ms_token], ...)
```

- It expires. Copy a new one if requests start failing.
- For search, run a search on tiktok.com first, then copy the cookie.
- Keep it out of git. Use the env var or a local `.env` (already gitignored).
- You can pass `ms_tokens=None` and Playwright may create one. Explore often works better that way than with a stale cookie.

## Explore categories (recommended)

`api.trending.videos()` hits the For You feed (`recommend/item_list`). TikTok often returns an empty body for that. Use Explore instead:

`https://www.tiktok.com/api/explore/item_list/` with `categoryType`. IDs come from the live Explore chips (`data-e2e="explore-category-chip"`) and are listed in [`examples/explore_category_example.py`](examples/explore_category_example.py).

| ID | Category | ID | Category |
| ---: | --- | ---: | --- |
| 100 | Anime & Comics | 110 | Lipsync |
| 101 | Shows | 111 | Food |
| 102 | Beauty Care | 112 | Sports |
| 103 | Games | 113 | Animals |
| 104 | Comedy | 114 | Society |
| 105 | Daily Life | 115 | Cars |
| 106 | Family | 116 | Education |
| 107 | Relationship | 117 | Fitness & Health |
| 108 | Drama | 118 | Technology |
| 109 | Outfit | 119 | Singing & Dancing |

There is no Apps category. Closest: **Technology (`118`)**, then **Games (`103`)**.

```sh
CATEGORY=technology COUNT=30 python -m examples.explore_category_example
```

`HEADLESS=0` shows the browser. Leave `ms_token` unset unless the cookie is fresh. Language follows your IP, not the library `region` field.

### Save to JSON

Printing only goes to the terminal. Set `OUTPUT` to write a file (id, url, author, caption, plays, likes, comments, shares, hashtags, duration, sound). `SAVE_RAW=1` also stores each video’s full `as_dict`.

```sh
CATEGORY=technology COUNT=30 OUTPUT=technology.json python -m examples.explore_category_example
```

## Trending (For You)

```py
from ViralApi import ViralApi
import asyncio
import os

ms_token = os.environ.get("ms_token", None)

async def trending_videos():
    async with ViralApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3,
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
        )
        async for video in api.trending.videos(count=30):
            print(video)
            print(video.as_dict)

if __name__ == "__main__":
    asyncio.run(trending_videos())
```

```sh
python -m examples.trending_example
```

If that comes back empty, use Explore.

Full fields are on `video.as_dict` (plays, likes, caption, author, hashtags, …). TikTok changes that shape. Nothing is written to disk unless you set `OUTPUT` or write the file yourself.

## Problems

- **EmptyResponseException** — TikTok is treating the client as a bot. A residential proxy often helps. ProxyProviders: `create_sessions(proxy_provider=...)`. See [`examples/proxy_provider_example.py`](examples/proxy_provider_example.py).
- **Browser has no attribute** — run `python3 -m playwright install`. If it still fails, use the [playwright-python](https://github.com/microsoft/playwright-python) quickstart.
- **Got a Coroutine** — most methods are async; `await` them.

## Credits
- @ [Viralway](https://viralway.co)
- @ [Microsoft Playwright](https://playwright.dev)
