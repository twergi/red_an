const site_url = '127.0.0.1:8000'

function getPostRating(section_id, post_id, user_token, vote) {
    return fetch(`http://${site_url}/api/sections/${section_id}/posts/${post_id}/vote`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${user_token}`,
        },
        body: JSON.stringify({
            'value': vote,
        })

    })
}

function getCommentRating(section_id, post_id, comment_id, user_token, vote) {
    return fetch(`http://${site_url}/api/sections/${section_id}/posts/${post_id}/comments/${comment_id}/vote`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${user_token}`,
        },
        body: JSON.stringify({
            'value': vote,
        })
    })
}

async function clickPostVote(element) {
    let vote = element.target.dataset.value

    let post_id = element.target.dataset.post_id
    let section_id = element.target.dataset.section_id
    let post_rating = parseInt(document.getElementById('post-'+post_id+'-rating').innerHTML)
    let rating_element = document.getElementById('post-'+post_id+'-rating')

    response = await getPostRating(section_id, post_id, user_token, vote)
    data = await response.json()
    post_rating = data.rating

    if (element.target.classList.contains('voted')) {
        element.target.classList.remove('voted')

    }
    else {
        element.target.classList.add('voted')

        let counter_rating = ''

        if (vote == 'up') {
            counter_rating = document.getElementById('post-' + post_id + '-down')
        }
        else {
            counter_rating = document.getElementById('post-' + post_id + '-up')
        }
        if (counter_rating.classList.contains('voted')) {
            counter_rating.classList.remove('voted')
        }
    }
    rating_element.innerHTML = post_rating
}

async function clickCommentVote(element) {
    let vote = element.target.dataset.value
    let post_id = element.target.dataset.post_id
    let section_id = element.target.dataset.section_id
    let comment_id = element.target.dataset.comment_id
    let comment_rating = parseInt(document.getElementById('comment-'+comment_id+'-rating').innerHTML)
    let rating_element = document.getElementById('comment-'+comment_id+'-rating')

    response = await getCommentRating(section_id, post_id, comment_id, user_token, vote)
    data = await response.json()
    comment_rating = data.rating

    if (element.target.classList.contains('voted')) {
        element.target.classList.remove('voted')

    }
    else {
        element.target.classList.add('voted')

        let counter_rating = ''

        if (vote == 'up') {
            counter_rating = document.getElementById('comment-' + comment_id + '-down')
        }
        else {
            counter_rating = document.getElementById('comment-' + comment_id + '-up')
        }
        if (counter_rating.classList.contains('voted')) {
            counter_rating.classList.remove('voted')
        }
    }
    rating_element.innerHTML = comment_rating
}

async function getVotedPosts() {
    return fetch(`http://127.0.0.1:8000/api/users/${user_username}/voted_posts`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${user_token}`,
    }
    })
    .then(response => response.json())
}

async function getVotedComments(post_id) {
    return fetch(`http://127.0.0.1:8000/api/users/${user_username}/posts/${post_id}/voted_comments`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${user_token}`,
    }
    })
    .then(response => response.json())
}

async function addVoteEvents() {
    let voteButtons = document.getElementsByClassName("post_vote")
    let voteCommentButtons = document.getElementsByClassName("comment_vote")

    let post_id = ''
    let voted_comments = ''
    if (voteCommentButtons.length !== 0) {
        post_id = voteCommentButtons[0].dataset.post_id
        voted_comments = JSON.parse(await getVotedComments(post_id))

        for (let i = 0; i < voteCommentButtons.length; i++) {
            if (voteCommentButtons[i].dataset.value == voted_comments[voteCommentButtons[i].dataset.comment_id]) {
                voteCommentButtons[i].classList.add('voted')
            }
            voteCommentButtons[i].addEventListener('click', clickCommentVote)
        }
    }

    if (voteButtons.length !== 0) {
        let voted_posts = JSON.parse(await getVotedPosts())

        for (let i = 0; i < voteButtons.length; i++) {
            if (voteButtons[i].dataset.value == voted_posts[voteButtons[i].dataset.post_id]) {
                voteButtons[i].classList.add('voted')
            }
            voteButtons[i].addEventListener('click', clickPostVote)
        }
    }




}

if (user_username != '') {
    addVoteEvents()
}
