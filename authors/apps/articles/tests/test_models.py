from authors.apps.authentication.tests_.test_base_class import BaseTestClass
from authors.apps.articles.models import Article
from authors.apps.articles.apps import ArticlesConfig


class ArticleModelTest(BaseTestClass):
    def test_article_representation(self):
        """
         Tests the return datatype of the article elements
         """
        self.assertIsInstance(self.article, dict)

    def test_article_model(self):
        """
        This function validates the internal state of the model to ensure
        it returns the correct values
        """
        self.assertEqual(self.article['title'], "hello worlfd")
        self.assertEqual(self.article['description'], "desctriptuo")
        self.assertEqual(self.article['body'], "boddydydabagd")

    def test_str_returns_correct_string_representation(self):
        """
        Tests that __str__ generates a correct string representation of
        article title
        """
        article = Article(title="Hello today",
                          description="Today is beautiful",
                          body="This is the body")
        self.assertEqual(str(article), "Hello today")

    def test_articles_app_instance(self):
        """
        Tests the instance of the articles app
        """
        self.assertEqual(ArticlesConfig.name, 'articles')
