// Array of YouTube links
const youtubeLinks = [
    "https://www.youtube.com/embed/vOI2w-aRBN0",
    "https://www.youtube.com/embed/U7e6aLHC7tE",
    "https://www.youtube.com/embed/NGZohEUdZ5g",
    "https://www.youtube.com/embed/-MRwvo3-dyA",
    "https://www.youtube.com/embed/p_-y0UCwAqg",
    "https://www.youtube.com/embed/jW_0aO8VHyo"
];

// Function to return a random YouTube link from the array
function getRandomYoutubeLink() {
    return youtubeLinks[Math.floor(Math.random() * youtubeLinks.length)];
}

// Function to show a video
function showVideo() {
    const videoURL = getRandomYoutubeLink(); // This function should return the URL of a random video

    $('#youtube-video').attr('src', videoURL + '?autoplay=1'); // Assign the videoURL to the iframe's src
    $('#waiting-video').removeClass('hidden'); // Remove the 'hidden' class to show the video
}

// Function to hide the video
function hideVideo() {
    // Hide the video
    $("#waiting-video").addClass("hidden");
    // Reset the source of the video so it stops playing
    document.getElementById('youtube-video').src = "";
}
