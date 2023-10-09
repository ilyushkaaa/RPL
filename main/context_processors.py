from django.db import connection

from main.models import TicketSales


def my_context_processor(request):
    num = 0
    if request.user.is_authenticated:

        current_email = request.user.email
        num = TicketSales.get_items_in_basket_count(current_email)

        return {'number': num}
    return {'number': num}


def show_tickets_in_basket(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        with connection.cursor() as cursor3:
            query = "select t1.name, t2.name, ticket.id, sector, row, place from rpl.ticket_sales join rpl.ticket on rpl.ticket.id = rpl.ticket_sales.ticket_id join rpl.match on rpl.match.id = rpl.ticket.match_id join rpl.team t1 on t1.id = rpl.match.team_home_id join rpl.team t2 on t2.id = rpl.match.team_guest_id where rpl.ticket_sales.fan_id = %s and is_in_basket = true"
            cursor3.execute(query, [user_email])
            tickets_in_basket = cursor3.fetchall()
            return {'tickets_in_basket': tickets_in_basket}

    return {'tickets_in_basket': ''}

