from datetime import datetime

from flask import g

from data.menuitems import MenuItem


class Order:
    def __init__(self,
                 order_id,
                 restaurant_id,
                 organizer,
                 restaurant_name,
                 order_time):
        self.order_id = order_id
        self.restaurant_id = restaurant_id
        self.organizer = organizer
        self.restaurant_name = restaurant_name
        self.order_time = order_time

    @classmethod
    def create(cls, organizer, restaurant_id, order_time: datetime):
        query = """
            INSERT INTO
              grouporders
              (restaurant, organizer, ordertime)
            VALUES
              (%s, %s, %s)
            RETURNING
              order_id, 
              (select name from restaurants where restaurant_id=grouporders.restaurant);
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (restaurant_id, organizer, order_time))
            row = cursor.fetchone()
            g.db.commit()

        return cls(
            order_id=row[0],
            restaurant_id=restaurant_id,
            organizer=organizer,
            restaurant_name=row[1],
            order_time=order_time
        )

    @classmethod
    def by_id(cls, order_id):
        query = """
            SELECT 
              g.restaurant,
              g.organizer,
              g.ordertime,
              r.name
            FROM
              grouporders g
            INNER JOIN
              restaurants r ON g.restaurant = r.restaurant_id
            WHERE
              order_id = %s; 
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (order_id,))
            row = cursor.fetchone()

        return cls(
            order_id=order_id,
            restaurant_id=row[0],
            organizer=row[1],
            order_time=row[2],
            restaurant_name=row[3]
        )

    @classmethod
    def list_current(cls):
        query = """
            SELECT
              g.order_id,
              g.restaurant,
              g.organizer,
              g.ordertime,
              r.name
            FROM 
              grouporders g
            INNER JOIN
              restaurants r ON g.restaurant = r.restaurant_id
            WHERE
              ordertime > now()
            ORDER BY
              ordertime ASC;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        orders = []
        for row in rows:
            orders.append(cls (
                order_id=row[0],
                restaurant_id=row[1],
                organizer=row[2],
                order_time=row[3],
                restaurant_name=row[4]
            ))

        return orders

    def change_time(self, new_time):
        query = """
            UPDATE 
              grouporders 
            SET 
              ordertime = %s
            WHERE
              order_id = %s;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (new_time, self.order_id))
            g.db.commit()

        self.order_time = new_time

    def get_all_items(self):
        query = """
            SELECT
              l.username,
              m.item_id,
              m.name,
              m.price
            FROM
              lineitems l
            INNER JOIN menuitems m ON l.item_id = m.item_id
            WHERE
              l.order_id = %s;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (self.order_id,))
            rows = cursor.fetchall()

        items = {}
        for row in rows:
            username = row[0]
            if username not in items:
                items[username] = []

            items[username].append(MenuItem(row[1],
                                            self.restaurant_id,
                                            row[2],
                                            row[3]))

        return items

    def get_items_for_user(self, username):
        query = """
            SELECT
              m.item_id,
              m.name,
              m.price
            FROM
              lineitems l
            INNER JOIN menuitems m ON l.item_id = m.item_id
            WHERE
              l.order_id = %s AND l.username = %s;
        """

        with g.db.cursor() as cursor:
            cursor.execute(query, (self.order_id, username))
            rows = cursor.fetchall()

        items = []
        for row in rows:
            items.append(MenuItem(row[0],
                                  self.restaurant_id,
                                  row[1],
                                  row[2]))

        return items
