from django.test import TestCase

from flatpagesplus.models import MainFlatPage, SubFlatPage


class FlatPageModelsTests(TestCase):
    fixtures = ['sample_flatpages.json']
    
    def test_no_extra_or_links(self):
        """A flatpage with neither has empty string attributes."""
        fp = MainFlatPage.objects.get(pk=1)
        self.assertEqual(fp.head_content, '')
        self.assertEqual(fp.foot_content, '')
    
    def test_with_extra(self):
        """A flatpage with extra content has filled attributes."""
        fp = MainFlatPage.objects.get(pk=201)
        self.assertEqual(fp.head_content, '<link rel="stylesheet" href="" />')
        self.assertEqual(fp.foot_content, '<script src=""></script>')
    
    def test_with_links(self):
        """A flatpage with subpages has links in attributes."""
        fp = MainFlatPage.objects.get(pk=202)
        self.assertEqual(fp.head_content, '<link rel="stylesheet" type="text/css" href="css/" media="screen, projection" />')
        self.assertEqual(fp.foot_content, '<script type="text/javascript" src="js/"></script>')
    
    def test_with_both(self):
        """A flatpage with both has content concatenated with links."""
        fp = MainFlatPage.objects.get(pk=203)
        self.assertEqual(fp.head_content, '<link rel="stylesheet" href="" />\n<link rel="stylesheet" type="text/css" href="css/" media="screen, projection" />')
        self.assertEqual(fp.foot_content, '<script src=""></script>\n<script type="text/javascript" src="js/"></script>')
