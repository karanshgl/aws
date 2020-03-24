$(document).ready(function(){

    let curr_section = 0;

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
        console.log("Added section #"+String(curr_section));
    }

    //function for adding a string field to the dynamic form
    function addStrngField(title, required){
        section_id = getCurrSectionID();
        section_selector = getSelectorByID(section_id);
        console.log(section_selector);
        let field_id = section_id+"_"+removeWhitespace(title);
        let label_html = "<label for='"+field_id+"'>"+title+":  </label>";
        let input_html="";
        if (required==true)
            input_html = "<input type='text' id='"+field_id+"' required='required'><br>";
        else
            input_html = "<input type='text' id='"+field_id+"'><br>";
        console.log(field_id);
        console.log(label_html);
        console.log(input_html);
        $(section_selector).append(label_html+input_html);
    }

    $("#add_section").click(function(){
        console.log("Adding section....");
        addSection();
    });

    $("#type_of_field").change(function(){
        var selected = $( "#type_of_field option:selected" ).val();
        console.log("Type of field is now "+selected);
    });

    $("#add_field_form").submit(function(event){
        var selected = $( "#type_of_field option:selected" ).val();
        //title and required are common attributes for all the field types
        var title =$("#title_of_field").val();
        var required = $("#required_field").is(":checked");
    
        // alert("Submitted");
    
        // log the results
        console.log(selected);
        console.log(title);
        console.log(required);
        
        //check if the user has added any sections at all
        if(curr_section==0) {
            alert('Add a section first');
            throw 'Error: Add a section first';
        }


        //if field type is string...
        if (selected==="strng"){
            //inject code in the dynamic-form for this field
            addStrngField(title, required);
        }
        //if field type is int...
        else if(selected=='intgr'){
    
        }
        //if field type is mcq_single....
        else if(selected=='mcq_single'){
    
        }
        //if field type is mcq_multiple...
        else if(selected=='mcq_multi'){
    
        }
        //if field type is file upload...
        else if(selected=='fl'){
            
        }
        else{
            throw "Error: Invalid Field Type";
        }

        event.preventDefault();
    });

});

