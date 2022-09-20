function clickVote(element) {
    let vote = element.target.dataset.value
    let post_id = element.target.dataset.post_id
    let section_id = element.target.dataset.section_id
    fetch(`http://127.0.0.1:8000/api/sections/${section_id}/posts/${post_id}/vote`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'value': vote})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
}

function addVoteEvents() {
    let voteButtons = document.getElementsByClassName("post_vote")

    for (let i = 0; i < voteButtons.length; i++) {
        voteButtons[i].addEventListener('click', clickVote)
    }
}

addVoteEvents()
