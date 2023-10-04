from django.contrib import admin

# Register your models here.

from .models import Referee, Fan, Ticket, TicketSales
from .models import Stadium
from .models import Team
from .models import Footballer
from .models import Match
from .models import Goal

admin.site.register(Referee)
admin.site.register(Stadium)
admin.site.register(Team)
admin.site.register(Footballer)
admin.site.register(Match)
admin.site.register(Goal)
admin.site.register(Fan)
admin.site.register(Ticket)
admin.site.register(TicketSales)




#fcgfcvgbhn