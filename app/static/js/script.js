let feed= document.getElementById('feed');
let feedMessages = document.querySelector('#feed > div');
let writtingMessage = document.getElementById('message');
let submitButton = document.getElementById('submit');

function clearMessage() {
    writtingMessage.value = '';
}

function createPost(author, content) {
    let post = document.createElement('p');
    post.classList.add('post', author);
    if (author == 'sent') {
        post.textContent = content;
    } else {
        post.appendChild(content);
        console.log(content);
        console.log(post);
    }
    feedMessages.appendChild(post);
    feed.scrollTop = feed.scrollHeight;
}

function processUserInput() {
    // Get the user message
    let userMessage = {'author': 'sent', 'content': writtingMessage.value};

    // Create a post for the feed
    createPost(userMessage['author'], userMessage['content']);

    // Place waiting message to feed's bottom
    feedMessages.appendChild(document.getElementById('waiting'));

    // Remove the class 'hidden' for the waiting message
    let waitingPost = document.getElementById('waiting');
    waitingPost.classList.remove('hidden');

    // Send the message to '/process'
    let postParser = new XMLHttpRequest();
    let parserUrl = new URL('process', document.URL);
    let postBody = new FormData();
    postBody.append('message', writtingMessage.value)

    // Clear the writing form
    clearMessage();

    postParser.open('POST', parserUrl);
    postParser.onreadystatechange = function () {
        if (postParser.status == 200 && postParser.response) {
            console.log(postParser.response);
        }
    }
    postParser.send(postBody);

    // Hide waiting message
    // waitingPost.classList.add('hidden');
}

writtingMessage.addEventListener('keydown', function(event) {
    // Event for using <Ctrl> or <Meta> + <Enter> for carriage return and <Enter> to submit message
    if (event.key == 'Enter' && (event.metaKey || event.ctrlKey)) {
        event.preventDefault();
        writtingMessage.value += '\n';
        this.scrollTop = this.scrollHeight;
    } else if (event.key == 'Enter' && writtingMessage.value) {
        event.preventDefault();
        processUserInput();
    }
});

submitButton.addEventListener('click', function(event) {
    event.preventDefault();
    if (writtingMessage.value) {
        processUserInput();
    }
})

// Execute Clear message in case the user refresh the page with a message already written
clearMessage();
