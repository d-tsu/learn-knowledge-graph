/* Substring search supports Japanese without requiring spaces or an external service. */
(() => {
    const base = new URL("../", document.currentScript.src);
    const toggle = document.getElementById("mdbook-search-toggle");
    const wrapper = document.getElementById("mdbook-search-wrapper");
    const input = document.getElementById("mdbook-searchbar");
    const form = document.getElementById("mdbook-searchbar-outer");
    const results = document.getElementById("mdbook-searchresults");
    const outer = document.getElementById("mdbook-searchresults-outer");
    const header = document.getElementById("mdbook-searchresults-header");
    if (!toggle || !input) return;

    toggle.title = "本文を検索（/）";
    toggle.setAttribute("aria-label", "本文を検索");
    input.placeholder = "本文を検索（日本語の部分一致に対応）";
    input.setAttribute("aria-describedby", header.id);
    header.setAttribute("role", "status");
    header.setAttribute("aria-live", "polite");
    window.search = {hasFocus: () => document.activeElement === input};
    const normalize = value => value.normalize("NFKC").toLocaleLowerCase("ja");
    let index;
    let timer;
    let revision = 0;

    function show(visible, focus = false) {
        wrapper.classList.toggle("hidden", !visible);
        toggle.setAttribute("aria-expanded", String(visible));
        if (focus) input.focus();
    }

    async function search() {
        const current = ++revision;
        const query = input.value.trim();
        const url = new URL(location.href);
        if (query) url.searchParams.set("search", query);
        else url.searchParams.delete("search");
        history.replaceState(null, "", url);
        results.replaceChildren();
        outer.classList.toggle("hidden", !query);
        if (!query) { header.textContent = ""; return; }
        header.textContent = "検索中…";
        try {
            index ||= fetch(new URL("reader-search-index.json", base)).then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            }).then(items => items.map(item => ({...item,
                key: normalize(item.title + " " + item.body), titleKey: normalize(item.title)})));
            const items = await index;
            if (current !== revision) return;
            const terms = normalize(query).split(/\s+/);
            const matches = items.filter(item => terms.every(term => item.key.includes(term)))
                .map(item => ({...item, score: terms.reduce((score, term) =>
                    score + (item.titleKey.includes(term) ? 10 : 0), 0)}))
                .sort((a, b) => b.score - a.score);
            header.textContent = matches.length ? `「${query}」：${matches.length}件${matches.length > 30 ? "（先頭30件を表示）" : ""}` : `「${query}」は見つかりませんでした`;
            for (const item of matches.slice(0, 30)) {
                const li = document.createElement("li");
                const link = document.createElement("a");
                link.href = new URL(item.url, base).href;
                link.textContent = item.title;
                const teaser = document.createElement("p");
                const position = normalize(item.body).indexOf(terms[0]);
                const start = Math.max(0, position - 35);
                teaser.textContent = (start ? "…" : "") + item.body.slice(start, start + 150) + "…";
                li.append(link, teaser);
                results.append(li);
            }
        } catch (error) {
            index = undefined;
            if (current === revision) header.textContent = "検索データを読み込めませんでした。もう一度入力してください。";
            console.error(error);
        }
    }

    toggle.addEventListener("click", () => show(wrapper.classList.contains("hidden"), true));
    form.addEventListener("submit", event => { event.preventDefault(); search(); });
    input.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(search, 100); });
    document.addEventListener("keydown", event => {
        const editing = event.target.closest("input, textarea, select, [contenteditable='true']");
        if (!editing && !event.ctrlKey && !event.metaKey && !event.altKey && (event.key === "/" || event.key === "s")) {
            event.preventDefault(); show(true, true);
        }
        if (event.key === "Escape" && !wrapper.classList.contains("hidden")) {
            show(false); toggle.focus();
        }
    });
    const initial = new URL(location.href).searchParams.get("search");
    if (initial) { input.value = initial; show(true); search(); }
})();
