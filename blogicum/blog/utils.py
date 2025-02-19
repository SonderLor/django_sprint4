from django.utils import timezone


def get_relevant_posts(posts):
    return (
        posts.filter(
            is_published=True
        ).filter(
            pub_date__lte=timezone.now()
        ).filter(
            category__is_published=True
        )
    )
