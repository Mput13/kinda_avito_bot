def compile_lot_message(lot: dict):
    return f"""Объявление {lot['id']}
{lot['title']} {lot['price']}
{lot['description']}
{lot['creator']}"""
