// blog_posts.js

const posts = [
    {
      id: "001",
      title: "First Post",
      date: "2025-04-01",
      description: "This is the beginning of my blog. Here's what to expect.",
      url: "blog/posts/post001.html"
    },
    {
      id: "002",
      title: "Second Thoughts",
      date: "2025-04-03",
      description: "Some reflections on how things have evolved.",
      url: "blog/posts/post002.html"
    }
  ];
  
  function createBlogList() {
    const container = document.getElementById("blog-list");
  
    posts.sort((a, b) => new Date(b.date) - new Date(a.date)); // Newest first
  
    posts.forEach(post => {
      const article = document.createElement("article");
      article.className = "blog-preview";
  
      article.innerHTML = `
        <h2><a href="${post.url}">${post.title}</a></h2>
        <p class="date">${new Date(post.date).toLocaleDateString()}</p>
        <p class="description">${post.description}</p>
      `;
  
      container.appendChild(article);
    });
  }
  
  createBlogList();
  