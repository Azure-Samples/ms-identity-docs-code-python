from django.test import TestCase
from django.template.exceptions import TemplateDoesNotExist


class TemplateAccessibilityTest(TestCase):
    def test_login_attempt_should_render_its_template(self):
        try:
            response = self.client.get("/")  # It will trigger the login attempt
            print(response.content)
            # The response could be rendered by login.html if .env is complete,
            # or by auth_error.html otherwise.
            # I haven't figured out how to mock the .env to test it decisively.
        except TemplateDoesNotExist:
            self.fail(
                "Template should be accessible, "
                "typically came from inside the Identity package.")

