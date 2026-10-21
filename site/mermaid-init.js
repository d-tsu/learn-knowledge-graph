/* Mermaid is supplied locally by the pinned mdbook-mermaid release. */
(() => {
    const darkThemes = ["ayu", "navy", "coal"];
    const isDark = () => darkThemes.some(theme => document.documentElement.classList.contains(theme));
    const original = new Map();
    for (const element of document.querySelectorAll(".mermaid")) {
        original.set(element, element.textContent);
        element.setAttribute("role", "img");
        element.setAttribute("aria-label", "本文の関係図");
    }

    let lastDark;
    let pending = Promise.resolve();
    function render() {
        pending = pending.then(async () => {
            const dark = isDark();
            if (dark === lastDark) return;
            lastDark = dark;
            for (const [element, source] of original) {
                element.removeAttribute("data-processed");
                element.textContent = source;
            }
            mermaid.initialize({
                startOnLoad: false,
                securityLevel: "strict",
                theme: dark ? "dark" : "default",
                fontFamily: '"Noto Sans JP", "Yu Gothic", Meiryo, sans-serif',
            });
            await mermaid.run({nodes: [...original.keys()]});
            for (const element of original.keys()) {
                const svg = element.querySelector("svg");
                if (svg) svg.style.minWidth = svg.viewBox.baseVal.width + "px";
            }
        }).catch(error => {
            lastDark = undefined;
            console.error("図を描画できませんでした", error);
        });
    }
    new MutationObserver(render).observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["class"],
    });
    render();
})();
