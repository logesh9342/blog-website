from typing import Any
from fewapp.models import Post,Category
from django.core.management.base import BaseCommand
import random


class Command(BaseCommand):
    help = "This command inserts post data"

    def handle(self, *args: any, **options: any):
     #delete existing data
     Post.objects.all().delete()
     titles = [
            "Understanding Django Basics",
            "Advanced Python Techniques",
            "Building Responsive Websites",
            "Introduction to Machine Learning",
            "Mastering Frontend Development",
            "The Art of Debugging Code",
            "Deploying Web Applications",
            "Guide to RESTful APIs",
            "Data Science with Python",
            "Designing Scalable Systems",
            "JavaScript for Beginners",
            "Exploring Cloud Computing",
            "Database Optimization Strategies",
            "Learning React Step-by-Step",
            "Version Control with Git",
            "Creating Dynamic Web Pages",
            "Artificial Intelligence Essentials",
            "Mastering CSS for Layouts",
            "Web Development Best Practices",
            "Introduction to SQL Queries",
        ]

     contents = [
            "Learn the fundamentals of Django for web development, covering models, views, and templates to create powerful web apps.",
"Discover advanced techniques to write efficient Python code, focusing on optimizing performance and improving readability.",
"Create websites that look great on any device by mastering responsive design and cross-browser compatibility.",
"Explore the basics of machine learning and predictive modeling, including data preprocessing and model evaluation.",
"Master essential frontend tools like HTML, CSS, and JavaScript to build interactive and visually appealing websites.",
"Understand the key principles to debug code effectively, helping you solve issues faster and more efficiently.",
"Learn how to deploy web applications to the cloud, making them accessible from anywhere with minimal downtime.",
"Build APIs that adhere to RESTful principles, enabling efficient communication between different software components.",
"Analyze and visualize data using Python libraries like Pandas, Matplotlib, and Seaborn for actionable insights.",
"Design systems that can handle large-scale traffic, ensuring reliability, scalability, and high availability.",
"Get started with JavaScript, the language of the web, and learn how it enables dynamic, interactive web experiences.",
"Understand the fundamentals of cloud services and architecture, including infrastructure and platform services.",
"Improve database performance with optimization strategies, such as indexing, query tuning, and caching.",
"Learn how to build dynamic interfaces using React, one of the most popular JavaScript libraries for UI development.",
"Manage your codebase with Git and version control, enabling collaborative development and code tracking.",
"Create interactive and dynamic web pages using JavaScript, enhancing user engagement and experience.",
"Explore the basics of artificial intelligence concepts, including machine learning, neural networks, and natural language processing.",
"Master CSS techniques for creating complex layouts with Flexbox, Grid, and other modern styling methods.",
"Follow best practices to ensure clean, maintainable web code, focusing on readability, structure, and scalability.",
"Write powerful SQL queries to interact with databases effectively, optimizing data retrieval and management.",




        ]

     img_urls = [
            "https://picsum.photos/id/1/800/400",
            "https://picsum.photos/id/2/800/400",
            "https://picsum.photos/id/3/800/400",
            "https://picsum.photos/id/4/800/400",
            "https://picsum.photos/id/5/800/400",
            "https://picsum.photos/id/6/800/400",
            "https://picsum.photos/id/7/800/400",
            "https://picsum.photos/id/8/800/400",
            "https://picsum.photos/id/9/800/400",
            "https://picsum.photos/id/10/800/400",
            "https://picsum.photos/id/11/800/400",
            "https://picsum.photos/id/21/800/400",
            "https://picsum.photos/id/12/800/400",
            "https://picsum.photos/id/22/800/400",
            "https://picsum.photos/id/13/800/400",
            "https://picsum.photos/id/14/800/400",
            "https://picsum.photos/id/15/800/400",
            "https://picsum.photos/id/16/800/400",
            "https://picsum.photos/id/17/800/400",
            "https://picsum.photos/id/18/800/400",
         ]


     categories = Category.objects.all() 
     for title, content, img_url in zip(titles, contents, img_urls):
          category = random.choice(categories)
          Post.objects.create(title=title, content=content, img_url=img_url ,category=category)
   
     self.stdout.write(self.style.SUCCESS("Completed inserting data"))
