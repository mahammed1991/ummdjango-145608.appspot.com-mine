$(document).ready(function(){

    var cateSubTaskList = [];

    BudgetBandTableLoad()
    
    comboData();

    $('a.main-category').click(function () {
        taskList(this.id);

        for(i=0; i<cateList.length; i++){
            if(cateList[i]==this.id)
            {
                $("#"+this.id).addClass("make-active");
            }
            else
            {
                $("#" + cateList[i]).removeClass("make-active");
            }
        }
    });

    var callback_id = localStorage.getItem("id");

    if (callback_id != ' ')
    {
        var parent_id = localStorage.getItem("parent_id");
        TableLoad(callback_id);
        reload_tasks(parent_id, callback_id);
        localStorage.setItem("id",' ');
    }
    else
    {
        elem_id = $('ul.main-option li:first-child a').attr('id');
        $("#"+elem_id).addClass("make-active");
        taskList(elem_id);
    }
});

function reload_tasks(parent_id, callback_id)
{
    $.ajax({
        type: 'GET',
        url: '/task_list/'+ parent_id ,
        dataType: 'json',
        success: function(data, response, xhr)
        {
           $(".sub-task").html('');
           if(data!= null)
            {
                html = null
                global_id = data[0].pk
                cateSubTaskList = [];

                for(i=0; i<data.length; i++)
                {
                    newlink=document.createElement('a');
                    newlink.setAttribute('class',"sub-task-link")
                    link = "subtask_"+data[i].pk
                    newlink.setAttribute('id',link);
                    newlink.innerHTML = data[i].fields.task_name;
                    $('.sub-task').append(newlink);

                    cateSubTaskList.push(link);
                }

                if(data.length >0){
                    link = "subtask_"+callback_id;
                    $("#"+link).addClass("make-active-subtask");
                }

                $('.sub-task-link').bind('click', function(event) {
                    subtaskid = event.target.id.toString();
                    subtaskid = subtaskid.replace("subtask_","");
                    TableLoad(subtaskid);
                    PitchDataLoad(subtaskid);
                    RightTableLoad(subtaskid);

                    for(i=0; i<cateSubTaskList.length; i++)
                        {
                            if(cateSubTaskList[i]==event.target.id)
                            {
                                $("#"+event.target.id).addClass("make-active-subtask");
                            }
                            else
                            {
                                $("#" + cateSubTaskList[i]).removeClass("make-active-subtask");
                            }
                        }
                    });
            }

        },
        error:function(error)
        {
            console.log(error);
        }
    });
}

