class FormBlueprintParser:
    def __init__(self):
        self.html = "";

    def parse_section(self, dic, section_id):
        """
        args:
            section_id: is one-indexed
        """
        _section = dic['sections'][section_id-1]
        return self._parse_section(_section), _section['node_id']

    def parse(self, dic):
        _html = "<div class='container'><div class='row'><div class='col-md-1'></div><div class='col-md-10'><div class='jumbotron'><h4>Form Preview</h4></div></div><div class='col-md-1'></div></div>"
        _html+="<div class='row'><div class='col-md-1'></div><div class='col-md-10'>"
        # _html = ""
        for section in dic['sections']:
            _html += self._parse_section(section)

        _html += "</div><div class='col-md-1'></div></div></div>"
        return  _html

    def _parse_section(self, section):
        _id = section['id'].split('_')[-1]
        _section_html = "<section class='card' id='section_"+_id+"'>"
        _section_html +="<div class='card-header'><h4>Section "+_id+"</h4></div><div class='card-body'>"
        for _field in section['fields']:
            # print(_field['id'])
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
        _section_html += "</div></section><br>"
        return _section_html

    def _parse_string_field(self, field):
        #return the html string
        _field_id = field['id']
        _field_html = "<div class='form-group'>"
        _field_html += "<label for='"+_field_id+"'>"+field['title']+"</label>";
        if field['required']==True:
            _field_html += "<input class='form-control' type='text' id='"+_field_id+"' name='"+_field_id+"' required='required'><br>"
        else:
            _field_html += "<input class='form-control' type='text' id='"+_field_id+"' name='"+_field_id+"'><br>"
        _field_html+='</div>'
        return _field_html

    def _parse_integer_field(self, field):
        #return the html string
        _field_id = field['id']
        _field_html = "<div class='form-group'>"
        _field_html += "<label for='"+_field_id+"'>"+field['title']+"</label>";
        if field['required']==True:
            _field_html += "<input class='form-control' type='number' id='"+_field_id+"' name='"+_field_id+"' required='required'><br>"
        else:
            _field_html += "<input class='form-control' type='number' id='"+_field_id+"' name='"+_field_id+"' ><br>"
        _field_html+='</div>'
        return _field_html

    def _parse_fl_field(self, _field):
        #return the html string
        _field_id = _field['id']
        _field_html = "<div class='form-group'>"
        _field_html += "<label for='"+_field_id+"'>"+_field['title']+"</label>";
        if _field['required']==True:
            _field_html += "<input class='form-file' type='file' id='"+_field_id+"' name='"+_field_id+"'  required='required'><br>"
        else:
            _field_html += "<input class='form-file' type='file' id='"+_field_id+"' name='"+_field_id+"' ><br>"
        _field_html+='</div>'
        return _field_html

    def _parse_mcqs_field(self, _field):
        #return the html string
        _field_id = _field['id']
        _field_title = _field['title']
        _field_html = "<div id='"+_field_id+"'><p>"+_field_title+"</p>"

        for _option in _field['options']:
            if _field['required']==True:
                _field_html+="<div class='form-check'><label class='form-check-label'><input type='radio' name='"+_option['name']+"' value='"+_option['value']+"' required>"+_option['value']+"</label></div><br>";
            else:
                _field_html+="<div class='form-check'><label class='form-check-label'><input type='radio' name='"+_option['name']+"' value='"+_option['value']+"' >"+_option['value']+"</label></div><br>";

        _field_html+="</div>"
        return _field_html

    def _parse_mcqm_field(self, _field):
        #return the html string
        _field_id = _field['id']
        _field_title = _field['title']
        _field_html = "<div id='"+_field_id+"'><p>"+_field_title+"</p>"

        for _option in _field['options']:
            if _field['required']==True:
                _field_html+="<div class='form-check'><label class='form-check-label'><input type='checkbox' name='"+_option['name']+"' value='"+_option['value']+"' required>"+_option['value']+"</label></div><br>";
            else:
                _field_html+="<div class='form-check'><label class='form-check-label'><input type='checkbox' name='"+_option['name']+"' value='"+_option['value']+"' >"+_option['value']+"</label></div><br>";

        _field_html+="</div>"
        return _field_html
