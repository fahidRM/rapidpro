
class VoiceXMLException(Exception):
    pass


class Response(object):
    def __init__(self, **kwargs):
        self.document = '<?xml version="1.0" encoding="UTF-8"?>'

        result = '<vxml version = "2.1"><form>'
        self.document += result

    def __str__(self):
        if self.document.find('</form></vxml>') > 0:
            return self.document
        return self.document + '</form></vxml>'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def append(self, parts):
        self.document += parts
        return self

    def say(self, text, **kwargs):
        result = '<block><prompt>' + text + '</prompt></block>'
        self.document += result
        return self

    def play(self, url=None, digits=None, **kwargs):
        if url is None and digits is None:
            raise VoiceXMLException("Please specify either a url or digits to play.",)

        result = ''
        if digits:
            result += '<block><prompt>' + digits + '</prompt></block>'

        if url:
            result += '<block><prompt><audio src="' + url + '"/></prompt></block>'

        self.document += result
        return self

    def pause(self, **kwargs):
        result = '<block><prompt><break '
        if kwargs.get('length', False):
            result += ' time="' + kwargs.get('length') + '"'

        result += '/></prompt></block>'

        self.document += result
        return self

    def redirect(self, url=None, **kwargs):
        result = '<goto nextitem="' + url + '" />'

        self.document += result
        return self

    def hangup(self, **kwargs):
        result = '<exit/>'
        self.document += result
        return self

    def reject(self, reason=None, **kwargs):
        self.hangup()
        return self

    def gather(self, **kwargs):
        result = '<field name="Digits">'
        result += '<grammar termtimeout="60s" '

        if kwargs.get('finishOnKey', False):
            result += 'termchar="%s" ' % kwargs.get('finishOnKey')

        result += 'src="builtin:dtmf/digits'

        if kwargs.get('numDigits', False):
            result += '?minlength=%s;maxlength=%s' % (kwargs.get('numDigits'), kwargs.get('numDigits'))

        result += '" /></field>'
        if kwargs.get('action', False):
            method = kwargs.get('method', 'post')
            result += '<filled><submit next="' + kwargs.get('action') + '" method="' + method + '" /></filled>'

        self.document += result
        return self

    def record(self, **kwargs):
        result = '<record name="UserRecording" beep="true"'
        if kwargs.get('maxLength', False):
            result += 'maxtime="' + kwargs.get('maxLength') + 's"'

        result += ' finalsilence="4000ms" dtmfterm="true" type="audio/x-wav">'

        if kwargs.get('action', False):
            method = kwargs.get('method', 'post')
            result += '<filled><submit next="' + kwargs.get('action') + '" method="' + method + '" '
            result += 'enctype="multipart/form-data" /></filled>'

        result += '</record>'

        self.document += result
        return self
