console.log("Welcome to Mystic Synth!");
// page_listing comes from js/posts.js, which must be loaded first

let included_pages = [];
let page_sort = "0"; // "0" means new to old, "1" means old to new
const all_pages = Object.keys(page_listing);

// Create the blog feed
const createBlogConstruct = function (sortVar = "") {
    let construct_element = document.getElementById("blog_construct_div");

    // Interpret sorting variable
    switch (sortVar) {
        case "all":
            included_pages = all_pages;
            break;
        case "best":
            included_pages = all_pages.filter(page => page_listing[page].category === "best");
            break;
        case "album_recs":
            included_pages = all_pages.filter(page => page_listing[page].category === "album_recs");
            break;
        case "life":
            included_pages = all_pages.filter(page => page_listing[page].category === "life");
            break;
        case "philosophy":
            included_pages = all_pages.filter(page => page_listing[page].category === "philosophy");
            break;
        case "gaming":
            included_pages = all_pages.filter(page => page_listing[page].category === "gaming");
            break;
        case "movies":
            included_pages = all_pages.filter(page => page_listing[page].category === "movies");
            break;
        case "newtoold":
            page_sort = "0";
            break;
        case "oldtonew":
            page_sort = "1";
            break;
    }

     // Create new array containing content of included_pages, but with a new reference
    let sent_pages = [...included_pages];

    // Sort by actual date
    sent_pages.sort((a, b) => {
        const dateA = new Date(page_listing[a].date);
        const dateB = new Date(page_listing[b].date);
        return page_sort === "1" ? dateA - dateB : dateB - dateA;
    });

    // 🔍 Add this line right here:
    console.log("Included pages:", sent_pages);



    // Create pages from the sent_pages array
    for (let i in sent_pages) {
    let page_num = sent_pages[i];
    let page = page_listing[page_num];
    createBlogFeedEntry(page, page_num, construct_element);
}

};

// Create a blog feed entry
const createBlogFeedEntry = function (page, page_num, construct_element) {
    let entry_div = document.createElement("div");
    entry_div.classList.add("blog_feed_entry");

    // Create the clickable entry link
    let link_div = document.createElement("a");
    link_div.classList.add("blog_feed_entry_link");
    link_div.href = page.link;
    link_div.textContent = page.title || "Untitled Post";

    let content_div = document.createElement("div");
    content_div.classList.add("blog_feed_entry_content");

    // Create the excerpt
    if (page.excerpt) {
        let excerpt_div = document.createElement("p");
        excerpt_div.classList.add("post-excerpt");
        excerpt_div.textContent = page.excerpt;
        content_div.append(excerpt_div);
    }

    // Create the date and time
    let date_div = document.createElement("div");
    date_div.classList.add("blog_feed_entry_end_cont");
    date_div.textContent = formatDate(page.date);

    content_div.append(date_div);
    entry_div.append(link_div);
    entry_div.append(content_div);
    construct_element.append(entry_div);
};

// Function to format date and time in 12-hour AM/PM format
const formatDate = function(dateString) {
    const date = new Date(dateString);
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
    };
    return date.toLocaleString('en-US', options);
};

// Function to rebuild the blog feed when a radio button is clicked
const inputEnter = function (radioVal = "") {
    let construct_element = document.getElementById("blog_construct_div");
    construct_element.innerHTML = ''; // Clear current feed
    createBlogConstruct(radioVal);
};

// Set up radio buttons
const radios_group_type = document.forms["radio_group_type"].elements["construct_group"];
for (let radio of radios_group_type) {
    radio.onclick = function () {
        inputEnter(this.value);
    }
};

const radios_group_sort = document.forms["radio_group_sort"].elements["construct_group"];
for (let radio of radios_group_sort) {
    radio.onclick = function () {
        inputEnter(this.value);
    }
};

// Initialize blog feed with all posts
createBlogConstruct("all");


