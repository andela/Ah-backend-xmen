
from django.test import TestCase
from authors.apps.utils.estimator import article_read_time


class TestData():
    def __init__(self):
        self.paragraph = "Sunset is the time of day when our sky meets the outer"\
            +" space solar winds. There are blue, pink, and purple "\
            +"swirls, spinning and twisting, like clouds of balloons "\
            +"caught in a whirlwind. The sun moves slowly to hide "\
            +"behind the line of horizon, while the moon races to "\
            +"take its place in prominence atop the night sky. People"\
            +" slow to a crawl, entranced, fully forgetting the deeds"\
            +" that must still be done. There is a coolness, a calmness, when the sun does set. "

        self.short_article = self.paragraph+self.paragraph+self.paragraph
        self.medium_article = ""
        for i in range(30):
            self.medium_article += self.paragraph
        self.long_article = ""
        for i in range(100):
            self.long_article += self.paragraph
        self.very_long_article = ""
        for i in range(500):
            self.very_long_article += self.paragraph

        self.longest_article = ""
        for i in range(7000):
            self.longest_article += self.paragraph



class TestEstimateReadTime(TestCase):
    def test_estimate_read_time_for_short_article(self):
        time_to_read = article_read_time(test_data.short_article)
        self.assertIn("less than ",time_to_read)

    def test_estimate_read_time_for_medium_article(self):
        time_to_read = article_read_time(test_data.medium_article)
        self.assertIn("9 mins",time_to_read)

    def test_estimate_read_time_for_long_article(self):
        time_to_read = article_read_time(test_data.long_article)
        self.assertIn("31 mins",time_to_read)
        
    def test_estimate_read_time_for_very_long_article(self):
        time_to_read = article_read_time(test_data.very_long_article)
        self.assertIn("2 hrs and 38 mins",time_to_read)
        
    def test_estimate_read_time_for_longest_article(self):
        time_to_read = article_read_time(test_data.longest_article)
        self.assertIn("more than 1 day",time_to_read)
        
        
test_data = TestData()
