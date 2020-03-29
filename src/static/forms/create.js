class FormBlueprint{
    constructor(id){
        this.id=id;
        this.sections = new Array();
    }

    // get id(){
    //     return this.id;
    // }

    // get sections(){
    //     return this.sections;
    // }

    addSection(section){
        this.sections.push(section);
    }
}
//the Field class
class Field{
    constructor(type, title, required){
        this.type = type;
        this.title = title;
        this.required = required;
        this.options = new Array();
    }

    // get type(){
    //     return this.type;
    // }
    // get title(){
    //     return this.title;
    // }
    // get required(){
    //     return this.required;
    // }
    // get options(){
    //     return this.options;
    // }

    addOption(option){
        this.options.push(option);
    }
}
//the Section class
class Section{
    constructor(id){
        this.id = id;
        this.fields = new Array();
    }

    // get id(){
    //     return this.id;
    // }

    // get fields(){
    //     return this.fields;
    // }

    addField(field){
        this.fields.push(field);
    }
}

$(document).ready(function(){

    //the section the user is adding fields to right now
    let curr_section = 0;

    //create the form object
    let fb = new FormBlueprint(1);

    //utility function to convert ID to selector
    function removeWhitespace(text){
        return text.replace(/ /g,'');
    }

    function getSelectorByID(id){
        return "#"+id;
    }
    //using the section_<curr_section> to name the sections of the form
    function getCurrSectionID(){
        return "section_"+String(curr_section);
    }

    //function for adding a section in the form
    function addSection(){
        curr_section+=1;
        $("#dynamic-form").append("<section id='section_"+String(curr_section)+"'><h4>Section "+curr_section+"</h4></section>");
    
        //add the section in the form object as well
        let section = new Section(curr_section);
        fb.addSection(section);

    }

    //function for adding a string field to the dynamic form
    function addStrngField(title, required){
        section_id = getCurrSectionID();
        section_selector = getSelectorByID(section_id);
        let field_id = section_id+"_"+removeWhitespace(title)+'_strng';
        let label_html = "<p>"+title+":  </p>";
        let input_html="";
        if (required==true)
            input_html = "<input type='text' id='"+field_id+"' required='required'><br>";
        else
            input_html = "<input type='text' id='"+field_id+"'><br>";

        $(section_selector).append(label_html+input_html);

        //create the field object for JS object
        let field = new Field('strng', title, required);
        //add this field to the section
        fb.sections[curr_section-1].addField(field);
    }
    //this function is called when the user adds an integer field to the form
    function addIntgrField(title, required){
        section_id = getCurrSectionID();
        section_selector = getSelectorByID(section_id);
        let field_id = section_id+"_"+removeWhitespace(title)+'_intgr';
        let label_html = "<p>"+title+":  </p>";
        let input_html="";
        if (required==true)
            input_html = "<input type='number' id='"+field_id+"' required='required'><br>";
        else
            input_html = "<input type='number' id='"+field_id+"'><br>";
        $(section_selector).append(label_html+input_html);
        //create the field object for JS object
        let field = new Field('intgr', title, required);
        //add this field to the section
        fb.sections[curr_section-1].addField(field);
    }
    //this function is called when the user adds a file field
    function addFLField(title, required){
        section_id = getCurrSectionID();
        section_selector = getSelectorByID(section_id);
        let field_id = section_id+"_"+removeWhitespace(title)+'_fl';
        let label_html = "<p>"+title+":  </p>";
        let input_html="";
        if (required==true)
            input_html = "<input type='file' id='"+field_id+"' required='required'><br>";
        else
            input_html = "<input type='file' id='"+field_id+"'><br>";

        $(section_selector).append(label_html+input_html);
        //create the field object for JS object
        let field = new Field('fl', title, required);
        //add this field to the section
        fb.sections[curr_section-1].addField(field);
    }
    //this function is called when the user adds a mcqs field to the form
    function addMCQSField(title, required){
        section_id = getCurrSectionID();
        section_selector = getSelectorByID(section_id);
        let field_id = section_id+"_"+removeWhitespace(title)+'_mcqs';
        //means add p element as a question
        let p_html = "<div id='"+field_id+"'><p>"+title+"</p></div>";
        $(section_selector).append(p_html);

        //create the field object for JS object
        let field = new Field('mcqs', title, required);
        //add this field to the section
        fb.sections[curr_section-1].addField(field);
    }
    //this function is called when an option is to be added to the mcqs field
    function addMCQSOption(title, option, required){
        //this function is called when an option is added to a mcqs field
        //get the id of the div containing the question
        section_id = getCurrSectionID();
        section_selector = getSelectorByID(section_id);
        
        let field_id = section_id+"_"+removeWhitespace(title)+'_mcqs';
        let option_name = field_id+"o";
       
        //now append the options to the MCQS div
        //radio buttons must have the same name value for grouping
        let option_html = "";
        if (required==true){
            option_html="<label><input type='radio' name='"+option_name+"' value='"+option+"' required>"+option+"</label><br>";
        }
        else{
            option_html="<label><input type='radio' name='"+option_name+"' value='"+option+"' >"+option+"</label><br>";
        }
        $(getSelectorByID(field_id)).append(option_html);
        //add the option
        fb.sections[curr_section-1].fields[fb.sections[curr_section-1].fields.length-1].addOption(option);
    }

    //this function is called when the user adds a mcqm field to the form
    function addMCQMField(title, required){
        section_id = getCurrSectionID();
        section_selector = getSelectorByID(section_id);
        let field_id = section_id+"_"+removeWhitespace(title)+'_mcqm';
        //means add p element as a question
        let p_html = "<div id='"+field_id+"'><p>"+title+"</p></div>";
        $(section_selector).append(p_html);

        //create the field object for JS object
        let field = new Field('mcqm', title, required);
        //add this field to the section
        fb.sections[curr_section-1].addField(field);
    }

    //this function is called when an option is to be added to the mcqs field
    function addMCQMOption(title, option, required){
        //this function is called when an option is added to a mcqm field
        //get the id of the div containing the question
        section_id = getCurrSectionID();
        section_selector = getSelectorByID(section_id);
        
        let field_id = section_id+"_"+removeWhitespace(title)+'_mcqm';
        let option_name = field_id+"o";
        //now append the options to the MCQS div
        //radio buttons must have the same name value for grouping
        let option_html = "";
        if (required==true){
            option_html="<label><input type='checkbox' name='"+option_name+"' value='"+option+"' required>"+option+"</label><br>";
        }
        else{
            option_html="<label><input type='checkbox' name='"+option_name+"' value='"+option+"' >"+option+"</label><br>";
        }
        $(getSelectorByID(field_id)).append(option_html);
        //add the option
        fb.sections[curr_section-1].fields[fb.sections[curr_section-1].fields.length-1].addOption(option);
    }

    $("#add_section").click(function(){
        addSection();
    });

    $("#type_of_field").change(function(){
        let selected = $( "#type_of_field option:selected" ).val();
        //if field is of type strng 
        if(selected==='strng' || selected=='intgr' || selected=='file'){
            $(getSelectorByID('optional_div')).hide();
        }

        //if field is of type mcqs....the we need to change the div
        else if (selected==='mcqs' || selected=='mcqm'){
            $(getSelectorByID('optional_div')).show();
        }
    });

    $("#add_field_form").submit(function(event){
        let selected = $( "#type_of_field option:selected" ).val();
        //title and required are common attributes for all the field types
        let title =$("#title_of_field").val();
        let required = $("#required_field").is(":checked");
    
        // alert("Submitted");
    
        //check if the user has added any sections at all
        if(curr_section==0) {
            alert('Add a section first');
            event.preventDefault();
            throw 'Error: Add a section first';
        }


        //if field type is string...
        if (selected==="strng"){
            //inject code in the dynamic-form for this field
            addStrngField(title, required);
        }
        //if field type is int...
        else if(selected=='intgr'){
            addIntgrField(title, required);
        }
        //if field type is mcqs....
        else if(selected=='mcqs'){
            addMCQSField(title, required);
        }
        //if field type is mcqmple...
        else if(selected=='mcqm'){
            addMCQMField(title, required);
        }
        //if field type is file upload...
        else if(selected=='fl'){
            addFLField(title, required);
        }
        else{
            event.preventDefault();
            throw "Error: Invalid Field Type";
        }

        event.preventDefault();
    });

    //function called when 'add_option_form' is submitted
    $('#add_option_form').submit(function(event){
        let title =$("#title_of_field").val();
        let selected = $( "#type_of_field option:selected" ).val();
        let required = $("#required_field").is(":checked");
        //title and required are common attributes for all the field types
        let option =$("#option_text").val();
       
        if(selected=='mcqs')addMCQSOption(title, option, required);
        else if(selected=='mcqm')addMCQMOption(title, option, required);
        else throw "Error: Select MCQ type field to add option";
        event.preventDefault();
    });

    //functions dealing with POSTing the data to the server
    $('#log_btn').click(function(){
        let json = JSON.stringify(fb);
        console.log(json);


        $.ajax({
            beforeSend: function(request) {
                let csrftoken = Cookies.get('csrftoken');
                console.log(csrftoken);
                request.setRequestHeader('X-CSRFToken', csrftoken);
            },
            type: "POST",
            url: "/forms/fb_create/",
            data: {
                'fb': json, // from form
            },
            success: function () {
                alert('Request Sent Successfully');
            }

        });

    });

});

