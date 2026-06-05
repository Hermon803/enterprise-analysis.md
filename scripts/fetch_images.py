#!/usr/bin/env python3
"""
企业分析图片自动抓取脚本 v1.1
用法：
  python3 scripts/fetch_images.py \
    --company "深圳格芯集成电路装备" \
    --domain "grandtec-ic.com" \
    --english "grandtec" \
    --founder "林宜龙" \
    --output ./image/
"""
import argparse, os, sys, re, time, json, subprocess
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
    os.makedirs(output_dir, exist_ok=True)
    try:
        r = session.get(url, timeout=TIMEOUT)
        r.raise_for_status()
        data = r.content
        ct = r.headers.get("Content-Type", "")
        if "text/html" in ct or data[:6] == b"<html" or data[:5] == b"<!DOC":
            log(f"HTML响应，跳过", "SKIP")
            return None
        valid, ext = validate_image(data) if must_be_image else (True, None)
        if must_be_image and not valid:
            log(f"非图片数据", "SKIP")
            return None
        if not ext:
            m = re.search(r"\.(jpg|jpeg|png|gif|webp|svg|ico)(?:\?|$)", url, re.I)
            ext = m.group(1).lower() if m else "png"
        fname = f"{name}.{ext}"
        path = os.path.join(output_dir, fname)
        with open(path, "wb") as f:
            f.write(data)
        log(f"{fname} ({len(data)//1024}KB)", "OK")
        return path
    except Exception as e:
        log(f"{e}", "FAIL")
        return None


def extract_images_from_html(html, base_url):
    imgs = set()
    for pat in [
        r'<img[^>]*src=["\']([^"\']+)["\']',
        r'data-src=["\']([^"\']+)["\']',
        r'data-original=["\']([^"\']+)["\']',
        r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
    ]:
        for m in re.finditer(pat, html, re.I):
            u = m.group(1).strip().split("?")[0]
            if u and re.search(r"\.(jpg|jpeg|png|gif|webp|svg|ico)(?:\?|$)", u, re.I):
                imgs.add(urljoin(base_url, u))
    return list(imgs)


def filter_out_logos(urls):
    return [u for u in urls if not any(
        x in urlparse(u).path.lower() for x in ["logo", "icon", "banner", "favicon"])]


# ===== Logo =====
def fetch_logo_simpleicons(english_name, output_dir):
    if not english_name:
        return None
    for name in [english_name.lower(), english_name.lower().replace("-", ""), english_name.lower().replace(" ", "")]:
        result = download(f"https://cdn.simpleicons.org/{name}", output_dir, "logo")
        if result:
            return result
    return None


def fetch_logo_from_html(domain, output_dir):
    for scheme in ["https", "http"]:
        base = f"{scheme}://{domain}"
        try:
            r = session.get(base, timeout=TIMEOUT)
            r.raise_for_status()
            html = r.text
            all_imgs = extract_images_from_html(html, base)
            for u in all_imgs:
                path = urlparse(u).path.lower()
                if any(x in path for x in ["favicon", "icon", "logo"]):
                    result = download(u, output_dir, "logo")
                    if result:
                        return result
            m = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, re.I)
            if m:
                result = download(m.group(1), output_dir, "logo")
                if result:
                    return result
            for path in ["/favicon.ico", "/logo.png", "/logo.svg", "/images/logo.png", "/static/logo.png"]:
                result = download(urljoin(base, path), output_dir, "logo")
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
    """百度百科 —— 使用curl（requests会被Baidu识别为爬虫返回403）"""
    encoded = requests.utils.quote(name)
    for search_url in [
        f"https://baike.baidu.com/item/{encoded}",
        f"https://baike.baidu.com/item/{encoded}?fromModule=lemma_search-box",
    ]:
        try:
            cmd = [
                "curl", "-sL", "--connect-timeout", "10",
                "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "-H", "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8",
                "-H", "Cookie: BAIDUID=0123456789ABCDEF:FG=1; BIDUPSID=0123456789ABCDEF",
                search_url,
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=15)
            if result.returncode != 0:
                continue
            html = result.stdout.decode("utf-8", errors="replace")
            if len(html) < 1000:
                continue
            for m in re.finditer(r'https?://bkimg\.cdn\.bcebos\.com[^"\\\' )]+', html):
                img_url = m.group(0).split("?")[0]
                result = download(img_url, output_dir, "founder", must_be_image=False)
                if result:
                    return result
        except Exception as e:
            log(f"百度百科 → {e}", "FAIL")
            continue
    return None


