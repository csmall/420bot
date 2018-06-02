
import pytz
import datetime

class FourTwenty(object):

    # Just some to spread the tzinfo around
    _DEFAULT_COUNTRIES=[
            'au', 'ca', 'cn', 'de', 'es', 'fi', 'fr', 'gl', 'gr', 'ie',
            'in', 'it', 'jp', 'gb', 'mo', 'pk', 'pt', 'nz', 'se', 'sk',
            'tr', 'us', 'za']
    today = None
    offsets = None
    four_twenty_seconds = 16 * 3600 + 20 * 60
    day_seconds = 24 * 3600

    def __init__(self, countries=None):
        if countries is None:
            countries = self._DEFAULT_COUNTRIES
        self.today = datetime.datetime(2018, 1, 1)
        self.fill_tznames(countries)
        self.offsets = {}

    def fill_tznames(self, countries):
        self.tznames = []
        for country in countries:
            self.tznames.extend(pytz.country_timezones[country])

    def autofill_offsets(self):
        for tzname in self.tznames:
            offset = self.four_twenty_seconds - \
                    pytz.timezone(tzname).utcoffset(self.today).seconds
            if offset < 0:
                offset += self.day_seconds
            try:
                location = tzname.split('/')[1]
            except IndexError:
                location = tzname
            # Replace underscore with space
            location.replace('_', ' ')

            if offset in self.offsets:
                if not location in self.offsets[offset]:
                    self.offsets[offset].append(location)
            else:
                self.offsets[offset] = [location,]

    def seconds_past_midnight(self, when):
        ''' Return the number of seconds past midnight UTC '''
        if when is None:
            when = datetime.datetime.utcnow()
        seconds = when.second + when.minute * 60 + when.hour * 3600
        return seconds

    def all_offsets(self):
        ''' Return a list of all known offsets '''
        return sorted(self.offsets.keys())

    def timezones(self, seconds):
        ''' Return a list of cities that match the seconds past midnight '''
        if self.offsets is None or seconds not in self.offsets:
            return None
        return self.offsets[seconds]

    def next_offset(self, when=None):
        ''' return next available offset '''
        if self.offsets is None:
            return None
        now_seconds = self.seconds_past_midnight(when)
        for offset in self.all_offsets():
            if offset > now_seconds:
                return offset
        return self.all_offsets()[0]

    def wait_time(self, when=None):
        next_offset = self.next_offset(when)
        now_seconds = self.seconds_past_midnight(when)
        wait_time = next_offset - now_seconds
        if wait_time < 0:
            wait_time += self.day_seconds
        return wait_time