function comboData(){
$.ajax({
        type: 'GET',
        url: '/combodata/',
        dataType: 'json',
        success: function(data, response, xhr)
        {
            $('.looper').looper({
               
            });
            for(i=0; i<data.length; i++)
            {
                mytag=document.createElement('a');
                mytag.setAttribute('id',data[i].pk);
                mytag.setAttribute('class', "item");
                mytag.innerHTML = data[i].fields.title;
                $('.myclass').append(mytag);
            }
            $('.myclass').click(function(){
                $('.mytable').empty();
                for(i=0; i<data.length; i++)
                {
                    tablerow = document.createElement('tr');
                    tablerow.setAttribute('class',"myrow" + i);
                    $('.mytable').append(tablerow);
                    newlink1=document.createElement('td');
                    newlink1.innerHTML = data[i].fields.title
                    $('.myrow' + i).append(newlink1)
                    newlink2=document.createElement('td');
                    newlink2.innerHTML = data[i].fields.description
                    $('.myrow'+ i).append(newlink2)
                }
            });
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function taskList(id){
    cateSubTaskList = [];

    $.ajax({
        type: 'GET',
        url: '/task_list/'+ id ,
        dataType: 'json',
        success: function(data, response, xhr)
        {
            createSubTasks(data)
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function createSubTasks(data){
    global_id = null;
    $('.sub-task-link').remove()
    $('#key_data').remove()
    $('#value_data').remove()
    $('#key_row').empty()
    $('#value_row').empty()
    if(data!= null)
    {
        html = null
        global_id = data[0].pk
        for(i=0; i<data.length; i++)
        {
            newlink=document.createElement('a');
            newlink.setAttribute('class',"sub-task-link")
            link = "subtask_"+data[i].pk
            newlink.setAttribute('id',link);
            newlink.innerHTML = data[i].fields.task_name;
            $('.sub-task').append(newlink);

            cateSubTaskList.push(link);
        }

        if(data.length >0){
            link = "subtask_"+data[0].pk;
             $("#"+link).addClass("make-active-subtask");
        }
        
        TableLoad(global_id);
        PitchDataLoad(global_id);
        RightTableLoad(global_id);
    }


$('.sub-task-link').bind('click', function(event) {
    subtaskid = event.target.id.toString();
    subtaskid = subtaskid.replace("subtask_","");
    TableLoad(subtaskid);
    PitchDataLoad(subtaskid);
    RightTableLoad(subtaskid);

    for(i=0; i<cateSubTaskList.length; i++)
        {
            if(cateSubTaskList[i]==event.target.id)
            {
                $("#"+event.target.id).addClass("make-active-subtask");
            }
            else
            {
                $("#" + cateSubTaskList[i]).removeClass("make-active-subtask");
            }
        }
    });
}


function TableLoad(taskid){
    $('#key_row').empty()
    $('#value_row').empty()
    $.ajax({
        type: 'GET',
        url: '/left_column_list/'+ taskid ,
        dataType: 'json',
        success: function(data, response, xhr)
        {
            console.log(data);
            if(data!= null)
            {
                for(i=0; i<data.length; i++)
                {
                    newlink1=document.createElement('th');
                    newlink1.innerHTML = data[i].fields.column_name
                    $('#key_row').append(newlink1);
                    newlink2=document.createElement('td');
                    newlink2.innerHTML = data[i].fields.column_value
                    $('#value_row').append(newlink2)
                }
            }
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function PitchDataLoad(taskid){

    $('#elevator_data').empty()
    
    $.ajax({
        type: 'GET',
        url: '/elevator_pitch_data/'+ taskid ,
        dataType: 'json',
        success: function(data, response, xhr)
        {
            
            $('#elevator_data').append(data[0].fields.elevator_pitch)
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function RightTableLoad(taskid){

    document.getElementById("myModalLabel").innerHTML = document.getElementById("subtask_"+taskid).innerHTML;

    $.ajax({
        type: 'GET',
        url: '/right_column_list/'+ taskid ,
        dataType: 'json',
        success: function(data, response, xhr)
        {
            $('.tab-pane').text('');
            $('.modal-body #epitch').append(data[0].fields.email_pitch_guidelines)
            $('.modal-body #impl').append(data[0].fields.implementation_guide)
            $('.modal-body #faq').append(data[0].fields.faq)

            $('a#email_pitch').click(function(){
                $('#impl').removeClass('active');
                $('#faq').removeClass('active');
                $('#epitch').addClass('active');
                
                $('ul.nav.nav-tabs li:nth-child(3)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(2)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(1)').addClass('active');
            });
            $('a#implementation').click(function(){
                $('#epitch').removeClass('active');
                $('#faq').removeClass('active');
                $('#impl').addClass('active');

                $('ul.nav.nav-tabs li:nth-child(1)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(3)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(2)').addClass('active');
            });

            $('a#faq').click(function(){
                $('#epitch').removeClass('active');
                $('#impl').removeClass('active');
                $('#faq').addClass('active');

                $('ul.nav.nav-tabs li:nth-child(1)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(2)').removeClass('active');
                $('ul.nav.nav-tabs li:nth-child(3)').addClass('active');
            });


        },
        error:function(error)
        {
            console.log(error);
        }
    });
}


function BudgetBandTableLoad(){ 
    $.ajax({
        type: 'GET',
        url: '/budget_band/',
        dataType: 'json',
        success: function(data, response, xhr)
        {
            $('a#budget_band').click(function(){
                $('.modal-body .budget-body').empty();
                $('.budget-body').append(data[0].fields.band_details)
            }); 
        },
        error:function(error)
        {
            console.log(error);
        }
    });
}

