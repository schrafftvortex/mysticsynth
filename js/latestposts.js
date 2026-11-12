// Show the newest blog posts on the homepage (page_listing comes from js/posts.js)
const latest_count = 2;
const latest_list = document.getElementById("latest_posts_list");

const latest_pages = Object.values(page_listing)
    .sort((a, b) => new Date(b.date) - new Date(a.date))
    .slice(0, latest_count);

for (let page of latest_pages) {
    let item = document.createElement("li");
    let link = document.createElement("a");
    link.href = page.link;
    link.textContent = page.title || "Untitled Post";
    item.append(link);
    latest_list.append(item);
}
