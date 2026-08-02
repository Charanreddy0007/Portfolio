// =========================
// Load Article
// =========================

const content = document.getElementById("content");
const params = new URLSearchParams(window.location.search);
const article = params.get("article");

if (!article) {

    content.innerHTML = "<h2>Article not found.</h2>";

} else {

    const file = article.endsWith(".html")
        ? article
        : `${article}.md`;

    fetch(file)
        .then(response => {

            if (!response.ok) {
                throw new Error("File not found");
            }

            return response.text();

        })
        .then(data => {

            if (article.endsWith(".html")) {
                content.innerHTML = data;
            } else {
                content.innerHTML = marked.parse(data);
            }

        })
        .catch(err => {

            console.error(err);

            content.innerHTML = "<h2>Unable to load article.</h2>";

        });

}


// =========================
// Theme
// =========================
const root = document.documentElement;
const toggle = document.getElementById("themeToggle");

let theme = localStorage.getItem("theme");

if (!theme) {
    theme = window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
}

setTheme(theme);

toggle.addEventListener("click", () => {

    theme = theme === "dark" ? "light" : "dark";

    localStorage.setItem("theme", theme);

    setTheme(theme);

});

function setTheme(theme) {

    root.setAttribute("data-theme", theme);
    updateIcon(theme);

}

function updateIcon(theme){

    const icon=document.getElementById("themeIcon");

    if(theme==="dark"){

        icon.innerHTML = `<path d="M12 3a6 6 0 0 0 9 9A9 9 0 1 1 12 3z"/>`;

    }else{

        icon.innerHTML = `
        <circle cx="12" cy="12" r="4"/>
        <path d="
        M12 2v2
        M12 20v2
        M4.93 4.93l1.41 1.41
        M17.66 17.66l1.41 1.41
        M2 12h2
        M20 12h2
        M4.93 19.07l1.41-1.41
        M17.66 6.34l1.41-1.41"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"/>
        `;
    }

}