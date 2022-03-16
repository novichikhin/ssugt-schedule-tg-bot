from telegram_bot_calendar import DetailedTelegramCalendar, base


class CalendarService(DetailedTelegramCalendar):
    first_step = base.DAY
    locale = 'ru'
