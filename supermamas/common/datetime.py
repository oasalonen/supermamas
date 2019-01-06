from flask_babel import gettext

def weekdays():
    return [
        gettext(u"Mon"), 
        gettext(u"Tue"), 
        gettext(u"Wed"), 
        gettext(u"Thu"), 
        gettext(u"Fri"), 
        gettext(u"Sat"), 
        gettext(u"Sun")
        ]