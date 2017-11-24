from flask import g


class MenuItem:
    def __init__(self, item_id, restaurant_id, name, price):
        self.item_id = item_id
        self.restaurant_id = restaurant_id
        self.name = name
        self.price = price

    @classmethod
    def list(cls, restaurant_id):
        query = """
            SELECT
              item_id, name, price
            FROM
              menuitems
            WHERE restaurant = %s;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (restaurant_id,))
            rows = cursor.fetchall()

        items = []
        for row in rows:
            items.append(cls(
                item_id=row[0],
                restaurant_id=restaurant_id,
                name=row[1],
                price=row[2]
            ))

        return items

    @classmethod
    def by_id(cls, menu_item_id):
        query = """
            SELECT 
              item_id, restaurant, name, price 
            FROM
              menuitems
            WHERE
              item_id=%s; 
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (menu_item_id,))
            row = cursor.fetchone()

        return cls(
            item_id=row[0],
            restaurant_id=row[1],
            name=row[2],
            price=row[3]
        )

    @classmethod
    def create(cls, restaurant_id, name, price):
        query = """
            INSERT INTO
              menuitems
              (restaurant, name, price)
            VALUES
              (%s, %s, %s)
            RETURNING
              item_id;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (restaurant_id, name, price))
            row = cursor.fetchone()
            g.db.commit()

        return cls(
            item_id=row[0],
            restaurant_id=restaurant_id,
            name=name,
            price=price
        )

    def update(self, name, price):
        query = """
            UPDATE
              menuitems
            SET
              name = %s, price = %s
            WHERE
              item_id = %s;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (name, price, self.item_id))
            g.db.commit()

        self.name = name
        self.price = price

    def delete(self):
        query = """
            DELETE FROM
              menuitems
            WHERE
              item_id = %s;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (self.item_id,))
            g.db.commit()
