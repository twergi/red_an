from PIL import Image
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def square_crop(path):
    with Image.open(path) as im:
        x = im.width
        y = im.height

        if x % 2 != y % 2:
            if x % 2:
                x -= 1
            else:
                y -= 1

        if im.width > im.height:
            dif = (x - y) // 2
            im = im.crop((dif, 0, dif + y, y))

        if im.height > im.width:
            dif = (y - x) // 2
            im = im.crop((0, dif, x, dif + x))

        if x > 300:
            im.thumbnail((300, 300))
        im.save(path)


def paginatePosts(request, posts_all):
    page_num = request.GET.get('page')
    p_posts = Paginator(posts_all, 10)
    try:
        posts = p_posts.page(page_num)
    except PageNotAnInteger:
        page_num = 1
        posts = p_posts.page(page_num)
    except EmptyPage:
        page_num = p_posts.num_pages
        posts = p_posts.page(page_num)

    leftIndex = int(page_num) - 4
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = int(page_num) + 5
    if rightIndex > p_posts.num_pages:
        rightIndex = p_posts.num_pages + 1

    page_range = range(leftIndex, rightIndex)

    return posts, page_range
