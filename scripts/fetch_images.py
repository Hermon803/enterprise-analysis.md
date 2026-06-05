#!/usr/bin/env python3
"""
企业分析图片自动抓取脚本 v1
用法：
  python3 scripts/fetch_images.py \
    --company "深圳格芯集成电路装备" \
    --domain "grandtec-ic.com" \
    --english "grandtec" \
    --founder "林宜龙" \
    --output ./image/
"""
import argparse, os, sys, re, time, json
from urllib.parse import urljoin, urlparse
import requests
from PIL import Image
from io import BytesIO

TIMEOUT = 15
MAX_RETRIES = 2
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]

session = requests.Session()
session.headers.update({"User-Agent": USER_AGENTS[0]})
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
session.mount("https://", adapter)
session.mount("http://", adapter)


def log(msg, tag="INFO"):
    print(f"  [{tag}] {msg}")


def validate_image(data):
    try:
        img = Image.open(BytesIO(data))
        img.verify()
        ext = img.format.lower() if img.format else "png"
        return True, ext
    except Exception:
        return False, None


def download(url, output_dir, name, must_be_image=True):
    try:
        r = session.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.content
        ct = r.headers.get("Content-Type", "")
        if "text/html" in ct or data[:6] == b"<html" or data[:5] == b"<!DOC":
            log(f"{url} → HTML响应，跳过", "SKIP")
            return None
        valid, ext = validate_image(data) if must_be_image else (True, None)
        if must_be_image and not valid:
            log(f"{url} → 非图片数据", "SKIP")
            return None
        if not ext:
            ext = "png"
        fname = f"{name}.{ext}"
        path = os.path.join(output_dir, fname)
        with open(path, "wb") as f:
            f.write(data)
        log(f"{fname} ({len(data)/1024:.0f}KB) ← {url}", "OK")
        return path
    except Exception as e:
        log(f"{url} → {e}", "FAIL")
        return None


# ===== Logo =====

def fetch_logo_simpleicons(english_name, output_dir):
    if not english_name:
        return None
    url = f"https://cdn.simpleicons.org/{english_name.lower()}"
    return download(url, output_dir, "logo")


