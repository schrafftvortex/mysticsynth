console.log("Welcome to Mystic Synth!");
// Data structure for blog posts with time included
const page_listing = {
    "001": { 
        title: "Winter Solstice Web Development", 
        link: "blog/blog001.html", 
        displaynum: "001", 
        date: "2024-12-21 10:56 AM", 
        excerpt: "First blog post! I talk about building the website and 2024 accomplishments.",
        var: "1", 
        category: "life" 
    },
    "002": { 
        title: "Album Rec: Blue Mena's Multi Adolescence", 
        link: "blog/blog002.html", 
        displaynum: "002", 
        date: "2024-12-21 01:30 PM", 
        excerpt: "My recommendation of this dreampop gem!",
        var: "2", 
        category: "album_recs" 
    },
    "003": { 
        title: "Basics of Clay Pot Metaphysics", 
        link: "blog/blog003.html", 
        displaynum: "003", 
        date: "2024-12-21 02:18 PM", 
        excerpt: "I talk about how an ancient invention can help you",
        var: "1", 
        category: "philosophy" 
    },
    "post4": { 
        title: "Gaming in 2024", 
        link: "gaming-article.html", 
        displaynum: "004", 
        date: "2024-12-04 03:45 PM", 
        var: "3", 
        category: "gaming" 
    },
    "post5": { 
        title: "The Best Movies of the Year", 
        link: "movies-review.html", 
        displaynum: "005", 
        date: "2024-12-05 09:00 AM", 
        var: "2", 
        category: "movies" 
    },
    "post6": { 
        title: "Mystic Thoughts on Philosophy", 
        link: "mystic-philosophy.html", 
        displaynum: "006", 
        date: "2024-12-06 01:30 PM", 
        var: "1", 
        category: "philosophy" 
    }
};

let included_pages = [];
let page_sort = "0"; // "0" means new to old, "1" means old to new
let num_pages = 0;
const all_pages = Object.keys(page_listing);

// Create the blog feed
const createBlogConstruct = function (sortVar = "", numVar = 0) {
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

    // Handle number of pages to display
    if (numVar !== 0) {
        num_pages = numVar;
    }

    // Create new array containing content of included_pages, but with a new reference
    let sent_pages = [...included_pages];

    // Apply sorting
    if (page_sort === "1") {
        sent_pages.reverse();
    }

    // Create pages from the sent_pages array, up to the num_pages limit
    let pages_made = 0;
    for (let i in sent_pages) {
        pages_made++;
        if (pages_made > num_pages) {
            break;
        }
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

    // Create the title
    let content_div = document.createElement("div");
    content_div.classList.add("blog_feed_entry_content");

    // Create the date and time
    let date_div = document.createElement("div");
    date_div.classList.add("blog_feed_entry_end_cont");
    date_div.textContent = formatDate(page.date || "Unknown Date");

    // Format and display the time in 12-hour AM/PM format
    const formattedDate = formatDate(page.date);
    let date_text = document.createTextNode(formattedDate);
    date_div.appendChild(date_text);

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

// Interpret a page title
const parseTitle = function (title = "") {
    let title_div = document.createElement("div");
    let rVals = [0, 0];
    let limit = 0;
    while (rVals[0] !== -1) {
        limit++;
        if (limit > 10) {
            break;
        }

        rVals = extractTitleTag(title);

        if (rVals[1] !== "") {
            let title_text = document.createTextNode(rVals[1]);
            title_div.appendChild(title_text);
            title = title.replace(rVals[1], "");
        }

        if (rVals[0] !== -1) {
            let tagElement = rVals[0];
            // Add specific logic for handling custom tags
            title = title.replace(rVals[0], "");
        }
    }

    return title_div;
};

// Extract a tag and preceding text
const extractTitleTag = function (title = "") {
    let tagS = title.indexOf("[");
    if (tagS !== -1) {
        let tagE = title.indexOf("]");
        let tag = title.substring(tagS, tagE + 1);
        let beforeTag = tagS !== 0 ? title.substring(0, tagS) : "";
        return [tag, beforeTag];
    } else {
        return [-1, title];
    }
};

// Function to rebuild the blog feed when a radio button is clicked
const inputEnter = function (radioVal = "", numInput = 0) {
    let construct_element = document.getElementById("blog_construct_div");
    construct_element.innerHTML = ''; // Clear current feed
    createBlogConstruct(sortVar = radioVal, numVar = numInput);
};

// Set up radio buttons
const radios_group_type = document.forms["radio_group_type"].elements["construct_group"];
for (let radio of radios_group_type) {
    radio.onclick = function () {
        inputEnter(radioVal = this.value);
    }
};

const radios_group_sort = document.forms["radio_group_sort"].elements["construct_group"];
for (let radio of radios_group_sort) {
    radio.onclick = function () {
        inputEnter(radioVal = this.value);
    }
};

// Initialize blog feed with all posts
createBlogConstruct("all", 0);

document.addEventListener('DOMContentLoaded', () => {
    const blogPosts = [
        { title: "Winter Solstice Web Development", url: "blog/blog001.html", category: "life", date: "2024-12-21" },
        { title: "Album Rec: Blue Mena's Multi Adolescence", url: "blog/blog002.html", category: "album_recs", date: "2024-12-21" },
        { title: "Basics of Clay Pot Metaphysics", url: "blog/blog003.html", category: "philosophy", date: "2024-12-21" },
        
        // Add more blog posts here
    ];

    // Function to display posts
    function displayPosts(posts) {
        const blogDiv = document.getElementById('blog_construct_div');
        blogDiv.innerHTML = ''; // Clear the current content

        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.classList.add('blog-post');

            // Create the title link
            const title = document.createElement('a');
            title.href = post.url;
            title.textContent = post.title;
            title.classList.add('blog-title');

            // Create the category and date
            const details = document.createElement('div');
            details.classList.add('post-details');
            details.innerHTML = `<span class="category">${post.category}</span> | <span class="date">${post.date}</span>`;

            // Add the elements to the post
            postElement.appendChild(title);
            postElement.appendChild(details);
            blogDiv.appendChild(postElement);
        });
    }

    // Call displayPosts initially with all blog posts
    displayPosts(blogPosts);

    // Event listener for category filtering
    const categoryFilters = document.querySelectorAll('input[name="construct_group"]');
    categoryFilters.forEach(input => {
        input.addEventListener('change', filterPosts);
    });

    // Event listener for date sorting
    const dateSorts = document.querySelectorAll('input[name="construct_group"][value="newtoold"], input[name="construct_group"][value="oldtonew"]');
    dateSorts.forEach(input => {
        input.addEventListener('change', sortPosts);
    });

    // Function to filter posts by category
    function filterPosts() {
        const selectedCategory = document.querySelector('input[name="construct_group"]:checked').value;
        const filteredPosts = blogPosts.filter(post => selectedCategory === "all" || post.category === selectedCategory);
        displayPosts(filteredPosts);
    }

    // Function to sort posts by date
    function sortPosts() {
        const sortOrder = document.querySelector('input[name="construct_group"][value="newtoold"]:checked') ? 'newtoold' : 'oldtonew';
        const sortedPosts = [...blogPosts].sort((a, b) => {
            const dateA = new Date(a.date);
            const dateB = new Date(b.date);
            return sortOrder === 'newtoold' ? dateB - dateA : dateA - dateB;
        });
        displayPosts(sortedPosts);
    }
});
