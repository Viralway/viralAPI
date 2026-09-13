from ViralApi import ViralApi
import asyncio
import json
import os

ms_token = os.environ.get("ms_token", None)

CATEGORIES = {
    "anime_comics": 100,
    "shows": 101,
    "beauty_care": 102,
    "games": 103,
    "comedy": 104,
    "daily_life": 105,
    "family": 106,
    "relationship": 107,
    "drama": 108,
    "outfit": 109,
    "lipsync": 110,
    "food": 111,
    "sports": 112,
    "animals": 113,
    "society": 114,
    "cars": 115,
    "education": 116,
    "fitness_health": 117,
    "technology": 118,
    "singing_dancing": 119,
}


async def explore_videos(api, category, count=30, max_requests=20):
    category_type = CATEGORIES[category]
    seen = set()
    requests_made = 0

    while len(seen) < count and requests_made < max_requests:
        resp = await api.make_request(
            url="https://www.tiktok.com/api/explore/item_list/",
            params={"categoryType": category_type, "count": 30, "cursor": 0},
        )
        requests_made += 1

        items = resp.get("itemList") or []
        if not items:
            return

        for item in items:
            if item["id"] in seen:
                continue
            seen.add(item["id"])
            yield api.video(data=item)
            if len(seen) >= count:
                return

        await asyncio.sleep(1)


def summarize(video, category):
    data = video.as_dict
    stats = video.stats or {}
    author = data.get("author", {}) or {}
    username = author.get("uniqueId", "unknown")
    return {
        "id": video.id,
        "category": category,
        "url": f"https://www.tiktok.com/@{username}/video/{video.id}",
        "author": username,
        "author_nickname": author.get("nickname"),
        "desc": (data.get("desc") or "").strip(),
        "create_time": video.create_time.isoformat() if video.create_time else None,
        "plays": stats.get("playCount"),
        "likes": stats.get("diggCount"),
        "comments": stats.get("commentCount"),
        "shares": stats.get("shareCount"),
        "hashtags": [c.get("title") for c in data.get("challenges", [])],
        "duration": (data.get("video") or {}).get("duration"),
        "music": (data.get("music") or {}).get("title"),
    }


async def main():
    category = os.environ.get("CATEGORY", "technology")
    count = int(os.environ.get("COUNT", "30"))
    headless = os.environ.get("HEADLESS", "1") != "0"
    out_path = os.environ.get("OUTPUT")
    save_raw = os.environ.get("SAVE_RAW", "0") == "1"

    rows = []

    async with ViralApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token] if ms_token else None,
            num_sessions=1,
            sleep_after=3,
            headless=headless,
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
        )

        async for video in explore_videos(api, category, count=count):
            row = summarize(video, category)
            if save_raw:
                row["raw"] = video.as_dict
            rows.append(row)

            print(row["url"])
            print(f"  plays={row['plays']} likes={row['likes']}")
            print(f"  {row['desc'][:100]}")
            if row["hashtags"]:
                print(f"  tags={row['hashtags'][:8]}")
            print()

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(rows)} videos to {os.path.abspath(out_path)}")


if __name__ == "__main__":
    asyncio.run(main())
