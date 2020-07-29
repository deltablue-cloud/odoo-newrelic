from openerp import http, tools
import openerp.addons.bus.bus

try:
    import newrelic
    import newrelic.agent
except ImportError:
    newrelic = None


class BusController(openerp.addons.bus.bus.Controller):

    @http.route()
    def send(self, channel, message):
        if newrelic:
            newrelic.agent.ignore_transaction()
        return super(BusController, self).send(channel, message)

    @http.route()
    def poll(self, channels, last, options=None):
        if newrelic:
            newrelic.agent.ignore_transaction()
        return super(BusController, self).poll(channels, last, options)

if tools.config['debug_mode']:
    class TestErrors(http.Controller):
        @http.route('/test_errors_404', auth='public')
        def test_errors_404(self):
            import werkzeug
            return werkzeug.exceptions.NotFound('Successful test of 404')

        @http.route('/test_errors_500', auth='public')
        def test_errors_500(self):
            raise ValueError
