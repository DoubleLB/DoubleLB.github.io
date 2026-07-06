# xuexin.pages.dev 本地源码镜像

来源入口：

`https://xuexin.pages.dev/#/`

已下载内容：

- `index.html`
- `favicon.ico`
- `assets/index-C-sc3Fg2.js`
- `assets/index-BiCCTU3I.css`
- `xjlb.html`，用于 `/#/xjcx` 页面内嵌 iframe
- `xjxx.html`，用于从 `xjlb.html` 点击学籍/学历条目后的详情页

本地启动：

```powershell
cd "E:\其他\学信网\xuexin-pages-source"
python serve-spa.py --port 8081
```

访问：

`http://127.0.0.1:8081/#/`

路由列表见 `ROUTES.md`。

说明：这个站点是 hash 路由单页应用，`/#/account`、`/#/xjcx` 等页面都由同一份 JS bundle 渲染；外部跳转页面没有下载。
