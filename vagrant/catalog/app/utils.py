from flask import flash
from wtforms import SelectMultipleField
from slugify import Slugify
from .app_setup import app
from jinja2 import Markup
# Misc utils methods


def flash_errors(form):
    # Create a flash message for all the WTForms errors
    # Taken from http://flask.pocoo.org/snippets/12/
    form_errors = getattr(form, 'errors', {'items': []})
    for field, errors in form_errors.items():
        for error in errors:
            flash(u"Error in %s - %s" % (
                getattr(form, field).label.text,
                error
            ))


def slugify_category_list(category_list):
    # "Slugify" the categories received from the New/Edit item forms
    if category_list is not None:
        slugifier = Slugify(to_lower=True)
        slugified_list = []
        for cat in category_list:
            cat_elem = cat.split('|')
            if len(cat_elem) == 1:
                cat_elem.append(cat_elem[0])
            slugified_list.append([cat, cat_elem[0], slugifier(cat_elem[1])])
        return slugified_list


def allowed_file(filename):
    # Return if the file extension is in the list of allowed extensions
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


class momentjs(object):
    # Class to display the dates in local format, using momentjs
    # Taken from: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-dates-and-times
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        return \
            Markup("<script>\ndocument.write(moment(\"%s\").%s);\n</script>"
                   % (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
app.jinja_env.globals['momentjs'] = momentjs


class OpenSelectMultipleField(SelectMultipleField):
    """
    Attempt to make an open ended select multiple field that can accept dynamic
    choices added by the browser.
    """
    # Taken from http://stackoverflow.com/a/31282492/2423859
    def pre_validate(self, form):
        pass
