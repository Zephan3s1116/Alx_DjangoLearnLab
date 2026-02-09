# Blog Images

This directory contains images used in the blog.

## Usage

Place your blog images here and reference them in templates using:

```html
{% load static %}
<img src="{% static 'blog/images/your-image.jpg' %}" alt="Description">
```

## Recommended Image Sizes

- Blog post featured images: 1200x630px
- Author avatars: 200x200px
- Thumbnails: 400x300px