def fetch_logo_from_html(domain, output_dir):
    for scheme in ["https", "http"]:
        url = f"{scheme}://{domain}"
        try:
            r = session.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            html = r.text
            for pat, attr in [
                (r'<link[^>]*rel=["\'](?:shortcut )?icon["\'][^>]*href=["\']([^"\']+)["\']', None),
                (r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', None),
                (r'<img[^>]*class=["\'][^"\']*logo[^"\']*["\'][^>]*src=["\']([^"\']+)["\']', None),
            ]:
                m = re.search(pat, html, re.I)
                if m:
                    result = download(urljoin(url, m.group(1)), output_dir, "logo")
                    if result:
                        return result
            for path in ["/logo.png", "/logo.svg", "/images/logo.png", "/static/logo.png"]:
                result = download(urljoin(url, path), output_dir, "logo")
                if result:
                    return result
        except Exception:
            continue
    return None


def fetch_logo(english_name, domain, output_dir):
    log("===== Logo =====", "STEP")
    result = fetch_logo_simpleicons(english_name, output_dir)
    if result:
        return result
    result = fetch_logo_from_html(domain, output_dir)
    if result:
        return result
    log("Logo: 全部尝试失败", "FAIL")
    return None


# ===== Founder =====

def fetch_founder_from_baidu(name, output_dir):
    encoded_name = requests.utils.quote(name)
    urls = [
        f"https://baike.baidu.com/item/{encoded_name}",
        f"https://baike.baidu.com/item/{encoded_name}?view=home",
    ]
    headers = {
        "User-Agent": USER_AGENTS[0],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    for search_url in urls:
        try:
            r = session.get(search_url, timeout=TIMEOUT, headers=headers)
            r.raise_for_status()
            html = r.text
            for pat in [
                r'<img[^>]*src=["\'](https?://bkimg\.cdn\.bcebos\.com[^"\']+)["\']',
                r'data-src=["\'](https?://bkimg\.cdn\.bcebos\.com[^"\']+)["\']',
            ]:
                m = re.search(pat, html, re.I)
                if m:
                    result = download(m.group(1), output_dir, "founder", must_be_image=False)
                    if result:
                        return result
        except Exception as e:
            log(f"百度百科 {search_url} → {e}", "FAIL")
            continue
    return None


def fetch_founder_from_website(domain, output_dir):
    for path in ["/about-us", "/about", "/aboutus", "/team", "/gywm", "/pages/1"]:
        url = f"https://{domain}{path}"
        try:
            r = session.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            html = r.text
            imgs = set()
            for pat in [r'<img[^>]*src=["\']([^"\']+)["\']', r'data-src=["\']([^"\']+)["\']']:
                for m in re.finditer(pat, html, re.I):
                    u = m.group(1).strip()
                    if u and u.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                        imgs.add(u)
            good = []
            for img_url in imgs:
                u = img_url.lower()
                if any(x in u for x in ["logo", "icon", "banner", "favicon", "btn", "arrow"]):
                    continue
                if any(x in u for x in ["people", "team", "member", "person", "avatar", "renwu", "photo", "tuan"]):
                    good.insert(0, img_url)
                elif not any(x in u for x in ["/product", "/pro/", "/cp/", "/chanpin"]):
                    good.append(img_url)
            for img_url in good:
                full_url = urljoin(url, img_url)
                result = download(full_url, output_dir, "founder")
                if result:
                    return result
        except Exception:
            continue
    return None


def fetch_founder(name, domain, output_dir):
    log("===== 创始人照片 =====", "STEP")
    result = fetch_founder_from_baidu(name, output_dir)
    if result:
        return result
    result = fetch_founder_from_website(domain, output_dir)
    if result:
        return result
    log("创始人照片: 全部尝试失败", "FAIL")
    return None


# ===== Product =====

def fetch_product_from_website(domain, output_dir, skip_urls=None):
    skip_urls = skip_urls or set()
    urls_to_try = [
        f"https://{domain}/product",
        f"https://{domain}/products",
        f"https://{domain}/pro",
        f"https://{domain}/cpzx",
        f"https://{domain}/chanpin",
    ]
    seen = set()
    for url in urls_to_try:
        try:
            r = session.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            html = r.text
            imgs = set()
            for pat in [
                r'<img[^>]*src=["\']([^"\']+)["\']',
                r'data-src=["\']([^"\']+)["\']',
                r'data-original=["\']([^"\']+)["\']',
            ]:
                for m in re.finditer(pat, html, re.I):
                    u = m.group(1).strip()
                    if u and u.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                        imgs.add(u)
            good = []
            for img_url in imgs:
                u = img_url.lower()
                if any(x in u for x in ["logo", "icon", "banner", "favicon"]):
                    continue
                full_url = urljoin(url, img_url)
                if full_url in skip_urls:
                    log(f"跳过已用图片: {os.path.basename(full_url)}", "SKIP")
                    continue
                good.append(full_url)
            good.sort(key=lambda u: not bool(re.search(r"(large|high|1920|big|full)", u, re.I)))
            for full_url in good:
                if full_url in seen:
                    continue
                seen.add(full_url)
                result = download(full_url, output_dir, "product", must_be_image=False)
                if result:
                    return result
            # 尝试产品详情子页面
            sub_links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\']', html, re.I)
            for link in sub_links:
                if any(x in link.lower() for x in ["/pro/", "/cp/", "/product/", "/chanpin/"]):
                    full_link = urljoin(url, link)
                    try:
                        r2 = session.get(full_link, timeout=TIMEOUT)
                        r2.raise_for_status()
                        html2 = r2.text
                        sub_imgs = set()
                        for m in re.finditer(r'<img[^>]*src=["\']([^"\']+\.(?:jpg|jpeg|png|webp))["\']', html2, re.I):
                            sub_imgs.add(m.group(1))
                        for si in sub_imgs:
                            if any(x in si.lower() for x in ["logo", "icon"]):
                                continue
                            full_si = urljoin(full_link, si)
                            if full_si not in seen and full_si not in skip_urls:
                                seen.add(full_si)
                                result = download(full_si, output_dir, "product", must_be_image=False)
                                if result:
                                    return result
                    except Exception:
                        continue
        except Exception:
            continue
    return None


def fetch_product(domain, output_dir, skip_urls=None):
    log("===== 产品图 =====", "STEP")
    result = fetch_product_from_website(domain, output_dir, skip_urls)
    if result:
        return result
    log("产品图: 全部尝试失败", "FAIL")
    return None


# ===== Main =====

def main():
    parser = argparse.ArgumentParser(description="企业分析图片自动抓取")
    parser.add_argument("--company", required=True, help="公司中文名")
    parser.add_argument("--domain", required=True, help="公司域名")
    parser.add_argument("--english", default="", help="英文名（simpleicons用）")
    parser.add_argument("--founder", default="", help="创始人/CEO姓名")
    parser.add_argument("--output", default="./image", help="输出目录")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    used_urls = set()

    results = {}
    logo_path = fetch_logo(args.english, args.domain, args.output)
    results["logo"] = logo_path
    if logo_path:
        used_urls.add(os.path.abspath(logo_path))

    founder_path = fetch_founder(args.founder, args.domain, args.output)
    results["founder"] = founder_path
    if founder_path:
        used_urls.add(os.path.abspath(founder_path))

    results["product"] = fetch_product(args.domain, args.output, skip_urls=used_urls)

    print("\n====== 抓取结果 ======")
    ok = 0
    for k, v in results.items():
        if v:
            ok += 1
            print(f"  ✅ {k}: {v}")
        else:
            print(f"  ❌ {k}: 失败")
    print(f"\n输出目录: {os.path.abspath(args.output)}")
    for f in sorted(os.listdir(args.output)):
        sz = os.path.getsize(os.path.join(args.output, f))
        print(f"  {f} ({sz/1024:.0f}KB)")
    print(f"\n结果: {ok}/3 成功")
    sys.exit(0 if ok == 3 else 1)


if __name__ == "__main__":
    main()
