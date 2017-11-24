from flask import g


class LineItem:
    def __init__(self, username, order_id, menu_item_id):
        self.username = username
        self.order_id = order_id
        self.menu_item_id = menu_item_id

    @classmethod
    def create(cls, username, order_id, menu_item_id):
        query = """
            INSERT INTO
              lineitems
              (username, order_id, item_id) 
            VALUES
              (%s, %s, %s);
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (username,order_id, menu_item_id))
            g.db.commit()

        return cls(
            username=username,
            order_id=order_id,
            menu_item_id=menu_item_id
        )

    @classmethod
    def delete(cls, username, order_id, menu_item_id):
        query = """
            DELETE FROM
              lineitems
            WHERE username = %s AND order_id = %s and item_id = %s; 
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (username,order_id, menu_item_id))
            g.db.commit()