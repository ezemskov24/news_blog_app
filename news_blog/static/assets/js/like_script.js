// like_script.js

document.addEventListener("DOMContentLoaded", function() {
  const likeBtn = document.getElementById("like-btn");
  const dislikeBtn = document.getElementById("dislike-btn");
  const likeCount = document.getElementById("like-count");

  if (userLikedNews === "True") {
    likeBtn.disabled = true;
  }

  if (userDislikedNews === "True") {
    dislikeBtn.disabled = true;
  }

  likeBtn.addEventListener("click", function() {
    fetch(`/${newsPk}/like/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
    .then(response => response.json())
    .then(data => {
      likeCount.textContent = data.likes;
      likeBtn.disabled = true;
      dislikeBtn.disabled = true;
    })
    .catch(error => {
      console.error("Error:", error);
    });
  });

  dislikeBtn.addEventListener("click", function() {
    fetch(`/${newsPk}/dislike/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
    })
    .then(response => response.json())
    .then(data => {
      likeCount.textContent = data.likes;
      likeBtn.disabled = true;
      dislikeBtn.disabled = true;
    })
    .catch(error => {
      console.error("Error:", error);
    });
  });
});
