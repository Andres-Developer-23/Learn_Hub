from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def course_icon(course, size=80, rounded=18):
    if course.image:
        return mark_safe(
            f'<img src="{course.image.url}" alt="{course.title}" '
            f'style="width:{size}px;height:{size}px;object-fit:cover;border-radius:{rounded}px;'
            f'box-shadow:0 8px 30px rgba(0,0,0,0.3)">'
        )

    letter = course.title[0].upper() if course.title else '?'
    cid = f'cg{course.id}'
    colors = [
        ('#4f8ef7', '#8b5cf6'),
        ('#10b981', '#059669'),
        ('#f59e0b', '#d97706'),
        ('#ec4899', '#db2777'),
        ('#14b8a6', '#0d9488'),
        ('#f97316', '#ea580c'),
        ('#8b5cf6', '#6d28d9'),
        ('#06b6d4', '#0891b2'),
    ]
    c1, c2 = colors[course.id % len(colors)]

    svg = (
        f'<svg viewBox="0 0 100 100" style="width:{size}px;height:{size}px;border-radius:{rounded}px;'
        f'box-shadow:0 8px 30px rgba(0,0,0,0.3)" xmlns="http://www.w3.org/2000/svg">'
        f'<defs><linearGradient id="{cid}" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" style="stop-color:{c1}"/>'
        f'<stop offset="100%" style="stop-color:{c2}"/>'
        f'</linearGradient></defs>'
        f'<rect width="100" height="100" rx="18" fill="url(#{cid})"/>'
        f'<text x="50" y="67" text-anchor="middle" font-size="40" fill="white" '
        f'font-family="Inter,sans-serif" font-weight="700">{letter}</text>'
        f'</svg>'
    )
    return mark_safe(svg)


@register.simple_tag
def course_icon_small(course, size=48):
    return course_icon(course, size=size, rounded=10)
