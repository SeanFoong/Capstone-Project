def convert(form_field):
    db_field = form_field.replace(' ', '_').lower()
    return db_field