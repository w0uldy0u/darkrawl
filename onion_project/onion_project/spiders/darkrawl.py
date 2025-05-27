import scrapy
import os
import hashlib
import re
import base64
from urllib.parse import urlparse, urljoin

MAX_FILENAME_LEN = 240 
blacklist_keywords = [
    "pedophile", "child porn", "preteen", "lolita", "pthc",
    "underage", "abused kids", "babyj", "minor sex", "young girls", "young boys", "young nudes",
    "pedo", "pedophilia", "child abuse", "preeteen", "preeteens", "10yo", "11yo", "12yo", "13yo", "14yo",
    "15yo", "16yo", "17yo", "9yo", "8yo", "7yo", "6yo", "5yo", "4yo", "3yo",
    "2yo", "1yo", "0yo", "infant", "toddler", "kid porn"
]
blocked_domains = [
    "facebookwkhpilnemxj7asaniu7vnjjbiltxjqhye3mhbshg7kx5tfyd.onion",
]

headers = {
}

def contains_blacklisted(text):
    text = text.lower()
    return any(keyword in text for keyword in blacklist_keywords)

def url_to_filename(url, is_media=False, index=None, ext=".html"):
    parsed = urlparse(url)
    host = parsed.hostname or "unknown"
    path = parsed.path.strip("/")
    path = re.sub(r'\W+', "_", path)
    base_name = f"{index:03d}_{host}__{path}" if is_media else f"{host}__{path or 'index'}"

    filename = f"{base_name}{ext}"
    if len(filename.encode('utf-8')) > MAX_FILENAME_LEN:
        h = hashlib.sha256(url.encode()).hexdigest()[:16]
        filename = f"{index:03d}_{host}__{h}{ext}" if is_media else f"{host}__{h}{ext}"
        with open("media_log.txt", "a", encoding="utf-8") as log:
            log.write(f"{filename} -> {url}\n")

    subdir = os.path.join("media" if is_media else "saved_pages", host)
    os.makedirs(subdir, exist_ok=True)
    return os.path.join(subdir, filename)


def should_crawl(url):
    try:
        hostname = urlparse(url).hostname
        return (
            hostname.endswith(".onion") and
            hostname not in blocked_domains
        )
    except Exception:
        return False


class Darkrawl(scrapy.Spider):
    name = "darkrawl"
    start_urls = [
        "http://tortimeswqlzti2aqbjoieisne4ubyuoeiiugel2layyudcfrwln76qd.onion",
        "http://torlinksge6enmcyyuxjpjkoouw4oorgdgeo7ftnq3zodj7g2zxi3kyd.onion",
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.1,
        'ROBOTSTXT_OBEY': False,
        'DEPTH_LIMIT': 0,
        'DEFAULT_REQUEST_HEADERS': {
            "Cookie": ""
        },
        'LOG_LEVEL': 'DEBUG',
        
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                meta={'proxy': 'http://127.0.0.1:8118', 'download_timeout': 60},
                headers=headers,
                callback=self.parse,
                errback=self.handle_error
            )

    def handle_error(self, failure):
    # HTTP 응답인 경우만 처리
        if failure.check(scrapy.spidermiddlewares.httperror.HttpError):
            response = failure.value.response
            status = response.status
            url = response.url

            if status in [401, 403]:
                self.logger.warning(f"⛔ {status} error at: {url}")
                with open("unauthorized_urls.txt", "a", encoding="utf-8") as f:
                    f.write(f"{status} {url}\n")

    def parse(self, response):
        os.makedirs("saved_pages", exist_ok=True)
        os.makedirs("media", exist_ok=True)

        # Content-Type이 텍스트일 때만 필터링
        content_type = response.headers.get("Content-Type", b"").decode("utf-8")
        is_text = "text" in content_type or "html" in content_type

        if is_text:
            if contains_blacklisted(response.url) or \
               contains_blacklisted(response.xpath("//title/text()").get() or "") or \
               contains_blacklisted(response.text):
                self.logger.warning(f"⛔ Skipped blacklisted page: {response.url}")
                with open("blacklist_urls.txt", "a", encoding="utf-8") as f:
                    f.write(response.url + "\n")
                # return 

        # 저장은 항상 진행
        # HTML 저장
        html_filename = url_to_filename(response.url)
        with open(html_filename, "wb") as f:
            f.write(response.body)
        self.logger.info(f"📄 Saved page: {html_filename}")

        with open("success_urls.txt", "a", encoding="utf-8") as f:
            f.write(response.url + "\n")

        # 바이너리 응답인 경우 media 추출 생략
        if is_text:
            media_urls = [
                urljoin(response.url, u)
                for u in response.css("img::attr(src), audio::attr(src), video::attr(src)").getall()
                if not re.match(r"^data:image/svg\+xml", u, re.IGNORECASE)
                and not u.lower().endswith(".svg")
                and not any(kw in u.lower() for kw in ["favicon", "icon", "logo", "sprite", "apple-touch", "android-icon", "pixel"])
                and not contains_blacklisted(u)
            ]

            for i, media_url in enumerate(media_urls):
                ext = self.get_extension(media_url)
                media_filename = url_to_filename(media_url, is_media=True, index=i, ext=ext)

                if media_url.startswith("data:"):
                    yield {
                        "media_base64": media_url,
                        "save_path": media_filename
                    }
                else:
                    yield scrapy.Request(
                        url=media_url,
                        meta={
                            'proxy': 'http://127.0.0.1:8118',
                            'save_path': media_filename,
                            'download_timeout': 60,
                        },
                        callback=self.save_media,
                        headers=headers,
                        dont_filter=False
                    )

        links = response.css("a::attr(href)").getall() if is_text else []
        for link in links:
            full_url = urljoin(response.url, link)
            if should_crawl(full_url) and not contains_blacklisted(full_url):
                yield scrapy.Request(
                    url=full_url,
                    meta={'proxy': 'http://127.0.0.1:8118', 'download_timeout': 60},
                    headers=headers,
                    callback=self.parse
                )
    def get_extension(self, url):
        if url.startswith("data:"):
            match = re.match(r"data:(image|audio|video)/(\w+);base64,", url)
            if match:
                return f".{match.group(2)}"
            return ".bin"
        else:
            path = urlparse(url).path
            return os.path.splitext(path)[1] or ".bin"

    def process_item(self, item, spider):
        if "media_base64" in item:
            url = item["media_base64"]
            save_path = item["save_path"]
            try:
                base64_data = url.split(",", 1)[1]
                with open(save_path, "wb") as f:
                    f.write(base64.b64decode(base64_data))
                spider.logger.info(f"🖼️  Saved base64 media: {save_path}")
            except Exception as e:
                spider.logger.error(f"❌ Failed to save base64: {e}")
        return item

    def save_media(self, response):
        save_path = response.meta["save_path"]
        with open(save_path, "wb") as f:
            f.write(response.body)
        self.logger.info(f"🖼️  Saved media: {save_path}")