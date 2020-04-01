class FormBlueprintParser:
    def __init__(self):
        self.html = "";

    def parse(self, dic):
        _html = ""
        for section in dic['sections']:
            _html += self._parse_section(section)

        return _html

    def _parse_section(self, section):
        _id = section['id']
        _section_html = "<section id='"+_id+"'>"
        for _field in section['fields']:
            if _field['id'].endswith('strng'):
                _section_html += self._parse_string_field(_field)
            elif _field['id'].endswith('intgr'):
                _section_html += self._parse_integer_field(_field)
            elif _field['id'].endswith('fl'):
                _section_html += self._parse_fl_field(_field)
            elif _field['id'].endswith('mcqs'):
                _section_html += self._parse_mcqs_field(_field)
            elif _field['id'].endswith('mcqm'):
                _section_html += self._parse_mcqm_field(_field)
        _section_html += "</section>"
        return _section_html

    def _parse_string_field(self, field):
        #return the html string
        _field_id = field['id']
        _field_html = "<p>"+field['title']+"</p>";
        if field['required']==True:
            _field_html += "<input type='text' id='"+_field_id+"' required='required'><br>"
        else:
            _field_html += "<input type='text' id='"+_field_id+"'><br>"

        return _field_html

    def _parse_integer_field(self, field):
        #return the html string
        _field_id = field['id']
        _field_html = "<p>"+field['title']+"</p>";
        if field['required']==True:
            _field_html += "<input type='number' id='"+_field_id+"' required='required'><br>"
        else:
            _field_html += "<input type='number' id='"+_field_id+"'><br>"

        return _field_html

    def _parse_fl_field(self, _field):
        #return the html string
        _field_id = _field['id']
        _field_html = "<p>"+_field['title']+"</p>";
        if _field['required']==True:
            _field_html += "<input type='file' id='"+_field_id+"' required='required'><br>"
        else:
            _field_html += "<input type='file' id='"+_field_id+"'><br>"

        return _field_html

    def _parse_mcqs_field(self, _field):
        #return the html string
        _field_id = _field['id']
        _field_title = _field['title']
        _field_html = "<div id='"+_field_id+"'><p>"+_field_title+"</p>"
        if _field['required']==True:
            _field_html += "<input type='file' id='"+_field_id+"' required='required'><br>"
        else:
            _field_html += "<input type='file' id='"+_field_id+"'><br>"

        for _option in _field['options']:
            if _field['required']==True:
                option_html="<label><input type='radio' name='"+_option['name']+"' value='"+_option['value']+"' required>"+_option['value']+"</label><br>";
            else:
                option_html="<label><input type='radio' name='"+_option['name']+"' value='"+_option['value']+"' >"+_option['value']+"</label><br>";

        _field_html+="</div>"
        return _field_html

    def _parse_mcqm_field(self, _field):
        #return the html string
        _field_id = _field['id']
        _field_title = _field['title']
        _field_html = "<div id='"+_field_id+"'><p>"+_field_title+"</p>"
        if _field['required']==True:
            _field_html += "<input type='file' id='"+_field_id+"' required='required'><br>"
        else:
            _field_html += "<input type='file' id='"+_field_id+"'><br>"

        for _option in _field['options']:
            if _field['required']==True:
                option_html="<label><input type='checkbox' name='"+_option['name']+"' value='"+_option['value']+"' required>"+_option['value']+"</label><br>";
            else:
                option_html="<label><input type='checkbox' name='"+_option['name']+"' value='"+_option['value']+"' >"+_option['value']+"</label><br>";

        _field_html+="</div>"
        return _field_html
