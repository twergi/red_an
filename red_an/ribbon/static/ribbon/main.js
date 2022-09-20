function clickVote(element) {
    console.log(element.target)
}

function addVoteEvents() {
    let voteButtons = document.getElementsByClassName("post_vote")

    for (let i = 0; i < voteButtons.length; i++) {
        voteButtons[i].addEventListener('click', clickVote)
    }
}

addVoteEvents()