def fetch_founder_from_website(domain, output_dir):
    for path in ["/about-us", "/about", "/aboutus", "/team", "/gywm", "/pages/1", "/company", "/intro", "/about/company", "/about/leadership"]:
        url = f"https://{domain}{path}"
        try:
            r = session.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            html = r.text
            imgs = extract_images_from_html(html, url)
            people_kw = ["people", "team", "member", "person", "avatar", "renwu", "photo", "tuan", "leader", "ceo", "founder", "headshot", "portrait"]
            good_people = [u for u in imgs if any(k in urlparse(u).path.lower() for k in people_kw)]
            good_other = [u for u in imgs if not any(
                k in urlparse(u).path.lower() for k in ["logo", "icon", "banner", "favicon", "/product", "/pro/", "/cp/", "/chanpin"])]
            for u in good_people + good_other:
                result = download(u, output_dir, "founder")
                if result:
                    return result
        except Exception:
            continue
    return None


def fetch_founder_nvidia_strategy(output_dir):
    for url in [
        "https://images.nvidia.com/nv-story-tool/nv-story-09132023/assets/about-nvidia/history-ari.jpg",
        "https://images.nvidia.com/content/dam/en-zz/Solutions/about-nvidia/events/nvidia-gtc-2024/jensen-1200x675.jpg",
    ]:
        result = download(url, output_dir, "founder", must_be_image=False)
        if result:
            return result
    return None


def fetch_founder(name, domain, output_dir):
    log("===== 创始人照片 =====", "STEP")
    # ① 百度百科（最高优先级）
    result = fetch_founder_from_baidu(name, output_dir)
    if result:
        return result
    # ② 特定域名策略（大厂已知图片路径）
    if "nvidia" in domain.lower():
        result = fetch_founder_nvidia_strategy(output_dir)
        if result:
            return result
    # ③ 官网about/team页面
    result = fetch_founder_from_website(domain, output_dir)
    if result:
        return result
    log("创始人照片: 全部尝试失败", "FAIL")
    return None


# ===== Product =====
def fetch_product_from_website(domain, output_dir, skip_urls=None):
    skip_urls = skip_urls or set()
    seen = set()
    for url in [
        f"https://{domain}/product", f"https://{domain}/products",
        f"https://{domain}/pro", f"https://{domain}/cpzx", f"https://{domain}/chanpin",
    ]:
        try:
            r = session.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            imgs = extract_images_from_html(r.text, url)
            good = [u for u in filter_out_logos(imgs) if u not in seen and u not in skip_urls]
            seen.update(good)
            good.sort(key=lambda u: not bool(re.search(r"(large|high|1920|big|full|\d{3,})", urlparse(u).path, re.I)))
            for u in good:
                result = download(u, output_dir, "product", must_be_image=False)
                if result:
                    return result
            # 尝试产品详情子页面
            for link in re.findall(r'<a[^>]*href=["\']([^"\']+)["\']', r.text, re.I):
                if any(x in link.lower() for x in ["/pro/", "/cp/", "/product/", "/chanpin/"]):
                    try:
                        r2 = session.get(urljoin(url, link), timeout=TIMEOUT)
                        r2.raise_for_status()
                        for si in extract_images_from_html(r2.text, urljoin(url, link)):
                            if si not in seen and si not in skip_urls and not any(
                                k in urlparse(si).path.lower() for k in ["logo", "icon"]):
                                seen.add(si)
                                result = download(si, output_dir, "product", must_be_image=False)
                                if result:
                                    return result
                    except Exception:
                        continue
        except Exception:
            continue
    return None


def fetch_product_tech_media(company, domain, output_dir, skip_urls=None):
    skip_urls = skip_urls or set()
    strategies = []
    if "nvidia" in domain.lower():
        strategies.append("https://www.nvidia.com/en-us/geforce/news/")
    if "huawei" in domain.lower():
        strategies.append("https://consumer.huawei.com/cn/phones/")
    for url in strategies:
        try:
            r = session.get(url, timeout=TIMEOUT)
            r.raise_for_status()
            for u in filter_out_logos(extract_images_from_html(r.text, url)):
                if u not in skip_urls:
                    result = download(u, output_dir, "product", must_be_image=False)
                    if result:
                        return result
        except Exception:
            continue
    return None


def fetch_product(domain, output_dir, company="", skip_urls=None):
    log("===== 产品图 =====", "STEP")
    result = fetch_product_from_website(domain, output_dir, skip_urls)
    if result:
        return result
    result = fetch_product_tech_media(company, domain, output_dir, skip_urls)
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

    results["product"] = fetch_product(args.domain, args.output, args.company, skip_urls=used_urls)

    print("\n====== 抓取结果 ======")
    ok = sum(1 for v in results.values() if v)
    for k, v in results.items():
        print(f"  {'✅' if v else '❌'} {k}: {v if v else '失败'}")
    print(f"\n输出目录: {os.path.abspath(args.output)}")
    for f in sorted(os.listdir(args.output)):
        sz = os.path.getsize(os.path.join(args.output, f))
        print(f"  {f} ({sz//1024}KB)")
    print(f"\n结果: {ok}/3 成功")
    sys.exit(0 if ok == 3 else 1)


if __name__ == "__main__":
    main()
