import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlsplit


ROOT = Path(__file__).resolve().parent


NEWS_ITEMS = [
    {
        "id": "local-news-001",
        "title": "关于做好2026年普通高校招生录取工作的提示",
        "displayOn": "20260706100000",
        "url": "https://www.chsi.com.cn/",
    },
    {
        "id": "local-news-002",
        "title": "学籍学历信息查询与在线验证报告使用说明",
        "displayOn": "20260705180000",
        "url": "https://www.chsi.com.cn/xlcx/",
    },
    {
        "id": "local-news-003",
        "title": "高校学生学籍信息核验常见问题",
        "displayOn": "20260704120000",
        "url": "https://www.chsi.com.cn/help/",
    },
    {
        "id": "local-news-004",
        "title": "毕业生学历电子注册图像校对相关说明",
        "displayOn": "20260703100000",
        "url": "https://www.chsi.com.cn/xlcx/",
    },
    {
        "id": "local-news-005",
        "title": "在线验证报告申请、查看和延期操作指南",
        "displayOn": "20260702160000",
        "url": "https://www.chsi.com.cn/xlcx/bgys.jsp",
    },
    {
        "id": "local-news-006",
        "title": "学信档案账号与实名信息维护提醒",
        "displayOn": "20260701110000",
        "url": "https://account.chsi.com.cn/",
    },
]


class HashRouteHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        raw_path = urlsplit(path).path
        if raw_path == "/":
            return str(ROOT / "index.html")
        return super().translate_path(path)

    def serve_news(self):
        query = parse_qs(urlsplit(self.path).query)
        size = int(query.get("size", ["10"])[0] or 10)
        on = query.get("on", ["99999999999999"])[0]

        items = [item for item in NEWS_ITEMS if item["displayOn"] < on]
        payload = json.dumps(items[:size], ensure_ascii=False).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        raw_path = urlsplit(self.path).path
        target = ROOT / raw_path.lstrip("/")

        if raw_path == "/api/news":
            self.serve_news()
            return

        if raw_path != "/" and not target.exists() and "." not in raw_path.rsplit("/", 1)[-1]:
            hash_path = quote(raw_path, safe="/")
            self.send_response(302)
            self.send_header("Location", f"/#{hash_path}")
            self.end_headers()
            return

        return super().do_GET()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Serve the local hash-route SPA mirror.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8081, type=int)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), HashRouteHandler)
    print(f"Serving {ROOT} at http://{args.host}:{args.port}/#/ ")
    server.serve_forever()
