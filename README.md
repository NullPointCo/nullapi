# NullAPI — Free Developer Utility APIs

⚡ Fast, free, dependency-free APIs for developers. No API key required for
basic usage. Built with the Python standard library only (zero dependencies),
so it deploys anywhere in seconds.

Part of the [NullPointerCo](https://github.com/NullPointCo) product line —
*Earn. Build. Compute.*

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info + endpoint map |
| `/qr?text=hello` | GET | Generate a QR code as SVG |
| `/shorten?url=https://example.com` | GET | Create a short URL |
| `/s/{id}` | GET | 302 redirect to the original URL |
| `/api/v1/status` | GET | Service statistics (URLs shortened, total clicks) |

All responses send `Access-Control-Allow-Origin: *` for easy browser use.

### Example

```bash
# QR code (returns SVG)
curl "https://YOUR_HOST/qr?text=https://github.com/NullPointCo"

# Shorten a URL
curl "https://YOUR_HOST/shorten?url=https://github.com/NullPointCo"
# => {"short_id":"a1b2c3d4","short_url":".../s/a1b2c3d4","original_url":"..."}

# Redirect
curl -L "https://YOUR_HOST/s/a1b2c3d4"
```

## Run locally

```bash
python app.py                 # listens on :8080 (set PORT env to override)
# or
pip install -r requirements.txt && python app.py
```

## Run with Docker

```bash
docker build -t nullapi .
docker run -p 8080:8080 nullapi
```

## Deploy to Render (Free tier)

1. Fork / push this repo to GitHub.
2. In Render, **New → Web Service**, connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `python app.py`
5. Add environment variable `PORT=8080` (Render injects this automatically).

The same image works on Fly.io, Railway, Koyeb, and any container platform.

## List on RapidAPI (monetization)

Wrap the endpoints behind an API key and publish on RapidAPI at
**$0.001–$0.01 / call**. The current handlers already return clean JSON and
SVG, so adding a thin auth layer (e.g. `?api_key=` or a header check) is the
only remaining step before listing.

> Note: the in-memory `url_store` resets on restart. Swap it for SQLite
> (or Redis) before production use to persist short links.

## License

MIT — do what you want, just keep the notice.
