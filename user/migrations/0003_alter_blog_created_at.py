# Generated by Django 5.1.4 on 2025-03-19 13:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_category_blog_comment_bloglike_blogview"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="created_at",
            field=models.DateField(blank=True, null=True),
        ),
    ]
